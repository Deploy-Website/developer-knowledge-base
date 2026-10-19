# Hands-on Lab: PostgreSQL EXPLAIN ANALYZE Deep Dive

Tài liệu hướng dẫn thực nghiệm đo đạc hiệu năng và phân tích Execution Plan trên cơ sở dữ liệu PostgreSQL 16 chứa **1.000.000 bản ghi**.

---

## 1. Yêu cầu Tiên Quyết (Prerequisites)
- Docker Desktop hoặc Docker Engine đã được cài đặt và đang chạy.
- Docker Compose v2+.

---

## 2. Khởi Động Môi Trường Lab

Từ thư mục gốc của repository, di chuyển vào thư mục lab:

```bash
cd labs/postgresql/explain-analyze
docker compose up -d
```

> [!NOTE]
> Container sẽ tự động nạp tệp `init.sql`, khởi tạo bảng `orders`, sinh ngẫu nhiên 1.000.000 dòng dữ liệu, tạo B-Tree indexes, và chạy `ANALYZE orders;`.
> Quá trình khởi tạo ban đầu mất khoảng 10 - 20 giây tùy tốc độ CPU/Disk.

Kiểm tra trạng thái container:
```bash
docker compose ps
```

---

## 3. Thực Thi Các Kịch Bản Thử Nghiệm

Chạy toàn bộ 5 kịch bản phân tích `EXPLAIN ANALYZE` bằng lệnh:

```bash
docker compose exec postgres psql -U postgres -d knowledgedb -f /scripts/queries.sql
```

Hoặc truy cập trực tiếp vào console `psql` tương tác:
```bash
docker compose exec -it postgres psql -U postgres -d knowledgedb
```

---

## 4. Các Kịch Bản Thực Nghiệm Chi Tiết

### Kịch bản 1: Quét tuần tự (Sequential Scan)
- **Câu lệnh**: Tìm kiếm theo trường văn bản `notes` không có index:
  ```sql
  EXPLAIN (ANALYZE, BUFFERS) SELECT count(*) FROM orders WHERE notes LIKE '%abcde%';
  ```
- **Hiện tượng**: Xuất hiện `Parallel Seq Scan`, quét qua toàn bộ 1 triệu bản ghi, sử dụng nhiều worker threads.

### Kịch bản 2: Quét qua chỉ mục độ chọn lọc cao (Index Scan)
- **Câu lệnh**: Tìm kiếm theo `customer_id = 4289` (chiếm ~20 dòng / 1.000.000 dòng = 0.002%):
  ```sql
  EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE customer_id = 4289;
  ```
- **Hiện tượng**: Xuất hiện `Index Scan using idx_orders_customer_id`, `actual time` chỉ mất dưới 0.1ms, `Buffers: shared hit=4..8`.

### Kịch bản 3: Gom cụm I/O (Bitmap Index Scan & Bitmap Heap Scan)
- **Câu lệnh**: Tìm các đơn hàng trạng thái `REFUNDED` (chiếm ~1% = ~10.000 dòng):
  ```sql
  EXPLAIN (ANALYZE, BUFFERS) SELECT id, customer_id, total_amount, status FROM orders WHERE status = 'REFUNDED';
  ```
- **Hiện tượng**: Xuất hiện `Bitmap Index Scan` để tạo bitmap trong RAM, sau đó `Bitmap Heap Scan` đọc tuần tự các page trên đĩa.

### Kịch bản 4: Tràn bộ nhớ Sort (Disk Spill vs. In-Memory Quicksort)
- **Khi `work_mem = '64kB'`**:
  ```text
  Sort Method: external merge  Disk: 420kB
  ```
- **Khi `work_mem = '16MB'`**:
  ```text
  Sort Method: quicksort  Memory: 650kB
  ```
- **Đánh giá**: Chạy trên RAM nhanh gấp 5-10 lần so với tràn ra đĩa.

### Kịch bản 5: Phân tích câu lệnh DELETE an toàn trong Production
- **Kỹ thuật**: Sử dụng Transaction Block (`BEGIN ... ROLLBACK`) để xem thời gian xóa và số lượng rows bị ảnh hưởng mà không làm mất dữ liệu.

---

## 5. Dọn Dẹp Môi Trường (Teardown)

Sau khi hoàn thành thực nghiệm, dừng container và xóa toàn bộ volume tạm:

```bash
docker compose down -v
```
