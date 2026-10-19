---
title: "Cấu Hình Virtual Threads Cho Spring Boot 3.3"
domain: "Spring Boot"
type: "How-to"
source_note: "nodes/spring-boot-virtual-threads.txt"
imported_at: "2026-10-19"
---

# Cấu Hình Virtual Threads Cho Spring Boot 3.3

> **Lĩnh vực (Domain)**: Spring Boot  
> **Phân loại (Type)**: How-to  
> **Tài liệu nguồn (Source)**: `nodes/spring-boot-virtual-threads.txt`  
> **Ngày nhập (Import Date)**: 2026-10-19  

---

## 1. Goal (Mục Tiêu)

Hướng dẫn từng bước thực hiện **Cấu Hình Virtual Threads Cho Spring Boot 3.3** trong môi trường Spring Boot.

---

## 2. Prerequisites (Điều Kiện Tiên Quyết)

- Phiên bản môi trường tương thích (Spring Boot).
- Quyền truy cập hoặc công cụ CLI / IDE cần thiết.

---

## 3. Step-by-step Instructions (Hướng Dẫn Chi Tiết)

Mục tiêu:
Hướng dẫn cấu hình và vận hành Virtual Threads (Project Loom, Java 21 LTS) trong ứng dụng Spring Boot 3.3+ để tăng đột biến thông lượng xử lý các tác vụ I/O blocking (REST calls, database queries) mà không cần chuyển đổi sang lập trình phản ứng (Reactive/WebFlux).

Điều kiện tiên quyết:
- JDK 21 LTS trở lên đã được cài đặt và cấu hình trong JAVA_HOME.
- Spring Boot 3.2.0 hoặc 3.3.x trở lên.
- Sử dụng mô hình Spring MVC tiêu chuẩn (Tomcat nhúng).

Các bước cấu hình chi tiết:

Bước 1: Kích hoạt Virtual Threads trong application.yml
Thêm cấu hình một dòng duy nhất để Spring Boot tự động chuyển đổi Embedded Tomcat Request Threads và TaskExecutor mặc định sang Virtual Threads:

```yaml
spring:
  threads:
    virtual:
      enabled: true
```

Bước 2: Cấu hình AsyncTaskExecutor cho các phương thức @Async (Tùy chọn nâng cao)
Nếu ứng dụng sử dụng @EnableAsync, cấu hình bean ThreadPoolTaskExecutor sử dụng Virtual Thread Factory:

```java
package com.knowledgebase.config;

import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.task.AsyncTaskExecutor;
import org.springframework.core.task.support.TaskExecutorAdapter;

import java.util.concurrent.Executors;

@Configuration
@ConditionalOnProperty(prefix = "spring.threads.virtual", name = "enabled", havingValue = "true")
public class VirtualThreadAsyncConfig {

    @Bean
    public AsyncTaskExecutor applicationTaskExecutor() {
        return new TaskExecutorAdapter(Executors.newVirtualThreadPerTaskExecutor());
    }
}
```

Bước 3: Phòng chống cạm bẫy Thread Pinning
Trong mã nguồn ứng dụng:
- Thay thế các khối synchronized bao bọc các thao tác gọi I/O (Database, REST, File) bằng java.util.concurrent.locks.ReentrantLock.
- Tuyệt đối không dùng ThreadLocal để lưu trữ các buffer dữ liệu dung lượng lớn vì hàng trăm ngàn Virtual Threads có thể gây OutOfMemoryError.

Bước 4: Kiểm chứng kết quả vận hành
Khởi động ứng dụng và kiểm tra log console:
- Tomcat worker threads sẽ có tiền tố định danh dạng: `[tomcat-handler-X] ...` chạy dưới dạng Carrier threads.
- In ra thông tin thread trong controller:
  `Thread.currentThread().isVirtual()` trả về true.

Bước 5: Xử lý sự cố thường gặp
- Lỗi "Virtual threads are not supported": Đảm bảo JVM target version trong pom.xml / build.gradle là 21, và cờ --enable-preview không còn cần thiết trên Java 21 GA.
- Kiểm tra Thread Pinning bằng cờ JVM: `-Djdk.tracePinnedThreads=short` hoặc `-Djdk.tracePinnedThreads=full`.

---

## 4. Verification (Kiểm Chứng Kết Quả)

- Kiểm tra trạng thái dịch vụ hoặc thực thi lệnh xác nhận kết quả.
- Đảm bảo các chỉ số hoạt động ổn định và không phát sinh lỗi bất thường.

---

## 5. Troubleshooting (Xử Lý Sự Cố Thường Gặp)

- Nếu gặp lỗi kết nối hoặc quyền hạn, kiểm tra lại cấu hình mạng và thông số môi trường.

---

## 6. References (Tài Liệu Tham Khảo)

- Tham chiếu tài liệu chính thức của Spring Boot.
