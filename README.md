# Personal Developer Knowledge Base

[![MkDocs](https://img.shields.io/badge/docs-MkDocs%20Material-526CFE?style=flat&logo=materialformkdocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat)](LICENSE)

> Hệ thống lưu trữ, tra cứu và chắt lọc tri thức chuyên sâu dành cho Senior Software Architect & Backend/Cloud Engineers, tập trung vào 5 trụ cột: **PostgreSQL**, **Java**, **Spring Boot**, **AWS**, và **System Design**.

---

## 📑 Mục Lục

- [1. Mục Tiêu Dự Án](#1-mục-tiêu-dự-án)
- [2. Đánh Giá Kiến Trúc: Material for MkDocs vs. Zensical](#2-đánh-giá-kiến-trúc-material-for-mkdocs-vs-zensical)
- [3. Cấu Trúc Repository](#3-cấu-trúc-repository)
- [4. Cài Đặt & Chạy Môi Trường](#4-cài-đặt--chạy-môi-trường)
- [5. Quy Trình Thêm Kiến Thức Mới](#5-quy-trình-thêm-kiến-thức-mới)
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
│   └── skills/                         # Bộ 6 Antigravity Agent Skills
│       ├── capture-knowledge/SKILL.md  # Kỹ năng thu thập, triage & điều phối tri thức
│       ├── import-notebooklm/SKILL.md  # Kỹ năng tích hợp ghi chú từ NotebookLM
│       ├── research-topic/SKILL.md     # Kỹ năng nghiên cứu sâu chủ đề kỹ thuật
│       ├── summarize-book/SKILL.md     # Kỹ năng tóm tắt sách kiến trúc
│       ├── create-hands-on-lab/SKILL.md# Kỹ năng thiết kế lab Dockerized độc lập
│       └── review-knowledge/SKILL.md   # Kỹ năng rà soát, audit & strict build
├── inbox/                              # Vùng đệm tiếp nhận ghi chú thô, error logs, drafts
│   ├── samples/                        # Mẫu ghi chú thô thực tế (e.g., incident logs)
│   └── README.md                       # Hướng dẫn quy trình Knowledge Inbox
├── docs/                               # Toàn bộ tài liệu hiển thị trên Web (Markdown)
│   ├── index.md                        # Trang chủ Knowledge Base
│   ├── postgresql/                     # Trụ cột PostgreSQL, EXPLAIN ANALYZE & Troubleshooting Locks
│   ├── java/                           # Trụ cột Modern Java 21+ & JVM Internals
│   ├── spring-boot/                    # Trụ cột Spring Boot 3.3+ & Hibernate Tuning
│   ├── aws/                            # Trụ cột AWS Cloud Architecture
│   ├── system-design/                  # Trụ cột System Design & Distributed Systems
│   ├── standards/                      # Quy chuẩn kỹ thuật, ADR & Unified Workflow
│   └── starter-templates/              # Biểu mẫu hiển thị tra cứu trên website
├── templates/                          # Biểu mẫu gốc dùng cho Agent & Contributor
│   ├── knowledge-note-template.md      # Biểu mẫu ghi chép kiến thức
│   ├── book-note-template.md           # Biểu mẫu tóm tắt sách
│   ├── troubleshooting-template.md     # Biểu mẫu xử lý sự cố & post-mortem
│   ├── how-to-template.md              # Biểu mẫu hướng dẫn tác vụ thực tế
│   ├── code-recipe-template.md         # Biểu mẫu snippet & SQL query recipe
│   └── hands-on-lab-template.md        # Biểu mẫu hướng dẫn lab
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

Hệ thống hỗ trợ 2 lộ trình ghi nhận tri thức linh hoạt:

### Lộ trình 1: Tiếp nhận nhanh qua Knowledge Inbox (Khuyến nghị cho công việc thực tế)
1. Tạo file ghi chú thô trong `inbox/` (ví dụ: `inbox/pg-timeout.md`) chứa log lỗi, câu query, hoặc ý tưởng thô.
2. Yêu cầu AI Agent kích hoạt skill **`capture-knowledge`** để tự động kiểm tra trùng lặp, chọn template chuẩn hóa và phân loại vào `docs/` hoặc `labs/`.

### Lộ trình 2: Tự biên soạn bài bản qua Templates
1. **Chọn Template**: Mở thư mục `templates/` hoặc xem tại `docs/starter-templates/`:
   - `knowledge-note-template.md`: Phân tích chuyên sâu cơ chế kiến trúc.
   - `book-note-template.md`: Chắt lọc mô hình tư duy từ sách kinh điển.
   - `troubleshooting-template.md`: Phân tích sự cố, Root Cause Analysis & Post-mortem.
   - `how-to-template.md`: Hướng dẫn quy trình thao tác và cấu hình thực tế.
   - `code-recipe-template.md`: Tập hợp các đoạn code hoặc truy vấn SQL tối ưu.
   - `hands-on-lab-template.md`: Thí nghiệm đo lường hiệu năng và benchmark.
2. **Soạn thảo**: Lưu file vào đúng thư mục tương ứng trong `docs/<topic>/<ten-bai>.md`.
   - Tuân thủ nguyên tắc: Giải thích bằng tiếng Việt, giữ nguyên thuật ngữ tiếng Anh.
   - Đính kèm link tài liệu chính thức (`Official Documentation`).
3. **Cập nhật Mục Lục**: Thêm đường dẫn bài viết vào phần `nav` trong tệp `mkdocs.yml`.
4. **Xác nhận**: Chạy `python -m mkdocs build --strict` để kiểm tra toàn vẹn liên kết.

---

## 6. Hướng Dẫn Kích Hoạt Antigravity Agent Skills

Dự án tích hợp sẵn **bộ 6 Antigravity Agent Skills** tại `.agents/skills/`. Bạn có thể yêu cầu AI Agent kích hoạt trực tiếp trong chat box:

| Kỹ năng (Skill) | Mục đích & Ngữ cảnh sử dụng | Lệnh mẫu kích hoạt |
| :--- | :--- | :--- |
| **`capture-knowledge`** | Thu thập, phân loại ghi chú thô từ `inbox/`, kiểm tra trùng lặp, cross-linking. | *"Hãy xử lý ghi chú tại inbox/sample-pg-lock-incident.md bằng skill capture-knowledge."* |
| **`import-notebooklm`** | Tích hợp và kiểm chứng kỹ thuật các ghi chú nghiên cứu xuất từ NotebookLM. | *"Dùng import-notebooklm để đưa ghi chú NotebookLM vào mục PostgreSQL."* |
| **`research-topic`** | Nghiên cứu sâu chủ đề kỹ thuật đối chiếu official docs, RFCs và JEPs. | *"Nghiên cứu cơ chế Generational ZGC trong Java 21 bằng skill research-topic."* |
| **`summarize-book`** | Trích xuất mô hình tư duy, failure modes và production mapping từ sách. | *"Tóm tắt Chương 7 cuốn Designing Data-Intensive Applications bằng skill summarize-book."* |
| **`create-hands-on-lab`** | Khởi tạo phòng thí nghiệm Docker Compose cô lập trong `labs/`. | *"Tạo lab đo lường HikariCP Pool Sizing bằng skill create-hands-on-lab."* |
| **`review-knowledge`** | Rà soát tính chính xác, phát hiện API lỗi thời và chạy `mkdocs build --strict`. | *"Audit toàn bộ liên kết nội bộ và chạy build strict bằng skill review-knowledge."* |

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

Hệ thống cung cấp quy trình quản trị tri thức hợp nhất thông qua 6 Agent Skills chuyên biệt:

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
