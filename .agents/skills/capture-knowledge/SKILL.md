---
name: capture-knowledge
description: >-
  Ingests and structures raw technical knowledge from the inbox or real-world engineering work
  (troubleshooting incidents, practical how-tos, SQL/code recipes, concepts, labs), detecting duplicates,
  cross-linking related pages, and routing to specialized skills as needed.
---

# Skill: Capture Knowledge (capture-knowledge)

Use this skill when capturing, processing, or transforming raw technical knowledge from real-world work (such as production incident logs, query tuning scripts, configuration guides, quick notes in `inbox/`, or external bookmarks) into the structured MkDocs Knowledge Base.

---

## 1. Input Processing & Ingestion

Input có thể đến từ:
1. **Tệp thô trong `inbox/`** (ví dụ: `inbox/sample-pg-lock-incident.md` hoặc một tệp text ghi chú bất kỳ).
2. **Nội dung dán trực tiếp trong chat box** từ kỹ sư (error trace, SQL snippet, log post-mortem).

### Nhiệm vụ trích xuất:
- **Xác định Pillar**: `postgresql`, `java`, `spring-boot`, `aws`, hoặc `system-design`.
- **Xác định phiên bản mục tiêu**: PostgreSQL 16+, Java 21 LTS, Spring Boot 3.3+, AWS IAM v2, v.v.
- **Trích xuất cốt lõi kỹ thuật**: Hiện tượng, root cause, câu lệnh truy vấn, hoặc giải pháp kiến trúc.

---

## 2. Kiểm Tra Trùng Lặp & Bản Đồ Tri Thức (Deduplication Check)

Trước khi tạo bất kỳ tệp mới nào, **bắt buộc phải tìm kiếm** trong thư mục `docs/`:

1. Sử dụng công cụ `grep_search` hoặc duyệt thư mục để kiểm tra xem chủ đề/API này đã được ghi chép ở đâu chưa.
2. **Quy tắc phân loại hành động**:
   - **Đã tồn tại trang chính**: Nếu trang hiện tại (ví dụ: `docs/postgresql/explain-analyze.md`) có thể bổ sung phần phân tích này vào mục Gotchas hoặc Use Cases, hãy **cập nhật trang hiện có** thay vì tạo trang mới.
   - **Chủ đề liên quan chặt chẽ**: Nếu nội dung đủ lớn để tạo một bài độc lập (ví dụ: một bài Troubleshooting sự cố Lock), hãy tạo bài mới và **bắt buộc tạo liên kết chéo (bi-directional cross-link)** giữa trang mới và trang liên quan.
   - **Mới hoàn toàn**: Tạo trang mới trong thư mục trụ cột tương ứng.

---

## 3. Phân Loại Tri Thức & Chọn Tuyến Xử Lý (Classification & Routing)

Đánh giá dạng tri thức để chọn template hoặc điều phối sang skill chuyên biệt:

| Dạng tri thức | Tiêu chí nhận diện | Hành động / Tuyến xử lý |
| :--- | :--- | :--- |
| **Troubleshooting Case** | Sự cố production, lỗi timeout, lock contention, memory leak, exception crash. | Dùng `templates/troubleshooting-template.md` -> Lưu vào `docs/<pillar>/troubleshooting-<topic>.md`. |
| **How-To Guide** | Hướng dẫn cấu hình từng bước, quy trình migration, setup service. | Dùng `templates/how-to-template.md` -> Lưu vào `docs/<pillar>/how-to-<topic>.md`. |
| **SQL / Code Recipe** | Tập hợp các câu query giám sát, script tự động, utility pattern. | Dùng `templates/code-recipe-template.md` -> Lưu vào `docs/<pillar>/recipe-<topic>.md`. |
| **Deep Concept** | Cơ chế hoạt động phức tạp cần đối chiếu sâu tài liệu chuẩn. | Kích hoạt hoặc kế thừa quy trình từ **`research-topic`**. |
| **Sách / Nghiên cứu** | Tóm tắt từ sách kỹ thuật hoặc bài báo nghiên cứu. | Kích hoạt **`summarize-book`**. |
| **NotebookLM Export** | Ghi chú xuất từ NotebookLM. | Kích hoạt **`import-notebooklm`**. |
| **Lab Thực Nghiệm** | Cần môi trường Docker để benchmark hoặc tái lập. | Kích hoạt **`create-hands-on-lab`** (Lưu code vào `labs/`). |

---

## 4. Biên Soạn & Quy Chuẩn Ngôn Ngữ

1. **Ngôn ngữ**: Tiếng Việt mạch lạc, giữ nguyên thuật ngữ tiếng Anh chuyên ngành (*Query Planner, Deadlock, Connection Pool, Write-Ahead Log, Thread Pinning*).
2. **Mã nguồn**: Code blocks phải có chỉ định ngôn ngữ rõ ràng (`sql`, `java`, `bash`, `yaml`), parameterized queries, không chứa secrets.
3. **Sơ đồ Mermaid**: Trực quan hóa luồng xử lý hoặc chuỗi nguyên nhân - kết quả nếu giải thích lỗi phân tán/bộ nhớ.
4. **Official Links**: Bắt buộc đối chiếu và dẫn link từ Official Documentation tương ứng.

---

## 5. Cập Nhật Navigation & Liên Kết Chéo (Cross-Linking)

1. Cập nhật `nav` trong `mkdocs.yml` tương ứng với phân mục của tệp mới.
2. Cập nhật trang tổng quan của trụ cột (`docs/<pillar>/index.md`), thêm bài viết mới vào danh mục liên quan.
3. Tạo liên kết hai chiều với các bài viết có liên quan (ví dụ: bài Troubleshooting Lock trỏ tới bài EXPLAIN ANALYZE và ngược lại).

---

## 6. Kiểm Thử Nghiêm Ngặt & Dọn Dẹp

1. Chạy lệnh kiểm tra tính toàn vẹn:
   ```powershell
   python -m mkdocs build --strict
   ```
2. Nếu xuất hiện cảnh báo (broken links, syntax error), sửa chữa ngay lập tức.
3. Sau khi tích hợp thành công, chuyển file thô trong `inbox/` vào `inbox/archive/` hoặc thông báo hoàn tất cho người dùng.
