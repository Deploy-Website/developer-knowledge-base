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

---

## 1. Mục Tiêu Dự Án

- **Tri thức chuẩn xác (Verified Knowledge)**: Kiến thức được tổng hợp và kiểm chứng trực tiếp từ tài liệu chính thống (Official Documentation) và sách kỹ thuật kinh điển.
- **Song ngữ Kỹ thuật (Bilingual Format)**: Diễn đạt tư duy và cơ chế bằng tiếng Việt mạch lạc, giữ nguyên thuật ngữ kỹ thuật tiếng Anh quốc tế (*Query Planner, Virtual Threads, HikariCP, DynamoDB GSI, Outbox Pattern*).
- **Tách biệt Triệt để (Docs vs. Labs)**: Thư mục `docs/` chứa tài liệu đọc tĩnh; toàn bộ source code thực thi và Docker Compose được cô lập tại thư mục `labs/`.
- **Hỗ trợ Tự Động Hóa (AI-Agent Driven)**: Tích hợp sẵn bộ Antigravity Agent Skills và bộ quy tắc `AGENTS.md` phòng chống bịa đặt (Zero Hallucination).

---

## 2. Đánh Giá Kiến Trúc: Material for MkDocs vs. Zensical

Trong quá trình khởi tạo dự án, hai giải pháp giao diện đã được phân tích và đánh giá kỹ lưỡng:

| Tiêu chí | Material for MkDocs (`mkdocs-material`) | Zensical (`zensical`) |
| :--- | :--- | :--- |
| **Mức độ Trưởng thành** | **Vững chắc (v9.5+)**: Được kiểm chứng trên hàng trăm ngàn dự án sản xuất lớn. | **Sơ khai (Pre-1.0 / v0.0.70)**: Dự án kế nhiệm đang trong giai đoạn phát triển tích cực. |
| **Hệ sinh thái Plugin** | Tương thích hoàn toàn với toàn bộ plugin MkDocs hiện hành. | Nhiều plugin bên thứ ba cần cơ chế tương thích riêng. |
| **Chế độ Build Nghiêm ngặt** | Hỗ trợ tuyệt đối cờ `mkdocs build --strict` (0 broken links, 0 warnings). | Đang tiếp tục hoàn thiện toolchain CLI. |
| **Quyết định** | **ĐƯỢC CHỌN (SELECTED)** làm nền tảng chính thức hiện tại. | Tiếp tục theo dõi để chuyển đổi (migrate) trong tương lai. |

Chi tiết đánh giá được công bố tại: [Kiến Trúc & Theme Evaluation](docs/standards/theme-evaluation.md).

---

## 3. Cấu Trúc Repository

```text
developer-knowledge-base/
├── .agents/
│   └── skills/                         # Antigravity Agent Skills
│       ├── research-topic/SKILL.md     # Kỹ năng nghiên cứu sâu chủ đề
│       ├── summarize-book/SKILL.md     # Kỹ năng tóm tắt sách kỹ thuật
│       ├── create-hands-on-lab/SKILL.md# Kỹ năng thiết kế lab Dockerized
│       └── review-knowledge/SKILL.md   # Kỹ năng rà soát & audit chất lượng
├── docs/                               # Toàn bộ tài liệu hiển thị trên Web (Markdown)
│   ├── index.md                        # Trang chủ Knowledge Base
│   ├── postgresql/                     # Trụ cột PostgreSQL & EXPLAIN ANALYZE
│   ├── java/                           # Trụ cột Modern Java 21+ & JVM Internals
│   ├── spring-boot/                    # Trụ cột Spring Boot 3.3+ & Hibernate Tuning
│   ├── aws/                            # Trụ cột AWS Cloud Architecture
│   ├── system-design/                  # Trụ cột System Design & Distributed Systems
│   ├── standards/                      # Quy chuẩn kỹ thuật & ADR đánh giá theme
│   └── templates/                      # Biểu mẫu hiển thị trên website
├── templates/                          # Biểu mẫu gốc dùng cho Agent & Contributor
│   ├── knowledge-note-template.md      # Biểu mẫu ghi chép kiến thức
│   ├── book-note-template.md           # Biểu mẫu tóm tắt sách
│   └── hands-on-lab-template.md        # Biểu mẫu hướng dẫn lab
├── labs/                               # Mã nguồn thực thi ĐỘC LẬP (Ngoại trừ docs/)
│   └── postgresql/
│       └── explain-analyze/            # Lab thực nghiệm PostgreSQL 1.000.000 dòng
├── AGENTS.md                           # Quy định tối thượng cho AI Agents
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
*(Lệnh trả về mã thoát `0` và sinh thư mục `site/`).*

---

## 5. Quy Trình Thêm Kiến Thức Mới

Khi tạo một tài liệu mới:
1. **Chọn Template**: Mở thư mục `templates/` và chọn biểu mẫu phù hợp:
   - `templates/knowledge-note-template.md`: Phân tích chủ đề kiến trúc / kỹ thuật.
   - `templates/book-note-template.md`: Tóm tắt sách và mô hình tư duy.
   - `templates/hands-on-lab-template.md`: Hướng dẫn thí nghiệm.
2. **Soạn thảo**: Lưu file vào đúng thư mục tương ứng trong `docs/<topic>/<ten-bai>.md`.
   - Đảm bảo tuân thủ nguyên tắc: Giải thích bằng tiếng Việt, giữ nguyên thuật ngữ tiếng Anh.
   - Đính kèm link tài liệu chính thức (`Official Documentation`).
3. **Cập nhật Mục Lục**: Thêm đường dẫn bài viết vào phần `nav` trong tệp `mkdocs.yml`.
4. **Xác nhận**: Chạy `python -m mkdocs build --strict` để kiểm tra toàn vẹn liên kết.

---

## 6. Hướng Dẫn Kích Hoạt Antigravity Agent Skills

Dự án tích hợp sẵn 4 Antigravity Agent Skills tại `.agents/skills/`. Bạn có thể yêu cầu AI Agent kích hoạt trực tiếp trong chat box bằng các câu lệnh tự nhiên:

### 1. `research-topic`
Sử dụng khi cần nghiên cứu chuyên sâu một chủ đề mới và tạo bài viết:
```text
Hãy sử dụng skill 'research-topic' để nghiên cứu cơ chế 'ZGC Generational Mode trong Java 21' 
và viết thành bài phân tích chi tiết vào docs/java/zgc-generational.md theo đúng template.
```

### 2. `summarize-book`
Sử dụng khi trích xuất kiến trúc và mô hình tư duy từ sách kỹ thuật:
```text
Hãy sử dụng skill 'summarize-book' để trích xuất Chương 5 (Replication) và Chương 7 (Transactions) 
từ cuốn sách 'Designing Data-Intensive Applications' và lưu vào docs/system-design/ddia-summary.md.
```

### 3. `create-hands-on-lab`
Sử dụng khi tạo một phòng thí nghiệm Dockerized độc lập:
```text
Hãy dùng skill 'create-hands-on-lab' để thiết kế lab 'HikariCP Connection Pool Exhaustion' 
trong labs/spring-boot/hikaricp-leak/ với Docker Compose và companion docs trong docs/spring-boot/.
```

### 4. `review-knowledge`
Sử dụng khi cần kiểm định chất lượng, rà soát link hỏng và chạy kiểm tra strict:
```text
Hãy dùng skill 'review-knowledge' để kiểm tra toàn bộ liên kết nội bộ, rà soát tính xác thực 
của các code sample và chạy mkdocs build --strict.
```

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
