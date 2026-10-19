# Nodes Staging Directory (TXT Notes Import)

Thư mục này là staging area chứa các ghi chú kỹ thuật thô dưới định dạng văn bản thuần (`.txt`) để tự động chuyển đổi thành tài liệu MkDocs thông qua Agent Skill **`import-txt-notes`**.

---

## 1. Định Dạng File TXT Chuẩn

Mỗi file trong thư mục này phải có cấu trúc:

```text
Item: <Tiêu đề tài liệu>
Type: <Best Practice | Concept | How-to | Investigation | Troubleshooting | Lab | Recipe>
Domain: <PostgreSQL | Java | Spring Boot | AWS | System Design>

Content:
<Nội dung ghi chú, câu lệnh, mã nguồn, quan sát...>
```

---

## 2. Lệnh Import Nhanh

### Import một file:
```bash
python .agents/skills/import-txt-notes/scripts/import_notes.py --file nodes/your-note.txt --validate
```

### Import hàng loạt:
```bash
python .agents/skills/import-txt-notes/scripts/import_notes.py --batch --validate
```

### Xem báo cáo các file đã import:
```bash
python .agents/skills/import-txt-notes/scripts/import_notes.py --report
```

---

## 3. Quy Tắc Hoạt Động
- File gốc trong `nodes/` luôn được bảo tồn, không bao giờ bị xóa.
- Hệ thống theo dõi mã hash nội dung trong `nodes/.import-manifest.json` để chống trùng lặp (Idempotent).
- Chi tiết hướng dẫn xem tại: [docs/standards/txt-import-guide.md](../docs/standards/txt-import-guide.md).
