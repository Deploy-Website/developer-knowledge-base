# Personal Developer Knowledge Base

[![MkDocs](https://img.shields.io/badge/docs-MkDocs%20Material-526CFE?style=flat&logo=materialformkdocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat)](LICENSE)

> Hệ thống lưu trữ, tra cứu và chắt lọc tri thức chuyên sâu dành cho Senior Software Architect & Backend/Cloud Engineers, tập trung vào 5 trụ cột: **PostgreSQL**, **Java**, **Spring Boot**, **AWS**, và **System Design**.

Deploy github page: python -m mkdocs gh-deploy --force

---

## 📑 Mục Lục

- [1. Mục Tiêu Dự Án](#1-mục-tiêu-dự-án)
- [2. Đánh Giá Kiến Trúc: Material for MkDocs vs. Zensical](#2-đánh-giá-kiến-trúc-material-for-mkdocs-vs-zensical)
- [3. Cấu Trúc Repository](#3-cấu-trúc-repository)
- [4. Cài Đặt & Chạy Môi Trường](#4-cài-đặt--chạy-môi-trường)
- [5. Quy Trình Thêm Kiến Thức Mới](#5-quy-trình-thêm-kiến-thức-mới)
  - [5.1. Lộ trình 1: Tiếp nhận nhanh qua Knowledge Inbox (Tự động hóa với AI Agent)](#51-lộ-trình-1-tiếp-nhận-nhanh-qua-knowledge-inbox-tự-động-hóa-với-ai-agent)
  - [5.2. Lộ trình 2: Tự thêm bài viết Markdown (.md) tùy chỉnh (Manual Contributor Workflow)](#52-lộ-trình-2-tự-thêm-bài-viết-markdown-md-tùy-chỉnh-manual-contributor-workflow)
    - [Bước 1: Khởi tạo file .md và cấu trúc bài viết chuẩn](#bước-1-khởi-tạo-file-md-và-cấu-trúc-bài-viết-chuẩn)
    - [Bước 2: Liên kết bài viết vào Menu điều hướng (mkdocs.yml)](#bước-2-liên-kết-bài-viết-vào-menu-điều-hướng-mkdocsyml)
    - [Bước 3: Tạo thêm Group / Phân mục Menu mới (Nested Navigation & Sections)](#bước-3-tạo-thêm-group--phân-mục-menu-mới-nested-navigation--sections)
    - [Bước 4: Kiểm tra và Khắc phục lỗi (Verification & Troubleshooting)](#bước-4-kiểm-tra-và-khắc-phục-lỗi-verification--troubleshooting)
- [6. Hướng Dẫn Kích Hoạt Antigravity Agent Skills](#6-hướng-dẫn-kích-hoạt-antigravity-agent-skills)
- [7. Thực Thi Thí Nghiệm Hands-on Labs](#7-thực-thi-thí-nghiệm-hands-on-labs)
- [8. Quy Chuẩn Kỹ Thuật (AGENTS.md)](#8-quy-chuẩn-kỹ-thuật-agentsmd)
- [9. Hướng Dẫn Sử Dụng Các Agent Skills](#9-hướng-dẫn-sử-dụng-các-agent-skills-detailed-skill-use-cases)

---

## 1. Mục Tiêu Dự Án

- **Tri thức chuẩn xác (Verified Knowledge)**: Kiến thức được tổng hợp và kiểm chứng trực tiếp từ tài liệu chính thống (Official Documentation) và sách kỹ thuật kinh điển.
- **Song ngữ Kỹ thuật (Bilingual Format)**: Diễn đạt tư duy và cơ chế bằng tiếng Việt mạch lạc, giữ nguyên thuật ngữ kỹ thuật tiếng Anh quốc tế (_Query Planner, Virtual Threads, HikariCP, DynamoDB GSI, Outbox Pattern_).
- **Tách biệt Triệt để (Docs vs. Labs)**: Thư mục `docs/` chứa tài liệu đọc tĩnh; toàn bộ source code thực thi và Docker Compose được cô lập tại thư mục `labs/`.
- **Hỗ trợ Tự Động Hóa (AI-Agent Driven)**: Tích hợp sẵn bộ Antigravity Agent Skills và bộ quy tắc `AGENTS.md` phòng chống bịa đặt (Zero Hallucination).

---

## 2. Đánh Giá Kiến Trúc: Material for MkDocs vs. Zensical

Trong quá trình khởi tạo dự án, hai giải pháp giao diện đã được phân tích và đánh giá kỹ lưỡng:

| Tiêu chí                     | Material for MkDocs (`mkdocs-material`)                                        | Zensical (`zensical`)                                                                     |
| :--------------------------- | :----------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------- |
| **Mức độ Trưởng thành**      | **Vững chắc (v9.5+)**: Được kiểm chứng trên hàng trăm ngàn dự án sản xuất lớn. | **Sơ khai (Pre-1.0 / v0.0.70)**: Dự án kế nhiệm đang trong giai đoạn phát triển tích cực. |
| **Hệ sinh thái Plugin**      | Tương thích hoàn toàn với toàn bộ plugin MkDocs hiện hành.                     | Nhiều plugin bên thứ ba cần cơ chế tương thích riêng.                                     |
| **Chế độ Build Nghiêm ngặt** | Hỗ trợ tuyệt đối cờ `mkdocs build --strict` (0 broken links, 0 warnings).      | Đang tiếp tục hoàn thiện toolchain CLI.                                                   |
| **Quyết định**               | **ĐƯỢC CHỌN (SELECTED)** làm nền tảng chính thức hiện tại.                     | Tiếp tục theo dõi để chuyển đổi (migrate) trong tương lai.                                |

Chi tiết đánh giá được công bố tại: [Kiến Trúc & Theme Evaluation](docs/standards/theme-evaluation.md).

---

## 3. Cấu Trúc Repository

```text
developer-knowledge-base/
├── .agents/
│   └── skills/                         # Bộ 9 Antigravity Agent Skills
│       ├── import-txt-notes/           # Kỹ năng nhập ghi chú TXT và tự động phân loại menu MkDocs
│       ├── manage-best-practices/      # Kỹ năng trích xuất, tổ chức & duy trì Best Practices theo domain
│       ├── document-investigation/     # Kỹ năng xử lý hồ sơ điều tra kỹ thuật nhiều bước
│       ├── capture-knowledge/SKILL.md  # Kỹ năng thu thập, triage & điều phối tri thức
│       ├── import-notebooklm/SKILL.md  # Kỹ năng tích hợp ghi chú từ NotebookLM
│       ├── research-topic/SKILL.md     # Kỹ năng nghiên cứu sâu chủ đề kỹ thuật
│       ├── summarize-book/SKILL.md     # Kỹ năng tóm tắt sách kiến trúc
│       ├── create-hands-on-lab/SKILL.md# Kỹ năng thiết kế lab Dockerized độc lập
│       └── review-knowledge/SKILL.md   # Kỹ năng rà soát, audit & strict build
├── inbox/                              # Vùng đệm tiếp nhận ghi chú thô, error logs, drafts
│   ├── investigations/                 # Staging hồ sơ điều tra thô (<id>/notes.md & attachments)
│   ├── samples/                        # Mẫu ghi chú thô thực tế (e.g., incident logs)
│   └── README.md                       # Hướng dẫn quy trình Knowledge Inbox
├── nodes/                              # Staging area chứa ghi chú TXT có cấu trúc (Item, Type, Domain)
│   ├── .import-manifest.json           # File manifest theo dõi trạng thái và hash chống trùng lặp
│   └── README.md                       # Hướng dẫn định dạng ghi chú TXT
├── docs/                               # Toàn bộ tài liệu hiển thị trên Web (Markdown)
│   ├── index.md                        # Trang chủ Knowledge Base
│   ├── postgresql/                     # Trụ cột PostgreSQL, EXPLAIN ANALYZE, Locks & Best Practices
│   │   ├── best-practices/             # Quy chuẩn sản xuất cho PostgreSQL (Query, Indexing, ...)
│   │   └── investigations/             # Các hồ sơ điều tra thực tế đã xuất bản
│   ├── java/                           # Trụ cột Modern Java 21+ & JVM Internals
│   │   └── best-practices/             # Quy chuẩn sản xuất cho Java (Exceptions, Concurrency, ...)
│   ├── spring-boot/                    # Trụ cột Spring Boot 3.3+ & Hibernate Tuning
│   │   └── best-practices/             # Quy chuẩn sản xuất cho Spring Boot (WebClient, HikariCP, ...)
│   ├── aws/                            # Trụ cột AWS Cloud Architecture
│   │   └── best-practices/             # Quy chuẩn sản xuất cho AWS (VPC, Aurora Export, ...)
│   ├── system-design/                  # Trụ cột System Design & Distributed Systems
│   │   └── best-practices/             # Quy chuẩn sản xuất cho System Design (Idempotency, Outbox, ...)
│   ├── standards/                      # Quy chuẩn kỹ thuật, ADR & Investigation Workflow
│   └── starter-templates/              # Biểu mẫu hiển thị tra cứu trên website
├── templates/                          # Biểu mẫu gốc dùng cho Agent & Contributor
│   ├── best-practice.md                # Biểu mẫu thực hành chuẩn mực theo lĩnh vực
│   ├── knowledge-note-template.md      # Biểu mẫu ghi chép kiến thức
│   ├── book-note-template.md           # Biểu mẫu tóm tắt sách
│   ├── troubleshooting-template.md     # Biểu mẫu xử lý sự cố & post-mortem
│   ├── how-to-template.md              # Biểu mẫu hướng dẫn tác vụ thực tế
│   ├── code-recipe-template.md         # Biểu mẫu snippet & SQL query recipe
│   ├── hands-on-lab-template.md        # Biểu mẫu hướng dẫn lab
│   ├── investigation-raw.md            # Biểu mẫu ghi chép thô cuộc điều tra
│   └── investigation-case.md           # Biểu mẫu xuất bản hồ sơ điều tra chuẩn
├── labs/                               # Mã nguồn thực thi ĐỘC LẬP (Ngoại trừ docs/)
│   └── postgresql/
│       └── explain-analyze/            # Lab thực nghiệm PostgreSQL 1.000.000 dòng
├── AGENTS.md                           # Quy định tối thượng cho AI Agents (Zero Hallucination)
├── mkdocs.yml                          # Cấu hình MkDocs & Material Theme
├── requirements.txt                    # Khai báo thư viện Python
└── README.md                           # Tài liệu tổng quan dự án (Tệp này)
```

---

## 4. Cài Đặt & Chạy Môi Trường

### 4.1. Yêu cầu Hệ thống

- Python 3.11+ (Hỗ trợ tốt trên Python 3.11, 3.12, 3.13).
- Git.

### 4.2. Cài đặt Dependencies

```bash
# Tạo môi trường ảo (Khuyến nghị)
python -m venv .venv

# Kích hoạt trên Windows PowerShell:
.venv\Scripts\Activate.ps1
# Hoặc trên Linux/macOS:
# source .venv/bin/activate

# Cài đặt thư viện:
pip install -r requirements.txt
```

### 4.3. Chạy Local Development Server

```bash
python -m mkdocs serve
```

Mở trình duyệt tại: **`http://127.0.0.1:8000`**

Giao diện hỗ trợ:

- **Instant Search**: Tìm kiếm tức thì với gợi ý và highlight từ khóa.
- **Light/Dark Mode**: Nút chuyển đổi giao diện mặt trời / mặt trăng ở góc trên bên phải.
- **Copy Code Button**: Sao chép code blocks một chạm.
- **Code Annotation & Tabs**: Trình bày code đa ngôn ngữ và chú thích trực quan.

### 4.4. Kiểm Tra Build Nghiêm Ngặt (Strict Build)

Trước khi commit, luôn đảm bảo không có bất kỳ warning hoặc link hỏng nào:

```bash
python -m mkdocs build --strict
```

_(Lệnh trả về mã thoát `0` và sinh thư mục `site/`)._

---

## 5. Quy Trình Thêm Kiến Thức Mới

Hệ thống hỗ trợ 2 lộ trình ghi nhận tri thức linh hoạt tùy theo nhu cầu: sử dụng AI Agent tự động hóa hoặc tự biên soạn bài viết tùy chỉnh (custom) thủ công.

---

### 5.1. Lộ trình 1: Tiếp nhận nhanh qua Knowledge Inbox (Tự động hóa với AI Agent)

Dành cho trường hợp bạn có ghi chú thô, error logs, draft post-mortem hoặc trích xuất từ NotebookLM và muốn AI Agent xử lý tự động:

1. **Tạo file ghi chú thô**: Đặt file vào `inbox/` (ví dụ: `inbox/pg-timeout.md`) hoặc `nodes/` (file `.txt` có header metadata `Item`, `Type`, `Domain`, `Content`).
2. **Kích hoạt Agent Skill**:
   - Sử dụng **`capture-knowledge`** cho ghi chú thô tự do: AI sẽ tự động kiểm tra trùng lặp (Deduplication), chọn template chuẩn hóa, phân loại vào `docs/` hoặc `labs/`, và cập nhật menu navigation.
   - Sử dụng **`import-txt-notes`** cho các file trong `nodes/`: AI sẽ đọc metadata, sinh markdown chuẩn và cập nhật `mkdocs.yml`.

---

### 5.2. Lộ trình 2: Tự thêm bài viết Markdown (.md) tùy chỉnh (Manual Contributor Workflow)

Dành cho trường hợp bạn muốn tự tay biên soạn một bài viết hoàn chỉnh, thêm các phân mục mới hoặc cấu trúc lại menu hiển thị theo ý muốn.

#### Bước 1: Khởi tạo file `.md` và cấu trúc bài viết chuẩn

1. **Chọn thư mục lưu trữ trong `docs/`**:
   - Lưu đúng theo chuyên mục công nghệ tương ứng:
     - `docs/postgresql/`: Các bài viết chuyên sâu về PostgreSQL.
     - `docs/java/`: Các bài viết về Java 21+, JVM internals.
     - `docs/spring-boot/`: Spring Boot 3.3+, Spring Data, Cloud.
     - `docs/aws/`: Kiến trúc AWS Cloud, RDS, DynamoDB, S3.
     - `docs/system-design/`: Kiến trúc phân tán, Outbox, Caching, Sharding.
     - `docs/standards/`: Các quy chuẩn kỹ thuật hoặc bài viết hướng dẫn chung.
   - *Lưu ý*: Nếu bài viết là **Best Practice**, hãy lưu vào thư mục con `best-practices/` của domain đó (ví dụ: `docs/spring-boot/best-practices/resilient-webclient.md`).

2. **Quy ước đặt tên file**:
   - Luôn sử dụng chữ thường, ngăn cách bằng dấu gạch ngang (**kebab-case**).
   - Ví dụ: `hikaricp-connection-leak.md`, `virtual-thread-pitfalls.md`, `dynamodb-gsi-design.md`.

3. **Cấu trúc nội dung bài viết khuyến nghị**:
   Bạn có thể tham khảo các template có sẵn trong thư mục `templates/` hoặc viết tự do theo khung chuẩn sau:

   ```markdown
   # Tên Bài Viết Đầy Đủ (Title H1)

   > Tóm tắt 1-2 câu về vấn đề cốt lõi, giá trị thực tế và bối cảnh áp dụng.

   ## 1. Bối Cảnh & Vấn Đề (Context & Problem Statement)

   Phân tích nguyên nhân gốc rễ và triệu chứng sự cố...

   ## 2. Cơ Chế Hoạt Động (Under the Hood / Deep Dive)

   Giải thích chi tiết cơ chế hoạt động, có thể kèm sơ đồ Mermaid:

   ```mermaid
   flowchart TD
       A[Client Request] --> B[API Gateway]
       B --> C[Spring Boot App]
   ```

   ## 3. Giải Pháp Kỹ Thuật (Production Implementation)

   ```java
   // Code minh họa tuân thủ Java 21+ idioms
   public record PaymentOrder(UUID id, BigDecimal amount) {}
   ```

   !!! tip "Kinh nghiệm thực chiến (Production Tip)"
       Sử dụng Admonition (`tip`, `note`, `warning`, `caution`) để nhấn mạnh các lưu ý sống còn.

   ## 4. Tài Liệu Tham Khảo (Official References)

   - [PostgreSQL Official Documentation](https://www.postgresql.org/docs/)
   - [Spring Boot Reference](https://docs.spring.io/spring-boot/reference/)
   ```

4. **Nguyên tắc quản lý tài nguyên (Separation of Concerns)**:
   - **Hình ảnh / Diagram**: Đặt tại `docs/assets/images/` và dẫn link tương đối (ví dụ: `![Diagram](../assets/images/my-diagram.png)`).
   - **Source code thực thi & Lab test**: Nếu bài viết có kèm Docker Compose, SQL seed, test suite Java, hãy tạo thư mục riêng tại `labs/<topic>/<lab-name>/` (tuyệt đối không đưa source code dự án lớn hoặc binary vào `docs/`).

---

#### Bước 2: Liên kết bài viết vào Menu điều hướng (`mkdocs.yml`)

Mục lục hiển thị trên website được quản lý tập trung tại trường `nav:` trong tệp [mkdocs.yml](mkdocs.yml).

1. **Quy tắc đường dẫn**:
   - MkDocs tự động coi thư mục `docs/` là thư mục gốc (documentation root).
   - Vì vậy, đường dẫn trong `nav` **tuyệt đối KHÔNG có tiền tố `docs/`**.
   - *Đúng*: `spring-boot/hikaricp-tuning.md`
   - *Sai*: `docs/spring-boot/hikaricp-tuning.md`

2. **Cú pháp thêm bài viết vào menu**:
   Mở `mkdocs.yml`, tìm đến mục công nghệ tương ứng dưới `nav:`, và thêm một dòng theo cú pháp:

   ```yaml
   - "Tên hiển thị trên Menu": duong-dan-tu-docs/ten-file.md
   ```

   > [!TIP]
   > Luôn bọc tên hiển thị trong dấu ngoặc kép `"` (ví dụ: `"Deep Dive: EXPLAIN ANALYZE"`) để tránh lỗi cú pháp YAML khi tiêu đề chứa ký tự đặc biệt như dấu hai chấm (`:`), gạch ngang (`-`), hoặc ký tự và (`&`).

3. **Ví dụ cụ thể**:
   Giả sử bạn vừa tạo file `docs/spring-boot/hikaricp-tuning.md`. Hãy mở `mkdocs.yml` và thêm vào mục `Spring Boot`:

   ```yaml
   nav:
     - Trang chủ: index.md
     - Spring Boot:
         - Tổng quan & Roadmap: spring-boot/index.md
         - Best Practices:
             - Tổng quan: spring-boot/best-practices/index.md
             - "Cấu hình WebClient Kháng lỗi": spring-boot/best-practices/resilient-webclient.md
         # Thêm bài viết mới vào đây:
         - "Tối ưu hóa HikariCP Connection Pool": spring-boot/hikaricp-tuning.md
   ```

---

#### Bước 3: Tạo thêm Group / Phân mục Menu mới (Nested Navigation & Sections)

Khi số lượng bài viết nhiều lên, bạn cần tạo thêm các **Group** (Nhóm bài viết) để menu gọn gàng, có tính phân cấp và chuyên nghiệp.

1. **Hiểu về cấp bậc điều hướng trong Material for MkDocs**:
   Repository đã bật sẵn các tính năng giao diện cao cấp:
   - `navigation.tabs`: Mục cấp cao nhất (Level 1) sẽ trở thành **Tab ngang** ở thanh Header.
   - `navigation.sections`: Các Group con (Level 2) bên trong Tab sẽ hiển thị thành các **khối section** trong sidebar bên trái.
   - `navigation.expand`: Tự động mở rộng cây thư mục để người đọc dễ tra cứu.
   - `navigation.indexes`: Cho phép gán trực tiếp một trang tài liệu làm trang index đại diện cho cả một Group.

2. **Cách tạo thêm Group mới bên trong một Tab đã có**:
   Để tạo một Group con, bạn chỉ cần tạo một nhãn group có thụt đầu dòng (indentation chuẩn YAML với khoảng trắng), theo sau là danh sách các bài viết con:

   ```yaml
   nav:
     - Spring Boot:                         # Tab cấp 1 (Header tab)
         - Tổng quan & Roadmap: spring-boot/index.md
         - Best Practices:                  # Group cấp 2 (Có sẵn)
             - Tổng quan: spring-boot/best-practices/index.md
             - "Cấu hình WebClient Kháng lỗi": spring-boot/best-practices/resilient-webclient.md
         - How-to:                          # Group cấp 2 (Có sẵn)
             - "Cấu Hình Virtual Threads": spring-boot/how-to/cau-hinh-virtual-threads-cho-spring-boot-33.md
         
         # ==========================================================
         # TẠO THÊM GROUP MỚI: Performance Tuning
         # ==========================================================
         - Performance Tuning:              # Tên Group hiển thị ở Sidebar
             - "Tối ưu hóa HikariCP": spring-boot/performance/hikaricp-tuning.md
             - "Chiến lược Caching Redis": spring-boot/performance/redis-caching.md
             - "Tối ưu Batch Processing": spring-boot/performance/batch-processing.md
   ```

3. **Cách tạo Sub-group lồng sâu hơn (Level 3)**:
   Nếu trong một Group lại cần phân nhánh nhỏ hơn, bạn chỉ cần tiếp tục thụt lề thêm một cấp:

   ```yaml
         - Advanced Architecture:           # Group cấp 2
             - Event-Driven Architecture:   # Sub-group cấp 3
                 - "Outbox Pattern với Debezium": spring-boot/architecture/eda/outbox-pattern.md
                 - "Idempotent Consumer": spring-boot/architecture/eda/idempotent-consumer.md
             - Security & Auth:             # Sub-group cấp 3
                 - "OAuth2 & JWT Hardening": spring-boot/architecture/security/jwt-hardening.md
   ```

4. **Cách tạo một Trụ Cột / Tab cấp cao mới (Top-level Tab)**:
   Nếu bạn muốn mở thêm một chuyên mục công nghệ hoàn toàn mới (ví dụ: `Kubernetes` hoặc `Kafka`), hãy khai báo ngang hàng với `PostgreSQL`, `Java`, `Spring Boot`:

   ```yaml
   nav:
     - Trang chủ: index.md
     - PostgreSQL:
         # ...
     - Spring Boot:
         # ...
     # ==========================================================
     # TẠO TAB MỚI TRÊN THANH HEADER:
     # ==========================================================
     - Kubernetes:
         - Tổng quan: k8s/index.md
         - Best Practices:
             - "Cấu hình Pod Resource Limits": k8s/best-practices/pod-limits.md
             - "Health Checks Liveness & Readiness": k8s/best-practices/health-checks.md
         - Troubleshooting:
             - "Xử lý OOMKilled & CrashLoopBackOff": k8s/troubleshooting/oomkilled.md
   ```

5. **Gán trang Index đại diện cho Group (`navigation.indexes`)**:
   Khi một Group có một bài viết tổng quan đại diện (thường đặt tên là `index.md`), bạn có thể cấu hình để khi người dùng nhấn vào tiêu đề của Group thì website sẽ mở ngay trang đó:

   ```yaml
         - Performance Tuning:
             - spring-boot/performance/index.md   # File này đóng vai trò trang chủ của group
             - "Tối ưu hóa HikariCP": spring-boot/performance/hikaricp-tuning.md
   ```

---

#### Bước 4: Kiểm tra và Khắc phục lỗi (Verification & Troubleshooting)

Sau khi tạo bài viết và cấu hình menu, bắt buộc thực hiện kiểm tra 2 bước:

1. **Khởi chạy Local Dev Server (Kiểm tra trực quan)**:
   ```bash
   python -m mkdocs serve
   ```
   - Truy cập **`http://127.0.0.1:8000`**.
   - Kiểm tra xem bài viết mới có xuất hiện đúng vị trí trong thanh menu không, click vào xem nội dung, thử chuyển đổi giao diện Sáng / Tối (Light/Dark mode) và kiểm tra hiển thị trên mobile.

2. **Chạy Strict Build (Bắt buộc theo chuẩn AGENTS.md)**:
   ```bash
   python -m mkdocs build --strict
   ```
   Lệnh phải trả về mã thoát **`0`** (exit code 0) và không có bất kỳ dòng `WARNING` hay `ERROR` nào.

3. **Bảng tra cứu các lỗi thường gặp**:

   | Triệu chứng lỗi | Nguyên nhân | Cách khắc phục |
   | :--- | :--- | :--- |
   | `yaml.parser.ParserError: mapping values are not allowed here` | Tiêu đề chứa dấu hai chấm (`:`) mà không bọc trong ngoặc kép `"` | Bọc toàn bộ tiêu đề trong dấu nháy kép, ví dụ: `"Deep Dive: Memory Management"` |
   | `yaml.scanner.ScannerError: found character '\t' that cannot start any token` | Dùng phím `Tab` thay vì phím `Space` khi thụt lề trong `mkdocs.yml` | Thay thế toàn bộ ký tự Tab bằng 2 hoặc 4 dấu khoảng trắng (spaces) |
   | `Doc file '...' contains a broken relative link to '...'` | Link trỏ tới file `.md` không tồn tại hoặc sai đường dẫn tương đối | Kiểm tra lại đường dẫn tương đối tính từ file hiện tại đến file đích |
   | `A file is listed in 'nav' but does not exist on disk` | Gõ sai tên file, hoặc vô tình thêm tiền tố `docs/` vào đường dẫn trong `nav` | Xóa tiền tố `docs/`, kiểm tra chính xác đường dẫn từ thư mục `docs/` |

---

## 6. Hướng Dẫn Kích Hoạt Antigravity Agent Skills

Dự án tích hợp sẵn **bộ 9 Antigravity Agent Skills** tại `.agents/skills/`. Bạn có thể yêu cầu AI Agent kích hoạt trực tiếp trong chat box:

| Kỹ năng (Skill)              | Mục đích & Ngữ cảnh sử dụng                                                                                                   | Lệnh mẫu kích hoạt                                                                                                  |
| :--------------------------- | :---------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------ |
| **`import-txt-notes`**       | Nhập ghi chú TXT từ `nodes/`, tự động chuyển đổi Markdown và phân loại menu MkDocs theo Domain & Type.                        | _"Nhập toàn bộ ghi chú từ thư mục nodes/ bằng skill import-txt-notes."_                                             |
| **`manage-best-practices`**  | Trích xuất, chuẩn hóa và duy trì Best Practices theo domain với 4 cấp độ bằng chứng (Official, Verified, Context, Candidate). | _"Trích xuất bài học tối ưu JSONB từ hồ sơ điều tra inv-001 thành Best Practice bằng skill manage-best-practices."_ |
| **`document-investigation`** | Xử lý hồ sơ điều tra kỹ thuật nhiều bước, bảo tồn tiến trình thời gian và cập nhật lũy tiến.                                  | _"Hãy xử lý hồ sơ điều tra tại inbox/investigations/inv-001/notes.md bằng skill document-investigation."_           |
| **`capture-knowledge`**      | Thu thập, phân loại ghi chú thô từ `inbox/`, kiểm tra trùng lặp, cross-linking.                                               | _"Hãy xử lý ghi chú tại inbox/sample-pg-lock-incident.md bằng skill capture-knowledge."_                            |
| **`import-notebooklm`**      | Tích hợp và kiểm chứng kỹ thuật các ghi chú nghiên cứu xuất từ NotebookLM.                                                    | _"Dùng import-notebooklm để đưa ghi chú NotebookLM vào mục PostgreSQL."_                                            |
| **`research-topic`**         | Nghiên cứu sâu chủ đề kỹ thuật đối chiếu official docs, RFCs và JEPs.                                                         | _"Nghiên cứu cơ chế Generational ZGC trong Java 21 bằng skill research-topic."_                                     |
| **`summarize-book`**         | Trích xuất mô hình tư duy, failure modes và production mapping từ sách.                                                       | _"Tóm tắt Chương 7 cuốn Designing Data-Intensive Applications bằng skill summarize-book."_                          |
| **`create-hands-on-lab`**    | Khởi tạo phòng thí nghiệm Docker Compose cô lập trong `labs/`.                                                                | _"Tạo lab đo lường HikariCP Pool Sizing bằng skill create-hands-on-lab."_                                           |
| **`review-knowledge`**       | Rà soát tính chính xác, phát hiện API lỗi thời và chạy `mkdocs build --strict`.                                               | _"Audit toàn bộ liên kết nội bộ và chạy build strict bằng skill review-knowledge."_                                 |

---

## 7. Thực Thi Thí Nghiệm Hands-on Labs

Tất cả các lab thực nghiệm đều được thiết kế độc lập, có thể tái lập trong môi trường Docker Container:

Ví dụ với **PostgreSQL EXPLAIN ANALYZE Lab**:

```bash
cd labs/postgresql/explain-analyze
docker compose up -d

# Thực thi toàn bộ 5 kịch bản benchmark trên 1.000.000 bản ghi:
docker compose exec postgres psql -U postgres -d knowledgedb -f /scripts/queries.sql

# Dọn dẹp sau khi kiểm thử xong:
docker compose down -v
```

Chi tiết hướng dẫn: Xem [labs/postgresql/explain-analyze/README.md](labs/postgresql/explain-analyze/README.md).

---

## 8. Quy Chuẩn Kỹ Thuật (AGENTS.md)

Mọi đóng góp vào repository này đều phải tuân thủ nghiêm ngặt [AGENTS.md](AGENTS.md):

- **Zero Hallucination**: Không bịa đặt số liệu benchmark hay method signatures.
- **Official Documentation Required**: Phải có liên kết đối chiếu từ tài liệu gốc.
- **Strict Separation**: Tuyệt đối không để mã nguồn thực thi hay file binary lớn trong thư mục `docs/`.
- **Security by Default**: Không để lộ secrets, passwords, hoặc API keys.
- **No Auto-Publishing**: Không tự động deploy ra môi trường production.

## 9. Hướng Dẫn Sử Dụng Các Agent Skills (Detailed Skill Use Cases)

Hệ thống cung cấp quy trình quản trị tri thức hợp nhất thông qua 9 Agent Skills chuyên biệt:

### 9.1. Use Case: `import-notebooklm`

Sử dụng khi bạn xuất các ghi chú tổng hợp hoặc tài liệu nghiên cứu từ Google NotebookLM để tích hợp vào MkDocs Knowledge Base.

**Câu lệnh mẫu:**

```text
Input:
inbox/notebooklm-ddia-transactions.md

Hãy dùng skill 'import-notebooklm' để tích hợp nội dung vào MkDocs.

Yêu cầu thực thi:
1. Phân tích các luận điểm chính về Transaction Isolation Levels.
2. Kiểm chứng kỹ thuật đối chiếu với PostgreSQL Official Documentation.
3. Kiểm tra kho tri thức hiện tại, tránh tạo nội dung trùng lặp.
4. Trích xuất thành Book Note và rút ra các cạm bẫy production (Write Skew, Phantom Reads).
5. Chạy mkdocs build --strict để đảm bảo không lỗi liên kết.
```

---

### 9.2. Use Case: `capture-knowledge` (Knowledge Inbox & Real-World Triage)

Sử dụng khi tiếp nhận thông tin thô từ thực chiến: ghi chú sự cố (Post-mortem), lỗi production timeout, câu query tuning, hoặc hướng dẫn cấu hình nhanh.

**Câu lệnh mẫu (Xử lý sự cố từ Inbox):**

```text
Input:
inbox/samples/sample-pg-lock-incident.md

Hãy dùng skill 'capture-knowledge' để xử lý ghi chú sự cố này:
1. Kiểm tra xem trong docs/ đã có bài viết nào về Lock Contention trong PostgreSQL chưa.
2. Nếu chưa, sử dụng 'templates/troubleshooting-template.md' để tạo docs/postgresql/troubleshooting-locks.md.
3. Trực quan hóa cơ chế Lock Queue FIFO bằng sơ đồ Mermaid.
4. Tạo liên kết chéo hai chiều với bài docs/postgresql/explain-analyze.md và docs/postgresql/index.md.
5. Cập nhật navigation trong mkdocs.yml và chạy mkdocs build --strict.
```

**Câu lệnh mẫu (Lưu trữ SQL Recipe tối ưu):**

```text
Tôi vừa viết một câu query giám sát connection state và active queries trong PostgreSQL:
[Dán SQL query vào đây]

Hãy dùng skill 'capture-knowledge' để chuẩn hóa thành Code Recipe theo template và lưu vào docs/postgresql/.
```

---

### 9.3. Use Case: `research-topic`

Sử dụng khi cần nghiên cứu chuyên sâu một chủ đề kỹ thuật nền tảng, cơ chế hoạt động bên dưới (Under the hood) đối chiếu từ Official Documentation.

**Câu lệnh mẫu:**

```text
Hãy sử dụng skill 'research-topic' để nghiên cứu chủ đề:
'Generational ZGC trong Java 21 LTS (JEP 439)'

Yêu cầu:
1. Tra cứu trực tiếp OpenJDK JEP 439 và Oracle Java 21 documentation.
2. Phân tích cơ chế Colored Pointers, Load Barriers và cấu trúc Young/Old generations.
3. So sánh trade-offs về throughput và latency với G1GC.
4. Soạn thảo bài viết theo 'templates/knowledge-note-template.md' lưu vào docs/java/zgc-generational.md.
5. Kiểm tra tính toàn vẹn liên kết bằng mkdocs build --strict.
```

---

### 9.4. Use Case: `summarize-book`

Sử dụng khi đúc kết kiến trúc và mô hình tư duy từ các cuốn sách kỹ thuật kinh điển.

**Câu lệnh mẫu:**

```text
Hãy sử dụng skill 'summarize-book' để trích xuất tinh hoa từ cuốn sách:
'Designing Data-Intensive Applications (Martin Kleppmann)' - Chương 5 (Replication)

Yêu cầu:
1. Trích xuất mô hình tư duy về Single-Leader, Multi-Leader, và Leaderless Replication.
2. Phân tích các Failure Modes: Replication Lag, Monotonic Reads, Read-After-Write Consistency.
3. Ánh xạ lý thuyết vào kiến trúc thực tế của PostgreSQL Streaming Replication và AWS DynamoDB.
4. Soạn thảo theo 'templates/book-note-template.md' lưu vào docs/system-design/ddia-replication.md.
```

---

### 9.5. Use Case: `create-hands-on-lab`

Sử dụng khi cần tạo một phòng thí nghiệm thực nghiệm độc lập với Docker Compose, seed data, và benchmark scripts.

**Câu lệnh mẫu:**

```text
Hãy sử dụng skill 'create-hands-on-lab' để thiết kế lab:
'HikariCP Connection Pool Tuning & Leak Detection'

Yêu cầu:
1. Đặt toàn bộ mã nguồn thực thi cô lập trong 'labs/spring-boot/hikaricp-tuning/' (Tuyệt đối không để source code trong docs/).
2. Tạo docker-compose.yml khởi chạy PostgreSQL và Spring Boot service với cấu hình leak-detection-threshold.
3. Viết script k6 hoặc curl mô phỏng tình trạng rò rỉ connection.
4. Viết README.md hướng dẫn từng bước tái lập sự cố và cách fix.
5. Tạo trang hướng dẫn tóm tắt trong docs/spring-boot/ và dẫn link tương đối sang labs/.
```

---

### 9.6. Use Case: `review-knowledge`

Sử dụng khi kiểm định chất lượng, rà soát link hỏng, phát hiện deprecated APIs hoặc kiểm tra strict build định kỳ.

**Câu lệnh mẫu:**

```text
Hãy kích hoạt skill 'review-knowledge' để audit toàn bộ kho lưu trữ:
1. Quét toàn bộ relative links trong docs/ đảm bảo không có link chết (dead links).
2. Kiểm tra xem có cấu hình hoặc API nào đã bị deprecated trên phiên bản hiện hành không.
3. Xác minh tính cô lập của thư mục labs/ (không có binary hay docker-compose trong docs/).
4. Chạy 'python -m mkdocs build --strict' và báo cáo chi tiết trạng thái.
```

---

### 9.7. Use Case: `document-investigation` (Engineering Investigation Management)

Sử dụng khi xử lý các cuộc điều tra kỹ thuật nhiều bước, các bài toán gỡ lỗi phức tạp kéo dài nhiều ngày, bảo tồn toàn bộ các thử nghiệm thất bại và cập nhật lũy tiến khi có bằng chứng mới.

> [!NOTE]
> _Lưu ý_: Các ví dụ dưới đây là **mô phỏng minh họa quy trình (Demonstrations)**, không phải số liệu đo đạc thực tế trên hệ thống sản xuất thật của bạn.

#### Ví Dụ 1 — PostgreSQL Query Optimization (Điều Tra Tối Ưu Truy Vấn Đa Kế Hoạch)

```text
Input:
inbox/investigations/inv-202610-pg-jsonb-tuning/notes.md

Hãy dùng skill 'document-investigation' để tổng hợp hồ sơ điều tra này:
1. Tái lập tiến trình 3 bước: B-Tree expression index (thất bại), GIN jsonb_ops (bloat 1.28GB), và GIN jsonb_path_ops + LZ4 compression (thành công).
2. Trích xuất bảng so sánh 4 chỉ số: P99 Latency, Dynamic Filtering, Index Size, và Insert Throughput.
3. Tạo liên kết chéo với docs/postgresql/explain-analyze.md và docs/postgresql/index.md.
4. Lưu bài viết vào docs/postgresql/investigations/inv-001-jsonb-tuning.md và chạy mkdocs build --strict.
```

#### Ví Dụ 2 — Spring Boot Troubleshooting (Điều Tra Lỗi Rollback & Connection Timeout)

```text
Input:
inbox/investigations/inv-202610-spring-tx-rollback/notes.md
Đính kèm: attachments/thread-dump.txt, attachments/application.yml

Hãy dùng skill 'document-investigation' để phân tích:
1. Bóc tách hiện tượng: Tại sao method có @Transactional gọi nội bộ (self-invocation) lại không được rollback khi gặp exception.
2. Ghi nhận thử nghiệm 1 thất bại khi cố gắng inject chính service đó (Circular dependency).
3. Ghi nhận thử nghiệm 2 thành công khi chuyển sang dùng TransactionTemplate.
4. Xuất bản hồ sơ vào docs/spring-boot/investigations/inv-001-self-invocation-rollback.md.
```

#### Ví Dụ 3 — AWS Infrastructure Investigation (Thử Nghiệm Chiến Lược Export Dữ Liệu Aurora)

```text
Input:
inbox/investigations/inv-202610-aws-aurora-export/notes.md

Hãy dùng skill 'document-investigation' để xây dựng case study:
1. Tái lập so sánh giữa: pg_dump thông thường qua EC2 (tốn CPU, network egress cao), AWS DMS task (phức tạp), và aws_s3.query_export_to_s3() tích hợp sẵn của Aurora.
2. Ghi nhận chi tiết các lệnh SQL, quyền IAM policy và thời gian export đo được trên dataset 100GB.
3. Rút ra khuyến nghị kiến trúc cho đội ngũ DevOps.
4. Xuất bản vào docs/aws/investigations/inv-001-aurora-s3-export.md.
```

#### Ví Dụ 4 — Updating an Existing Investigation (Cập Nhật Lũy Tiến Cho Điều Tra Đang Diễn Ra)

```text
Hồ sơ hiện có: docs/postgresql/investigations/inv-001-jsonb-tuning.md
Dữ liệu mới bổ sung: inbox/investigations/inv-202610-pg-jsonb-tuning/notes.md (Mục "Bước 4: Kiểm tra hành vi Autovacuum trên GIN index")

Hãy dùng skill 'document-investigation' để cập nhật lũy tiến:
1. Đọc trạng thái hiện tại của hồ sơ đã xuất bản.
2. Nối tiếp Bước 4 vào Chronological Timeline, ghi nhận các quan sát mới về pg_stat_user_indexes.
3. Cập nhật bảng chỉ số tổng hợp tại phần Quick Reference.
4. Giữ nguyên toàn bộ lịch sử Thí nghiệm 1, 2, 3 và kiểm tra strict build.
```

---

### 9.7. Use Case: `manage-best-practices`

Sử dụng khi bạn cần trích xuất, tổ chức, hoặc cập nhật các quy chuẩn sản xuất (**Best Practices**) cho từng lĩnh vực công nghệ (`postgresql`, `java`, `spring-boot`, `aws`, `system-design`), phân định 4 cấp độ bằng chứng (`Official Guidance`, `Verified Experiment`, `Context-specific Finding`, `Candidate`) và phân tích chuyên sâu _Why It Works_ cùng _When NOT to Use_.

#### Ví Dụ 1 — PostgreSQL: Trích xuất bài học tối ưu truy vấn từ hồ sơ điều tra

```text
Hồ sơ điều tra nguồn: docs/postgresql/investigations/inv-001-jsonb-tuning.md

Hãy dùng skill 'manage-best-practices' để tổng hợp thành Best Practice:
1. Đọc kết quả xác minh từ hồ sơ điều tra INV-001.
2. Tạo trang: docs/postgresql/best-practices/jsonb-query-optimization.md.
3. Làm nổi bật phương pháp: GIN jsonb_path_ops kết hợp nén LZ4 TOAST cho PostgreSQL 14+, toán tử @>.
4. Gán Evidence Level: Verified Experiment (nhanh gấp 50 lần, index giảm 83%).
5. Thiết lập liên kết chéo hai chiều với inv-001-jsonb-tuning.md và docs/postgresql/best-practices/index.md.
```

#### Ví Dụ 2 — Modern Java: Xây dựng quy chuẩn xử lý ngoại lệ chuẩn mực

```text
Chủ đề: Robust Exception Handling trong Modern Java 21+

Hãy dùng skill 'manage-best-practices' để biên soạn quy chuẩn:
1. Tạo trang: docs/java/best-practices/exception-handling.md.
2. Quy chuẩn hóa: Bảo toàn root cause qua Chained Exceptions, BaseDomainException mang ngữ cảnh, Sealed Exceptions, và quản lý ngoại lệ trong Virtual Threads.
3. Gán Evidence Level: Official Guidance (Oracle JLS & Effective Java).
4. Cập nhật docs/java/best-practices/index.md và mkdocs.yml.
```

#### Ví Dụ 3 — Spring Boot: Cấu hình WebClient chống sụp đổ dây chuyền

```text
Chủ đề: Resilient WebClient Configuration trong Spring Boot 3.3+

Hãy dùng skill 'manage-best-practices' để xây dựng quy chuẩn:
1. Tạo trang: docs/spring-boot/best-practices/resilient-webclient.md.
2. Bao gồm: 4 tầng timeout (Connect, Response, Read Idle, Write Idle) với Reactor Netty, ConnectionProvider pool sizing, và Retry có Exponential Backoff kèm Jitter.
3. Chỉ rõ chống chỉ định: Không dùng .block() trên Reactor EventLoop threads.
4. Gán Evidence Level: Official Guidance (Spring & Reactor Netty Docs).
5. Cập nhật navigation và kiểm tra strict build.
```

#### Ví Dụ 4 — AWS: Chuyển đổi thử nghiệm trích xuất dữ liệu Aurora sang Best Practice

```text
Thử nghiệm nguồn: Trích xuất dữ liệu lớn từ Amazon Aurora PostgreSQL sang Amazon S3

Hãy dùng skill 'manage-best-practices' để chuẩn hóa kiến trúc:
1. Tạo trang: docs/aws/best-practices/aurora-s3-export.md.
2. So sánh và tối ưu: aws_s3.query_export_to_s3() kết hợp S3 Gateway VPC Endpoint và IAM Role, loại bỏ máy trung gian EC2 và phí NAT Gateway.
3. Gán Evidence Level: Context-specific Finding (tối ưu cho dataset > 50GB khi có VPC Gateway Endpoint).
4. Cập nhật docs/aws/best-practices/index.md và mkdocs.yml.
```

#### Ví Dụ 5 — Updating an Existing Best Practice (Cập Nhật Lũy Tiến Cho Best Practice Hiện Có)

```text
Bài viết hiện có: docs/postgresql/best-practices/jsonb-query-optimization.md
Dữ liệu cập nhật: Tối ưu hóa bộ nhớ cho GIN VACUUM trong PostgreSQL 17 và tham số gin_pending_list_limit

Hãy dùng skill 'manage-best-practices' để cập nhật:
1. Mở bài viết hiện có, bổ sung mục Version Evolution cho PostgreSQL 16 & 17.
2. Giữ nguyên toàn bộ kết luận đã được kiểm chứng của PostgreSQL 16, không ghi đè lịch sử.
3. Bổ sung khuyến nghị điều chỉnh gin_pending_list_limit = '32MB' cho hệ thống có tốc độ ghi cao.
4. Chạy python -m mkdocs build --strict để xác nhận không có lỗi liên kết.
```

---

### 9.8. Use Case: `import-txt-notes`

Sử dụng khi bạn ghi chép các ghi chú kỹ thuật thô dưới dạng file text `.txt` trong thư mục `nodes/` và muốn tự động chuyển đổi thành tài liệu Markdown chuẩn mực, tích hợp vào đúng menu navigation theo **Domain** và **Type**.

#### Định Dạng Header Bắt Buộc Trong File TXT

```text
Item: <Tiêu đề tài liệu>
Type: <Best Practice | Concept | How-to | Investigation | Troubleshooting | Lab | Recipe>
Domain: <PostgreSQL | Java | Spring Boot | AWS | System Design>

Content:
<Nội dung ghi chú...>
```

#### Ví Dụ 1 — Import Một File Đơn Lẻ (Single File)

```text
Hãy dùng skill 'import-txt-notes' để import file nodes/postgresql-index-deduplication.txt:
1. Đọc và xác thực metadata (Item, Type, Domain).
2. Tạo file docs/postgresql/best-practices/postgresql-b-tree-index-deduplication.md.
3. Cập nhật navigation trong mkdocs.yml dưới PostgreSQL -> Best Practices.
4. Ghi nhận manifest và chạy mkdocs build --strict.
```

#### Ví Dụ 2 — Import Hàng Loạt Toàn Bộ Thư Mục (Batch Mode)

```text
Hãy dùng skill 'import-txt-notes' ở chế độ batch:
1. Quét toàn bộ file .txt trong thư mục nodes/.
2. Bỏ qua các file đã import không có thay đổi (idempotent).
3. Báo cáo bảng tổng kết (Imported, Skipped, Conflicts, Failed).
4. Xác thực toàn bộ website với mkdocs build --strict.
```

#### Ví dụ 3 - Note simple

Using skill 'import-txt-notes' import file: nodes/postgresql-export-import-data.txt

Read Item, Type, Domain and Content.
Convert the note into structured Markdown, use Item as the menu label, place it under the Type category of the corresponding technology domain, update MkDocs navigation and run mkdocs build --strict.
Preserve the original TXT
