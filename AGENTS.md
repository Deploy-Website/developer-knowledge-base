# Engineering Rules & Agent Governance (AGENTS.md)

Welcome to the **Developer Knowledge Base** repository. This document serves as the supreme rulebook and engineering protocol for all AI Agents (including Antigravity, Gemini, and human contributors) interacting with this knowledge base.

---

## 1. Core Operating Principles

### 1.1. Zero-Hallucination Policy (Chính sách không bịa đặt thông tin)
- **Tuyệt đối không bịa đặt (Never invent)**: Không tự tạo ra các benchmark results, API signatures, tham số cấu hình, hoặc trích dẫn sách/bài báo không tồn tại.
- **Xác thực phiên bản (Version-specific verification)**: Mọi kiến thức phải được gắn với phiên bản cụ thể (ví dụ: PostgreSQL 16+, Java 21 LTS, Spring Boot 3.3+, AWS Current Architecture).
- **Cảnh báo giới hạn**: Nếu một cơ chế chưa được tài liệu chính thức xác nhận hoặc phụ thuộc vào platform-specific behavior, phải ghi chú rõ ràng (ví dụ: `Implementation-dependent`, `Heuristic optimizer choice`).

### 1.2. Official Source Verification (Nguyên tắc kiểm chứng nguồn)
Mọi kiến thức được đưa vào kho lưu trữ phải đối chiếu từ các nguồn có thẩm quyền cao nhất:
1. **Official Documentation**:
   - PostgreSQL: [postgresql.org/docs](https://www.postgresql.org/docs/)
   - Java: [docs.oracle.com/en/java](https://docs.oracle.com/en/java/) & OpenJDK JEPs
   - Spring: [docs.spring.io/spring-boot/reference](https://docs.spring.io/spring-boot/reference/)
   - AWS: [docs.aws.amazon.com](https://docs.aws.amazon.com/) & AWS Well-Architected Framework
2. **Kinh điển kỹ thuật (Classic Engineering Books)**:
   - *Designing Data-Intensive Applications* (Martin Kleppmann)
   - *Database Internals* (Alex Petrov)
   - *Effective Java* (Joshua Bloch)
   - *Java Concurrency in Practice* (Brian Goetz)
   - *Building Microservices* (Sam Newman)
3. **Thực chiến Production**: Phản ánh các bài học vận hành thực tế (failure modes, performance degradation, trade-offs), không chỉ lý thuyết suông.

---

## 2. Language & Writing Guidelines (Quy tắc ngôn ngữ)

- **Ngôn ngữ chủ đạo**: Giải thích bằng **tiếng Việt mạch lạc**, giữ nguyên **thuật ngữ kỹ thuật tiếng Anh (English Technical Terms)**.
  - *Đúng*: "Query planner quyết định chuyển từ `Index Scan` sang `Seq Scan` khi selectivity vượt ngưỡng cost estimation."
  - *Sai*: "Bộ lập kế hoạch truy vấn quyết định chuyển từ quét chỉ mục sang quét tuần tự khi độ chọn lọc vượt ngưỡng ước lượng chi phí."
- **Phong cách hành văn**: Senior Architect tone — súc tích, trực diện, tập trung vào bản chất bên dưới (under the hood), phân tích ưu/nhược điểm (trade-offs), và các production pitfalls.

---

## 3. Repository Architecture & Separation of Concerns

```text
developer-knowledge-base/
├── .agents/skills/      # Antigravity Agent Skills (cheatsheets & workflows)
├── AGENTS.md            # Governing rules (this file)
├── inbox/               # Staging area for raw notes, logs, and drafts
├── docs/                # MkDocs Markdown documentation ONLY
│   ├── postgresql/      # Deep dives, how-tos, recipes & troubleshooting
│   ├── java/            # Deep dives & notes for Java
│   ├── spring-boot/     # Deep dives & notes for Spring Boot
│   ├── aws/             # Deep dives & notes for AWS
│   ├── system-design/   # Deep dives & notes for System Design
│   ├── standards/       # Architectural standards, workflows & evaluations
│   └── starter-templates/# Published markdown templates
├── templates/           # Raw templates for direct agent usage
├── labs/                # Executable hands-on code (SEPARATED FROM docs/)
│   └── <topic>/<lab>/   # Docker Compose, scripts, SQL, Java source code
├── mkdocs.yml           # MkDocs configuration
├── requirements.txt     # Python dependencies
└── README.md            # Repository overview & usage instructions
```

### 3.1. Tuyệt đối tách biệt Docs và Labs (Separation Rule)
- **Thư mục `docs/`**: CHỈ chứa các tệp Markdown (`.md`), hình ảnh sơ đồ (`.png`, `.svg`), hoặc diagrams (`mermaid`).
- **Thư mục `labs/`**: Chứa toàn bộ source code thực thi (Docker Compose, `init.sql`, bash scripts, Java test cases, JMeter/k6 scripts).
- **Tuyệt đối KHÔNG** để source code dự án lớn hoặc binary files bên trong `docs/`. Trong `docs/`, chỉ trích dẫn các code snippet quan trọng và dẫn link tương đối sang `labs/`.

### 3.2. Vùng Đệm Tiếp Nhận (Knowledge Inbox Rule)
- **Thư mục `inbox/`**: Là staging area tạm thời chứa ghi chú thô, error logs, draft post-mortems hoặc trích xuất từ NotebookLM.
- Khi tiếp nhận tài liệu từ `inbox/`, Agent phải kiểm tra trùng lặp (Deduplication), chọn template chuẩn hóa (`templates/`), chuyển đổi vào `docs/` hoặc `labs/`, và di chuyển hoặc dọn dẹp file thô.

### 3.3. Nguyên Tắc Chống Trùng Lặp & Liên Kết Chéo (Deduplication & Cross-Linking)
- Không tạo bài viết mới nếu chủ đề đó đã có trang chính trong `docs/`; hãy cập nhật và bổ sung trang hiện có.
- Bắt buộc tạo liên kết chéo hai chiều (bi-directional cross-link) giữa các bài viết lý thuyết nền tảng và bài viết thực chiến (Troubleshooting, Recipe, Lab).

---

## 4. Code & Security Standards (Tiêu chuẩn an toàn & chất lượng code)

1. **Bảo mật tuyệt đối (Security by Default)**:
   - Không commit mật khẩu, AWS Access Keys, Secret Keys, database connection strings thật vào Git.
   - Các cấu hình mẫu phải dùng biến môi trường (Environment Variables) hoặc placeholder an toàn (ví dụ: `${DB_PASSWORD:-postgres}`).
   - SQL queries mẫu phải dùng parameterized statements / prepared statements; không minh họa SQL injection nguy hiểm mà không có cảnh báo.
2. **Chất lượng mẫu code (Production-Ready Samples)**:
   - Code Java phải tuân thủ Java 21+ idioms: Records, Pattern Matching, Virtual Threads (nếu phù hợp), `try-with-resources`.
   - Spring Boot code phải dùng constructor injection, validation annotations, cấu hình pool timeout chuẩn xác.
   - Script SQL phải có chú thích về index usage, transaction isolation level, và tác động khóa (locking behavior).

---

## 5. Verification & Contribution Protocol (Quy trình xác minh & cập nhật)

Mỗi khi agent hoặc kỹ sư thêm/sửa tài liệu:
1. **Kiểm tra liên kết (Link Integrity)**: Tất cả link nội bộ phải tồn tại, cú pháp chuẩn MkDocs (`[Link](relative/path.md)`).
2. **Strict Build Validation**: Bắt buộc chạy lệnh sau và kiểm tra mã thoát = 0:
   ```bash
   python -m mkdocs build --strict
   ```
   Bất kỳ warning nào (broken link, missing document in nav, syntax error) đều bị coi là lỗi nghiêm trọng (blocking error).
3. **Không ghi đè bừa bãi**: Không xóa hoặc thay đổi cấu trúc nội dung đã có nếu không có lý do kiến trúc rõ ràng.
4. **Không tự động deploy**: Không chạy lệnh publish hoặc push production mà chưa có sự đồng ý của kỹ sư phụ trách.
