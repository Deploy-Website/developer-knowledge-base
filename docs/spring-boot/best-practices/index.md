# Spring Boot Best Practices Hub

> **Trọng tâm**: Các quy chuẩn thực hành sản xuất cho hệ sinh thái Spring Boot 3.3+ (Spring Framework 6.1+ & Java 21 LTS), tập trung vào Giao tiếp mạng bền bỉ (Resilient WebClient & HTTP Clients), Tối ưu hóa tầng dữ liệu (Hibernate & HikariCP), Quản trị giao dịch (`@Transactional`), và Khả năng quan sát (Production Observability & Metrics).  
> **Nguyên tắc kỹ thuật**: Tuân thủ tài liệu chính thức từ [Spring Boot Reference Guide](https://docs.spring.io/spring-boot/reference/) và [Reactor Netty Reference](https://projectreactor.io/docs/netty/release/reference/index.html).

---

## 1. Mục Tiêu & Triết Lý Thực Hành Spring Boot

Spring Boot giúp khởi tạo ứng dụng nhanh chóng nhờ cơ chế Auto-configuration. Tuy nhiên, các giá trị mặc định của Spring (chẳng hạn timeout không giới hạn của `RestTemplate`/`WebClient`, connection pool mặc định, hoặc cấu hình OSIV) được thiết kế cho sự tiện lợi khi phát triển (development convenience), hoàn toàn không an toàn trong môi trường Production.

Kho lưu trữ Best Practices của Spring Boot hướng tới:
1. **Phòng vệ chủ động trước sự cố mạng (Network Resilience)**: Mọi cuộc gọi qua mạng bắt buộc phải có timeout rõ ràng (Connection, Read, Write, Response) và giới hạn số lượng connection.
2. **Bảo vệ tài nguyên Database**: Ngăn chặn rò rỉ kết nối (Connection Leaks), triệt tiêu lỗi N+1 Query, và tắt hoàn toàn Open Session in View (`OSIV = false`).
3. **Thân thiện với Virtual Threads & Non-blocking I/O**: Định hình kiến trúc phù hợp khi kết hợp Spring MVC với Virtual Threads hoặc Spring WebFlux với Reactor Netty.

---

## 2. Danh Mục Các Thực Hành Đã Chuẩn Hóa (Curated Best Practices)

| Chủ đề / Bài viết | Trọng tâm kỹ thuật | Mức độ bằng chứng | Liên kết chuẩn |
| :--- | :--- | :--- | :--- |
| 🌐 **[Cấu Hình WebClient Kháng Lỗi (Resilient WebClient)](resilient-webclient.md)** | Cấu hình toàn diện 4 loại timeout với Reactor Netty `HttpClient`, định cỡ Connection Pool, chiến lược Retry có Exponential Backoff & Jitter, và cạm bẫy `.block()`. | **Official Guidance** | [Spring Docs](https://docs.spring.io/spring-framework/reference/web/webflux-webclient.html) & Reactor Netty |

---

## 3. Hệ Thống Cấp Độ Bằng Chứng (Evidence Classification)

Mỗi thực hành trong danh mục được gắn nhãn minh bạch:
- 🟢 **Official Guidance**: Khuyến nghị chuẩn từ [Spring Projects Documentation](https://docs.spring.io/).
- 🔵 **Verified Experiment**: Đã kiểm chứng qua tải cao (JMeter/k6 stress tests) trong môi trường staging.
- 🟡 **Context-specific Finding**: Cấu hình phụ thuộc vào đặc thù downstream services hoặc hạ tầng Kubernetes.
- ⚪ **Candidate**: Đang trong giai đoạn đánh giá.

---

## 4. Liên Kết Tri Thức Liên Quan

- **Lý thuyết nền tảng**:
  - [Spring Boot Ecosystem Knowledge Hub: Core, JPA & HikariCP](../index.md)
  - [Modern Java Best Practices: Robust Exception Handling](../../java/best-practices/exception-handling.md)
- **Tài liệu chính thức**:
  - [Spring Boot 3.3 Reference Documentation](https://docs.spring.io/spring-boot/reference/)
  - [Reactor Netty Documentation](https://projectreactor.io/docs/netty/release/reference/index.html)
