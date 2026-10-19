# PostgreSQL Best Practices Hub

> **Trọng tâm**: Các quy chuẩn thực hành sản xuất (Production Best Practices) được kiểm chứng cho PostgreSQL 16+, tập trung vào Tối ưu hóa truy vấn (Query Optimization), Thiết kế chỉ mục (Indexing Strategies), Quản trị bộ nhớ & Kết nối (Memory & Connection Pool), và Cơ chế Lưu trữ & Chống Bloat (MVCC & Vacuuming).  
> **Nguyên tắc quản trị**: Phân định rõ mức độ bằng chứng (**Evidence Levels**), giải thích sâu cơ chế bên dưới (**Under the Hood**), và luôn nêu rõ chống chỉ định (**When NOT to use**).

---

## 1. Mục Tiêu & Triết Lý Thực Hành PostgreSQL

PostgreSQL là hệ quản trị cơ sở dữ liệu quan hệ mạnh mẽ với Cost-based Query Optimizer và cơ chế MVCC đặc thù. Việc áp dụng các "mẹo vặt" thiếu hiểu biết kiến trúc thường dẫn tới hậu quả nghiêm trọng: **Index Bloat**, **Lock Starvation**, hoặc **Write Amplification**.

Kho lưu trữ Best Practices của PostgreSQL tuân thủ 3 nguyên tắc:
1. **Dựa trên dữ liệu thực tế (Empirical & Measured)**: Mọi khuyến nghị về hiệu năng phải được chứng minh bằng kế hoạch thực thi (`EXPLAIN (ANALYZE, BUFFERS)`), chỉ số I/O cache hits, hoặc số liệu từ các hồ sơ điều tra thực tế.
2. **Hiểu rõ chi phí đánh đổi (Trade-off Transparency)**: Tăng tốc độ đọc luôn đi kèm chi phí ghi (Write penalty) hoặc chiếm dụng bộ nhớ RAM.
3. **Phù hợp phiên bản (Version-Aware)**: Nêu rõ phiên bản áp dụng (ví dụ: tối ưu LZ4 TOAST compression từ PostgreSQL 14+, nbtree deduplication từ PostgreSQL 13+).

---

## 2. Danh Mục Các Thực Hành Đã Chuẩn Hóa (Curated Best Practices)

| Chủ đề / Bài viết | Trọng tâm kỹ thuật | Mức độ bằng chứng | Liên kết hồ sơ & Lab |
| :--- | :--- | :--- | :--- |
| 🚀 **[Tối Ưu Hóa Truy Vấn & Chỉ Mục JSONB](jsonb-query-optimization.md)** | Sử dụng `jsonb_path_ops` kết hợp nén LZ4 TOAST, tránh bẫy B-Tree expression index đơn lẻ khi lọc đa trường; tăng tốc 50 lần, giảm 83% kích thước index. | **Verified Experiment** | [INV-PG-JSONB-TUNING](../investigations/inv-001-jsonb-tuning.md) |

---

## 3. Hệ Thống Cấp Độ Bằng Chứng (Evidence Classification)

Mỗi thực hành trong danh mục được gắn nhãn minh bạch:
- 🟢 **Official Guidance**: Khuyến nghị chuẩn từ [PostgreSQL Documentation](https://www.postgresql.org/docs/current/).
- 🔵 **Verified Experiment**: Đã chứng minh qua các đợt benchmark nội bộ hoặc hồ sơ điều tra thực tế trong thư mục `docs/postgresql/investigations/`.
- 🟡 **Context-specific Finding**: Có hiệu quả cao trong một kịch bản hạ tầng/workload cụ thể (cần thận trọng khi tổng quát hóa).
- ⚪ **Candidate**: Đang theo dõi và thử nghiệm trong `labs/postgresql/`.

---

## 4. Liên Kết Tri Thức Liên Quan

- **Lý thuyết nền tảng**:
  - [PostgreSQL EXPLAIN ANALYZE: Bản chất & Tối ưu Execution Plan](../explain-analyze.md)
  - [PostgreSQL Overview & Architecture](../index.md)
- **Xử lý sự cố & Điều tra thực tế**:
  - [Troubleshooting: Chẩn đoán & Xử lý Lock Contention](../troubleshooting-locks.md)
  - [Investigation Case: INV-001 JSONB GIN Tuning](../investigations/inv-001-jsonb-tuning.md)
- **Hands-on Lab**:
  - [`labs/postgresql/explain-analyze/`](https://github.com/vinh-nt/developer-knowledge-base/tree/main/labs/postgresql/explain-analyze)
