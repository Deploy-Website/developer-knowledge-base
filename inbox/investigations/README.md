# Vùng Tiếp Nhận Điều Tra Kỹ Thuật (Engineering Investigations Staging)

Thư mục này là staging area dành cho các **cuộc điều tra kỹ thuật nhiều bước (Multi-step Engineering Investigations)**, các thí nghiệm gỡ lỗi phức tạp (Debugging experiments), quá trình tuning hiệu năng, hoặc sự cố kéo dài nhiều ngày trước khi được tổng hợp thành tài liệu chính thức.

---

## 📁 Cấu Trúc Thư Mục Điều Tra (Investigation Directory Structure)

Mỗi cuộc điều tra được quản lý trong một thư mục định danh riêng:

```text
inbox/investigations/
├── README.md                           # Tài liệu hướng dẫn này
└── <investigation-id>/                 # Ví dụ: inv-202610-pg-jsonb-tuning/
    ├── notes.md                        # Ghi chú thô theo tiến trình thời gian (Sử dụng templates/investigation-raw.md)
    ├── attachments/                    # Execution plans thô (.txt/.json), flamegraphs (.svg), configs
    └── private/                        # Dữ liệu nhạy cảm (Được tự động bỏ qua bởi .gitignore)
```

---

## 🔒 Quy Định Bảo Mật & An Toàn Thông Tin (Privacy & Sanitization)

> [!CAUTION]
> **Tuyệt đối không lưu trữ thông tin nhạy cảm vào Git**:
> - Không lưu mật khẩu, tokens, AWS keys, hoặc PII (Personally Identifiable Information) của khách hàng.
> - Các tệp dump database, file pcap hoặc log chứa dữ liệu thật phải đặt trong thư mục `private/` hoặc đặt tên có đuôi `.secret.*`, `.dump`, `.pcap` (đã được khai báo trong `.gitignore`).
> - Luôn che mờ (mask/anonymize) IP nội bộ, tên khách hàng và domain nhạy cảm trước khi công bố vào `docs/`.

---

## 🔄 Quy Trình Xử Lý Với Agent Skill `document-investigation`

1. **Ghi chép thô**: Sao chép `templates/investigation-raw.md` vào `<investigation-id>/notes.md` và ghi lại câu hỏi, giả thuyết, lệnh đã chạy và kết quả quan sát.
2. **Kích hoạt Agent**:
   ```text
   Hãy sử dụng skill 'document-investigation' để xử lý hồ sơ điều tra tại:
   inbox/investigations/<investigation-id>/notes.md
   ```
3. **Cập nhật lũy tiến (Incremental Updates)**:
   Nếu cuộc điều tra có thêm bằng chứng mới sau vài ngày:
   ```text
   Tôi vừa bổ sung Thí nghiệm 4 vào inbox/investigations/<investigation-id>/notes.md.
   Hãy cập nhật bài viết điều tra hiện tại mà không làm mất lịch sử các thí nghiệm trước đó.
   ```
