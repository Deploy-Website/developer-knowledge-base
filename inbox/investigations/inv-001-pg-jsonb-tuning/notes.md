# Raw Investigation Notes: PostgreSQL JSONB Query Latency & Index Bloat

> **Mã điều tra (ID)**: inv-202610-pg-jsonb-tuning  
> **Ngày bắt đầu**: 2026-10-15  
> **Người thực hiện**: Senior Backend Architect  
> **Lĩnh vực**: PostgreSQL 16 on Linux x86_64  
> **Môi trường**: Staging Cluster (tương đương 2.500.000 records production)  
> **Trạng thái**: RESOLVED  

---

## 1. Vấn Đề Ban Đầu (Initial Problem Statement)
- Endpoint `/api/v1/events/search` lọc các thuộc tính động trong cột `payload` (`jsonb`) của bảng `audit_events` bị chậm đột biến: P99 latency từ 15ms vọt lên 420ms sau khi bảng vượt ngưỡng 2 triệu rows.
- Cột `payload` chứa metadata biến đổi (ví dụ: `{"tenant_id": "t-102", "action": "LOGIN", "client_ip": "10.0.4.12", "device": {"os": "iOS", "version": "17.4"}}`).
- Dữ liệu text trong jsonb làm tăng kích thước bảng lên 4.8GB (TOAST storage).

---

## 2. Các Câu Hỏi Đặt Ra (Questions to Investigate)
- [x] Q1: Tại sao câu truy vấn lọc theo key lồng nhau `payload @> '{"device": {"os": "iOS"}}'` lại fallback về Sequential Scan?
- [x] Q2: Sử dụng B-tree index trên expression hay GIN index là tối ưu cho payload động?
- [x] Q3: Làm thế nào để giảm index bloat và write amplification khi bảng có lưu lượng insert 1.000 records/giây?

---

## 3. Nhật Ký Tiến Trình Thí Nghiệm (Chronological Log)

### [2026-10-15 09:30] Bước 1: Baseline & Thử nghiệm B-Tree Expression Index
- **Câu hỏi**: Có thể dùng B-Tree index thông thường để tránh chi phí GIN nặng nề không?
- **Giả thuyết**: Tạo B-Tree index trên `((payload->'device'->>'os'))` sẽ giải quyết được query lọc OS.
- **Hành động**:
  ```sql
  -- Chạy query baseline không có index
  EXPLAIN (ANALYZE, BUFFERS)
  SELECT id, created_at, payload 
  FROM audit_events 
  WHERE payload->'device'->>'os' = 'iOS';

  -- Tạo B-Tree expression index
  CREATE INDEX idx_events_device_os ON audit_events (((payload->'device'->>'os')));
  ```
- **Kết quả quan sát**:
  - Baseline query: `Parallel Seq Scan`, cost=0.00..58430.00, actual time=421.350 ms, Buffers: shared read=38210.
  - Sau khi tạo B-Tree: Query trên chạy bằng `Index Scan`, actual time giảm xuống 2.450 ms.
- **Phân tích**: B-Tree chỉ hỗ trợ đúng một biểu thức cụ thể. Khi người dùng lọc theo `action = 'LOGIN'` hoặc `tenant_id`, query lại quay về `Seq Scan` (420ms). Không thể tạo hàng chục B-Tree expression index cho các trường động vì làm tê liệt tốc độ `INSERT`.
- **Đánh giá**: **Thất bại một phần (Failed to solve dynamic filtering)**. Chỉ là giải pháp chắp vá cho 1 trường đơn lẻ.
- **Quyết định kế tiếp**: Phải chuyển sang GIN index để hỗ trợ toán tử chứa `@>` trên toàn bộ cấu trúc JSONB.

---

### [2026-10-15 14:15] Bước 2: Thử nghiệm GIN index mặc định (`jsonb_ops`)
- **Câu hỏi**: GIN index mặc định có đáp ứng được toàn bộ các truy vấn chứa `@>` không?
- **Giả thuyết**: GIN index mặc định sẽ index mọi key và value trong JSON document.
- **Hành động**:
  ```sql
  DROP INDEX idx_events_device_os;
  CREATE INDEX idx_events_payload_gin ON audit_events USING gin (payload);
  ```
- **Kết quả quan sát**:
  - Query: `WHERE payload @> '{"device": {"os": "iOS"}}'`
  - Kế hoạch: `Bitmap Index Scan on idx_events_payload_gin`, actual time=46.210 ms.
  - Kích thước index: `pg_relation_size('idx_events_payload_gin')` = **1.28 GB** (chiếm gần 30% kích thước bảng chính!).
  - Thời gian benchmark `INSERT 10.000 rows`: Tăng từ 1.8s lên 6.4s (Write throughput giảm 3.5 lần).
- **Phân tích**: GIN `jsonb_ops` mặc định index từng path, từng key và từng value thành các entry riêng biệt. Với document nhiều tầng, nó tạo ra quá nhiều posting lists trong GIN tree, gây bloat và write amplification khổng lồ.
- **Đánh giá**: **Không tối ưu cho production có write load cao (Severe Index Bloat)**.
- **Quyết định kế tiếp**: Thử nghiệm operator class chuyên biệt `jsonb_path_ops` kết hợp cấu hình TOAST compression LZ4 trong PostgreSQL 14+.

---

### [2026-10-15 17:00] Bước 3: Thử nghiệm GIN `jsonb_path_ops` + LZ4 Compression
- **Câu hỏi**: `jsonb_path_ops` giảm được bao nhiêu dung lượng và cải thiện thời gian query ra sao?
- **Giả thuyết**: `jsonb_path_ops` chỉ hash toàn bộ đường dẫn từ root tới leaf (ví dụ: hash của `device.os.iOS`), không index các key độc lập, giúp giảm 70% kích thước index.
- **Hành động**:
  ```sql
  DROP INDEX idx_events_payload_gin;

  -- Kích hoạt LZ4 compression cho TOAST (PostgreSQL 14+)
  ALTER TABLE audit_events ALTER COLUMN payload SET COMPRESSION lz4;

  -- Tạo GIN index tối ưu hóa theo path hash
  CREATE INDEX idx_events_payload_path ON audit_events USING gin (payload jsonb_path_ops);
  ```
- **Kết quả quan sát**:
  - Kích thước index: giảm từ 1.28 GB xuống còn **214 MB** (Giảm ~83%!).
  - Query time: `WHERE payload @> '{"device": {"os": "iOS"}}'` -> `actual time = 8.420 ms` (Nhanh gấp 5 lần so với `jsonb_ops` do mảng bitmap nhỏ hơn nhiều trong RAM).
  - Tốc độ `INSERT 10.000 rows`: 2.1s (Gần tương đương lúc không có index).
- **Phân tích**: `jsonb_path_ops` chỉ lưu trữ 32-bit hash của mỗi giá trị kèm đường dẫn, triệt tiêu tình trạng posting list phình to. Kết hợp nén LZ4 giúp giảm CPU overhead khi decompress TOAST pages từ Disk vào Shared Buffers.
- **Đánh giá**: **Thành công vượt bậc (Optimal Solution)**.

---

## 4. Kết Quả & Đúc Kết
- **Giải pháp chính thức**: Áp dụng `jsonb_path_ops` và LZ4 compression.
- **Hạn chế được ghi nhận**: `jsonb_path_ops` không hỗ trợ toán tử kiểm tra sự tồn tại của key `?`, `?|`, `?&` (chỉ hỗ trợ `@>`). Ứng dụng chỉ sử dụng `@>` nên hoàn toàn phù hợp.
