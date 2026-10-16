# Biểu Mẫu: Đoạn Mã & SQL Mẫu (Code Recipe Template)

Biểu mẫu chuẩn để lưu trữ các câu lệnh truy vấn SQL nâng cao, script vận hành, hoặc đoạn mã xử lý mẫu đã qua kiểm chứng production.

---

````markdown
# Recipe: [Tên Đoạn Mã / Pattern / Truy Vấn Hữu Ích]

> **Phân loại**: [PostgreSQL / Java / Spring Boot / AWS / System Design]  
> **Mục đích**: [Tóm tắt công dụng của recipe trong 1-2 câu]  
> **Đã kiểm chứng trên môi trường**: [e.g., PostgreSQL 16.2 on Alpine Linux, Java 21 LTS]  
> **Tần suất sử dụng**: [Hàng ngày / Khi tuning / Khi incident]  

---

## 1. Bài Toán & Ứng Dụng Thực Tiễn (Problem & Utility)

- **Vấn đề cần giải quyết nhanh**: Giải thích ngắn gọn tại sao đoạn script / query này tiết kiệm thời gian hoặc giải quyết được một vấn đề hóc búa.

---

## 2. Mã Nguồn Chuẩn Mực (Ready-to-Use Code / SQL)

```sql
-- Dán đoạn script / SQL query hoàn chỉnh có chú thích rõ ràng
SELECT ...
```

---

## 3. Cơ Chế Hoạt Động & Giải Thích Chi Tiết (Deep Explanation)

- **Dòng X-Y**: Giải thích tại sao đoạn logic này lại được viết như vậy.
- **Tại sao tối ưu hơn cách làm thông thường?**: So sánh với các cách tiếp cận ngây thơ (naive approaches).

---

## 4. Các Lưu Ý Về Hiệu Năng & Cạm Bẫy (Performance & Gotchas)

> [!WARNING]
> - **Ảnh hưởng tải (Resource Overhead)**: Đoạn script này có quét toàn bộ RAM hay lock bảng không? Có thể chạy trên Production vào giờ cao điểm không?
> - **Giới hạn**: Khi nào recipe này không còn hiệu quả?

---

## 5. Liên Kết Tới Các Khái Niệm Liên Quan (Related Concepts)

- **Bài viết lý thuyết nền tảng**: `docs/<topic>/<related-article>.md`
- **Troubleshooting Case liên quan**: `docs/<topic>/<related-case>.md`
````
