---
name: review-knowledge
description: >-
  Audits knowledge base articles and labs for factual correctness, official source alignment,
  security hygiene, link integrity, and MkDocs strict build compliance.
---

# Skill: Review Knowledge (review-knowledge)

Use this skill when auditing existing documentation, reviewing newly proposed knowledge notes, verifying external links, or troubleshooting MkDocs build warnings.

## Workflow

### 1. Factual Correctness & Source Verification
- **Đối chiếu Official Documentation**: Kiểm tra từng API signature, command flag, và kiến trúc đối với phiên bản tương ứng.
- **Phát hiện Deprecated Patterns**: Cảnh báo nếu bài viết sử dụng tính năng đã lỗi thời (ví dụ: SecurityConfigurerAdapter trong Spring Security 6, các tham số postgresql.conf cũ).
- **Phát hiện Hallucination**: Đảm bảo không có thông số benchmark tự vẽ, giả định phi thực tế, hoặc trích dẫn thiếu căn cứ.
- **Rà soát Best Practices & Cấp độ Bằng chứng**:
  - Xác nhận mọi bài viết Best Practice đều khai báo `Evidence Level` hợp lệ (`Official Guidance`, `Verified Experiment`, `Context-specific Finding`, `Candidate`).
  - Phát hiện các mâu thuẫn kỹ thuật (Contradictions) hoặc hướng dẫn chồng chéo giữa các bài Best Practice.
  - Cảnh báo nếu các thử nghiệm chưa được xác minh bị dán nhãn sai thành chuẩn mực phổ quát.

### 2. Language & Terminology Audit
- Kiểm tra tính nhất quán: Sử dụng tiếng Việt chuẩn xác kết hợp thuật ngữ tiếng Anh tự nhiên.
- Không dịch gượng ép các thuật ngữ cốt lõi (giữ nguyên: *Connection Pool, Thread Dump, Deadlock, B-Tree, Write-Ahead Log, Distributed Transaction, Event Sourcing*).

### 3. Code & Security Audit
- Kiểm tra bí mật (Secrets): Tuyệt đối không để lộ private keys, passwords, hoặc API credentials.
- Kiểm tra tính an toàn: Mã nguồn phải có parameterized queries, timeouts cho I/O, và cơ chế đóng resource (`AutoCloseable`).
- Kiểm tra tính cô lập của Labs: Xác nhận source code thực thi nằm trong `labs/`, không nằm trong `docs/`.

### 4. Link & Structure Integrity
- Kiểm tra tất cả internal links trong markdown:
  - Phải có file đích thực sự tồn tại.
  - Phải trỏ đúng cú pháp đường dẫn tương đối (e.g., `[Title](../topic/file.md)`).
- Kiểm tra mục lục trong `mkdocs.yml`: Đảm bảo mọi file trong `docs/` đều được quản lý rõ ràng.

### 5. Automated Build Validation
Chạy lệnh kiểm thử với chế độ `--strict` (coi mọi warning là lỗi):
```powershell
python -m mkdocs build --strict
```
Nếu xuất hiện cảnh báo, tiến hành sửa chữa ngay lập tức cho đến khi build thành công tuyệt đối (exit code 0).
