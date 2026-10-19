# System Design & Distributed Systems Best Practices Hub

> **Trọng tâm**: Các quy chuẩn thực hành thiết kế hệ thống phân tán chịu tải cao (High-Load Distributed Systems), tập trung vào Xử lý Tính lũy thừa & Chống trùng lặp (Idempotency & Deduplication), Mẫu hình giao dịch phân tán (Transactional Outbox & Saga Patterns), Cơ chế phòng vệ tự động (Circuit Breaker & Rate Limiting), và Chiến lược phân mảnh bộ nhớ đệm (Cache Invalidation).  
> **Nguyên tắc kỹ thuật**: Đối chiếu các định lý nền tảng (CAP, PACELC) và tác phẩm kinh điển [*Designing Data-Intensive Applications*](https://dataintensive.net/) của Martin Kleppmann.

---

## 1. Mục Tiêu & Triết Lý Thực Hành System Design

Trong hệ thống phân tán, sự cố mạng (Network Partitions), độ trễ thất thường (Jitter), và lỗi phần cứng là điều tất yếu xảy ra hàng ngày. Mọi thiết kế phải dựa trên triết lý **"Design for Failure"** (Thiết kế luôn giả định hệ thống con sẽ sập).

Kho lưu trữ Best Practices của System Design tập trung vào:
1. **Tính nhất quán dữ liệu không thỏa hiệp (Data Consistency)**: Giải quyết triệt để vấn đề Dual-Write bằng Transactional Outbox Pattern kết hợp Change Data Capture (CDC).
2. **Xử lý thông điệp Exactly-Once mang tính thực tiễn (Pragmatic Exactly-Once Processing)**: Kết hợp mạng lưới At-Least-Once Delivery với cơ chế nhận diện Idempotency Key tại tầng ứng dụng.
3. **Ngăn chặn sụp đổ dây chuyền (Cascading Failure Prevention)**: Kiểm soát tải bằng Bulkhead, Token Bucket Rate Limiter, và Circuit Breaker.

---

## 2. Danh Mục Các Thực Hành Đã Chuẩn Hóa (Curated Best Practices)

| Chủ đề / Bài viết | Trọng tâm kỹ thuật | Mức độ bằng chứng | Liên kết chuẩn |
| :--- | :--- | :--- | :--- |
| 🔄 **[Thiết Kế Idempotency & Phòng Vệ Sự Cố Phân Tán](idempotency-and-resilience.md)** | Hiện thực hóa Idempotency Key với Redis Distributed Lock và RDBMS unique constraints, giải quyết triệt để lỗi trừ tiền lặp lại do Network Retry. | **Official Guidance** | DDIA & IETF Idempotency-Key Spec |

---

## 3. Hệ Thống Cấp Độ Bằng Chứng (Evidence Classification)

Mỗi thực hành trong danh mục được gắn nhãn minh bạch:
- 🟢 **Official Guidance**: Khuyến nghị từ các tiêu chuẩn công nghiệp (IETF RFCs, sách kinh điển Martin Kleppmann).
- 🔵 **Verified Experiment**: Đã kiểm chứng qua các thử nghiệm giả lập phân vùng mạng (Chaos Engineering / Jepsen tests).
- 🟡 **Context-specific Finding**: Phù hợp với đặc thù kiến trúc lưu trữ nhất định (SQL vs NoSQL).
- ⚪ **Candidate**: Đang trong quá trình nghiên cứu và phát triển.

---

## 4. Liên Kết Tri Thức Liên Quan

- **Lý thuyết nền tảng**:
  - [System Design Knowledge Hub: Distributed Transactions, Outbox & Caching](../index.md)
  - [Spring Boot Best Practices: Resilient WebClient](../../spring-boot/best-practices/resilient-webclient.md)
- **Tài liệu kinh điển**:
  - *Designing Data-Intensive Applications* (Martin Kleppmann, O'Reilly)
