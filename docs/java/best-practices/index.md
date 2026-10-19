# Modern Java Best Practices Hub

> **Trọng tâm**: Các quy chuẩn thực hành sản xuất chuẩn mực cho Modern Java (Java 21 LTS+), tập trung vào Xử lý Ngoại lệ chuẩn mực (Robust Exception Handling), Lập trình đồng thời & Virtual Threads (Concurrency & Project Loom), Tối ưu bộ nhớ & Garbage Collection (ZGC/G1GC), và Modern Language Idioms (Records, Pattern Matching).  
> **Nguyên tắc kỹ thuật**: Tuân thủ triệt để [Effective Java 3rd Edition](https://www.oreilly.com/library/view/effective-java-3rd/9780134686097/), Oracle Java Language Specification, và OpenJDK JEPs.

---

## 1. Mục Tiêu & Triết Lý Thực Hành Modern Java

Java 21 LTS đã mang lại bước nhảy vọt về mô hình đồng thời (Virtual Threads - JEP 444), cú pháp bất biến (Records, Sealed Classes), và các công cụ quản lý tài nguyên. Việc viết code Java kiểu cũ (chẳng hạn bắt `Exception` chung chung, nuốt stack trace, hoặc block OS threads vô tội vạ) là nguồn cơn của nhiều sự cố nghiêm trọng trên production.

Kho lưu trữ Best Practices của Java tập trung vào:
1. **Khả năng quan sát & Chẩn đoán (Debuggability)**: Mọi lỗi phải lưu giữ nguyên nhân gốc rễ (`cause`), không để mất trace ID hoặc ngữ cảnh lỗi.
2. **Tương thích Virtual Threads**: Loại bỏ các anti-patterns gây thread pinning (`synchronized` lâu dài trên I/O) hoặc lãng phí bộ nhớ `ThreadLocal`.
3. **Bất biến & Phòng thủ (Immutability & Defensive Programming)**: Tận dụng Records và Type System để ngăn ngừa trạng thái dữ liệu không hợp lệ ngay từ compile-time.

---

## 2. Danh Mục Các Thực Hành Đã Chuẩn Hóa (Curated Best Practices)

| Chủ đề / Bài viết | Trọng tâm kỹ thuật | Mức độ bằng chứng | Liên kết chuẩn |
| :--- | :--- | :--- | :--- |
| 🛡️ **[Quy Chuẩn Xử Lý Ngoại Lệ (Exception Handling)](exception-handling.md)** | Nguyên tắc chuỗi nguyên nhân (Chained Exceptions), phân biệt Checked vs Unchecked, Custom Exceptions với Domain modeling, và bẫy ngoại lệ trong Virtual Threads. | **Official Guidance** | [JLS Ch. 11](https://docs.oracle.com/javase/specs/jls/se21/html/jls-11.html) & Effective Java |

---

## 3. Hệ Thống Cấp Độ Bằng Chứng (Evidence Classification)

Mỗi thực hành trong danh mục được gắn nhãn minh bạch:
- 🟢 **Official Guidance**: Khuyến nghị chuẩn từ [Oracle Java SE Documentation](https://docs.oracle.com/en/java/javase/21/) và OpenJDK JEPs.
- 🔵 **Verified Experiment**: Đã kiểm chứng qua benchmark thực tế (JMH - Java Microbenchmark Harness) hoặc stress test môi trường production.
- 🟡 **Context-specific Finding**: Tối ưu trong môi trường phần cứng hoặc kiến trúc cụ thể (ví dụ: JVM flags cho container cgroups v2).
- ⚪ **Candidate**: Đang được thử nghiệm và thảo luận.

---

## 4. Liên Kết Tri Thức Liên Quan

- **Lý thuyết nền tảng**:
  - [Modern Java Knowledge Hub: JVM Internals, Memory Model & Virtual Threads](../index.md)
- **Tài liệu chính thức**:
  - [Java SE 21 Documentation](https://docs.oracle.com/en/java/javase/21/)
  - [JEP 444: Virtual Threads](https://openjdk.org/jeps/444)
