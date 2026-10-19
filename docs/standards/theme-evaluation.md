# Đánh Giá Kiến Trúc: Material for MkDocs vs. Zensical

Trong quá trình thiết kế hệ thống **Personal Developer Knowledge Base**, việc lựa chọn nền tảng sinh trang tĩnh (Static Site Generator - SSG) và giao diện hiển thị (Theme) quyết định trực tiếp tới tốc độ hiển thị, khả năng tìm kiếm tức thì, độ ổn định lâu dài và khả năng mở rộng.

Tài liệu này ghi nhận quá trình đánh giá kiến trúc giữa hai ứng viên hàng đầu: **Material for MkDocs** và **Zensical**.

---

## 1. Bối cảnh & Mục tiêu Đánh giá

Hệ thống tài liệu hướng tới:
1. **Tìm kiếm siêu tốc (Instant Search)**: Tìm kiếm theo cả tiếng Việt và thuật ngữ kỹ thuật tiếng Anh mà không cần setup backend Elasticsearch phức tạp.
2. **Hỗ trợ Code & Diagram mạnh mẽ**: Syntax highlighting, code annotation, copy button một chạm, và hiển thị sơ đồ Mermaid mượt mà.
3. **Giao diện hiện đại (Modern UX)**: Dark/Light mode tự động và thủ công, navigation tabs, sticky header, responsive trên mobile/tablet/desktop.
4. **Độ ổn định cho quy trình CI/CD**: Chạy được cờ `--strict` không phát sinh lỗi hoặc cảnh báo ngầm.

---

## 2. Bảng So sánh Toàn diện (Comparative Matrix)

| Tiêu chí | Material for MkDocs (`mkdocs-material`) | Zensical (`zensical`) |
| :--- | :--- | :--- |
| **Tác giả & Xuất xứ** | Martin Donath (Squidfunk) - Dự án nguồn mở thành công bậc nhất hệ sinh thái Python. | Martin Donath (Squidfunk) - Dự án kế nhiệm được phát triển độc lập (Rust-based). |
| **Giai đoạn phát triển** | **Maturity (v9.5+)**: Ổn định tuyệt đối, kiểm chứng trên hàng trăm ngàn dự án (FastAPI, Pydantic, Typer, AWS CLI v2 docs). | **Early Alpha / Pre-1.0 (v0.0.70)**: Đang trong quá trình định hình API và cấu trúc tệp (`zensical.toml`). |
| **Hệ sinh thái Plugin** | Tương thích 100% với toàn bộ hệ sinh thái plugin Python MkDocs (`pymdown-extensions`, `mkdocs-git-revision-date-localized-plugin`, v.v.). | Đang tái hiện các tính năng; các plugin bên thứ ba cần cơ chế bridge hoặc chưa hỗ trợ đầy đủ. |
| **Chế độ kiểm thử nghiêm ngặt** | Hỗ trợ chuẩn `mkdocs build --strict` với khả năng kiểm tra broken link, missing nav hoàn hảo. | Bộ kiểm thử và toolchain CLI đang trong giai đoạn hoàn thiện. |
| **Code Highlighting & Copy** | Tích hợp sâu Pygments & `pymdownx.highlight`, hỗ trợ line highlighting, code annotation, copy buttons. | Hỗ trợ styling cơ bản; cấu hình chi tiết nâng cao còn giới hạn. |
| **Dark / Light Palette Toggle** | Cấu hình hoàn chỉnh thông qua `palette` trong `mkdocs.yml`, hỗ trợ chuyển đổi icon mặt trời/mặt trăng theo prefers-color-scheme. | Đang được tích hợp theo kiến trúc mới. |

---

## 3. Quyết định Kiến trúc (Architectural Decision Record - ADR)

### Quyết định
👉 **Lựa chọn Material for MkDocs làm Theme chủ đạo cho hệ thống.**

### Lý do lựa chọn (Rationale)
1. **Độ tin cậy cho Production**: `mkdocs-material` là tiêu chuẩn vàng của ngành công nghiệp. Mọi tính năng cần thiết cho một Senior Software Architect (bảng biểu, sơ đồ mermaid, code block có tabs, cảnh báo admonition, callouts) đều hoạt động trơn tru.
2. **Khả năng kiểm soát chất lượng**: Cho phép kích hoạt `mkdocs build --strict` trong CI/CD, ngăn chặn triệt để tình trạng link hỏng hoặc trang mồ côi (orphan pages).
3. **Lộ trình tương lai (Future-Proof)**: Vì Zensical được sáng lập bởi chính đội ngũ tác giả của Material for MkDocs và hỗ trợ tương thích drop-in với `mkdocs.yml`, cấu trúc tài liệu Markdown và cấu hình hiện tại sẽ dễ dàng di chuyển (migrate) sang Zensical trong tương lai khi Zensical đạt phiên bản ổn định 1.0.
