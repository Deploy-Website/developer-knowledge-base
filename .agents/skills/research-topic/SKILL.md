---
name: research-topic
description: >-
  Researches a technical topic (PostgreSQL, Java, Spring Boot, AWS, or System Design) using official
  documentation, extracting deep architectural mechanisms, production trade-offs, and drafting a verified
  knowledge note in Vietnamese with English technical terms.
---

# Skill: Research Topic (research-topic)

Use this skill when you need to research a new software engineering concept or update an existing topic within the knowledge base.

## Workflow

### 1. Scope & Version Alignment
- Xác định phạm vi kỹ thuật cụ thể (Scope): Component, API, Internal mechanism hoặc Architecture pattern.
- Xác định phiên bản mục tiêu rõ ràng (ví dụ: PostgreSQL 16+, Java 21 LTS, Spring Boot 3.3+, AWS Architecture 2024+).
- Tránh nghiên cứu chung chung; tập trung vào cơ chế hoạt động bên dưới (under the hood) và bài toán thực tế.

### 2. Authoritative Source Retrieval
Chỉ sử dụng các nguồn chính thống có thẩm quyền cao:
- **Official Documentation**:
  - PostgreSQL: `https://www.postgresql.org/docs/current/`
  - OpenJDK / Oracle Java: `https://docs.oracle.com/en/java/javase/` & JEPs
  - Spring Framework / Spring Boot: `https://docs.spring.io/`
  - AWS Documentation: `https://docs.aws.amazon.com/`
- Không sử dụng các bài blog không rõ nguồn gốc, thông tin chưa được kiểm chứng, hoặc API đã deprecated.

### 3. Deep-Dive Extraction Checklist
Đảm bảo tài liệu trả lời được các câu hỏi kiến trúc sau:
1. **Bản chất (What & Why)**: Vấn đề nó giải quyết là gì? Tại sao giải pháp này ra đời?
2. **Cơ chế hoạt động (How it works under the hood)**: Luồng dữ liệu (data flow), bộ nhớ (memory buffers), thuật toán hoặc trạng thái chuyển tiếp (state machine).
3. **Trade-offs & Constraints**: Ưu/nhược điểm khi áp dụng là gì? Ảnh hưởng đến Latency, Throughput, Concurrency, hoặc Storage ra sao?
4. **Production Pitfalls**: Các lỗi thường gặp nhất trong môi trường Production (e.g., Connection pool exhaustion, JIT overhead, Index bloat, Out-of-Memory).

### 4. Drafting the Document
- Sử dụng template tại `templates/knowledge-note-template.md`.
- Ngôn ngữ: Giải thích bằng tiếng Việt mạch lạc, giữ nguyên thuật ngữ kỹ thuật tiếng Anh.
- Code blocks phải có cú pháp chỉ định ngôn ngữ rõ ràng (`sql`, `java`, `bash`, `yaml`) và chú thích dòng.
- Bổ sung sơ đồ Mermaid để trực quan hóa luồng dữ liệu hoặc kiến trúc.

### 5. Verification & Navigation Update
- Kiểm tra toàn bộ đường dẫn relative link.
- Cập nhật mục lục trong `mkdocs.yml` tương ứng với vị trí trang mới tạo.
- Chạy kiểm tra nghiêm ngặt:
  ```powershell
  python -m mkdocs build --strict
  ```
