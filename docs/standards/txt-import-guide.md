# Hướng Dẫn Nhập Ghi Chú TXT (TXT Notes Import Guide)

> **Mục tiêu**: Hướng dẫn quy trình soạn thảo ghi chú kỹ thuật dạng text (`.txt`) trong thư mục `nodes/`, quy tắc phân loại tự động và cách sử dụng công cụ `import-txt-notes` để chuyển đổi thành tài liệu MkDocs chuẩn mực.

---

## 1. Cấu Trúc File Ghi Chú TXT (TXT Note Format)

Mỗi ghi chú kỹ thuật được lưu trong thư mục `nodes/<filename>.txt` theo định dạng chuẩn:

```text
Item: <Tiêu đề tài liệu>
Type: <Dạng tài liệu>
Domain: <Lĩnh vực công nghệ>

Content:
<Nội dung kỹ thuật thô, các bước thực hiện, câu lệnh,
đoạn code / SQL, kết quả quan sát và kết luận>
```

---

## 2. Quy Tắc Các Trường Dữ Liệu (Field Specifications)

### 2.1. Trường `Item`
- Đại diện cho **tiêu đề chính** của tài liệu.
- Được sử dụng làm nhãn hiển thị trong menu điều hướng MkDocs (`mkdocs.yml`).
- Được đặt làm tiêu đề H1 (`# <Item>`) trong file Markdown xuất bản.
- Hệ thống tự động sinh tên file (slug) chuẩn SEO từ `Item` (ví dụ: `postgresql-b-tree-index-deduplication.md`).

### 2.2. Trường `Type`
Xác định danh mục điều hướng và thư mục đích theo bảng quy chuẩn:

| Giá trị `Type` (Bao gồm các bí danh) | Thư mục đích trong `docs/` | Danh mục Menu MkDocs |
| :--- | :--- | :--- |
| `Best Practice`, `best-practice`, `thực hành` | `docs/<domain>/best-practices/` | `Best Practices` |
| `Concept`, `concepts`, `khái niệm` | `docs/<domain>/concepts/` | `Concepts` |
| `How-to`, `howto`, `hướng dẫn` | `docs/<domain>/how-to/` | `How-to` |
| `Investigation`, `điều tra` | `docs/<domain>/investigations/` | `Investigations` |
| `Troubleshooting`, `sự cố` | `docs/<domain>/troubleshooting/` | `Troubleshooting` |
| `Lab`, `hands-on lab` | `docs/<domain>/labs/` | `Labs` |
| `Recipe`, `code recipe`, `sql recipe` | `docs/<domain>/recipes/` | `Recipes` |

*Lưu ý*: Hệ thống tự động chuẩn hóa chữ hoa/chữ thường. Nếu `Type` không hợp lệ, hệ thống sẽ báo lỗi và từ chối xuất bản.

### 2.3. Trường `Domain`
Xác định trụ cột công nghệ trong `docs/<domain>/`:
- `PostgreSQL` -> `docs/postgresql/`
- `Java` -> `docs/java/`
- `Spring Boot` -> `docs/spring-boot/`
- `AWS` -> `docs/aws/`
- `System Design` -> `docs/system-design/`

*Cơ chế suy luận tự động (Inference)*: Nếu trường `Domain` bị bỏ trống, hệ thống sẽ quét từ khóa kỹ thuật trong `Item` và `Content`. Nếu xác định rõ ràng (e.g., chứa `PostgreSQL`, `Spring Boot`), hệ thống tự động gán domain. Nếu không thể xác định hoặc mâu thuẫn, file sẽ bị gắn cờ yêu cầu xem xét thủ công.

---

## 3. Cách Thức Thực Hiện Import

Hệ thống cung cấp script tự động tại `.agents/skills/import-txt-notes/scripts/import_notes.py`.

### 3.1. Import Một File Đơn Lẻ (Single File Mode)
Dùng khi vừa tạo hoặc cập nhật một file TXT cụ thể:
```bash
python .agents/skills/import-txt-notes/scripts/import_notes.py --file nodes/postgresql-index-deduplication.txt --validate
```

### 3.2. Import Hàng Loạt (Batch Mode)
Dùng để quét toàn bộ các file `.txt` có trong thư mục `nodes/`:
```bash
python .agents/skills/import-txt-notes/scripts/import_notes.py --batch --validate
```
Trong chế độ Batch:
- Mỗi file được kiểm tra và xử lý độc lập (Failure Isolation).
- File lỗi không ảnh hưởng tới các file hợp lệ khác.
- Hệ thống in bảng tổng kết: Thành công, Bỏ qua, Xung đột và Lỗi.

### 3.3. Xem Báo Cáo Trạng Thái (Manifest Report)
Kiểm tra danh sách các file đã được import qua file theo dõi `nodes/.import-manifest.json`:
```bash
python .agents/skills/import-txt-notes/scripts/import_notes.py --report
```

---

## 4. Cơ Chế Chống Trùng Lặp & Tính Lũy Thừa (Idempotency)

Quy trình import an toàn để chạy nhiều lần liên tục nhờ cơ chế theo dõi:
1. **Kiểm tra mã băm (SHA-256 Hash)**: Mỗi lần import, mã hash nội dung file TXT được lưu vào `nodes/.import-manifest.json`. Nếu chạy lại mà file TXT không thay đổi, hệ thống báo `SKIPPED (idempotent)` và không ghi đè file Markdown hay thay đổi menu.
2. **Phát hiện xung đột (Collision Detection)**: Nếu file Markdown đích đã tồn tại nhưng không xuất phát từ file TXT này (hoặc được tạo thủ công từ trước), hệ thống đánh dấu `CONFLICT`, giữ nguyên file cũ và không tự ý ghi đè.
3. **Bảo tồn file gốc**: Không bao giờ xóa hay sửa đổi các file `.txt` gốc trong `nodes/`.

---

## 5. Xử Lý Khi Import Thất Bại (Troubleshooting Failed Imports)

| Nguyên nhân | Triệu chứng | Cách khắc phục |
| :--- | :--- | :--- |
| **Thiếu trường Item / Type** | `[FAILED] Missing required field 'Item:'` | Bổ sung dòng `Item: <Tiêu đề>` ở đầu file TXT. |
| **Type không hỗ trợ** | `[FAILED] Unsupported Type 'tutorial'` | Đổi `Type` về một trong 7 loại chuẩn (`Best Practice`, `How-to`, `Concept`, ...). |
| **Domain không xác định** | `[FAILED] Domain is missing and could not be inferred` | Khai báo rõ ràng dòng `Domain: <PostgreSQL / Java / ...>`. |
| **Trùng tên file khác nguồn**| `[CONFLICT] Destination file exists and belongs to a different source` | Đổi tên `Item` cụ thể hơn để tránh trùng slug với tài liệu hiện có. |

---

## 6. Kiểm Tra & Xác Thực Thay Đổi (Verification)

Sau khi import thành công, chạy lệnh kiểm tra nghiêm ngặt:
```bash
python -m mkdocs build --strict
```
Đảm bảo lệnh trả về mã thoát `0` và 0 warnings. Mở trình duyệt tại `http://127.0.0.1:8000` để kiểm tra trực quan giao diện.

---

## 7. Ví Dụ Mẫu Hoàn Chỉnh

### Ví Dụ 1 — PostgreSQL Best Practice
`nodes/postgresql-index-deduplication.txt`:
```text
Item: PostgreSQL B-Tree Index Deduplication
Type: Best Practice
Domain: PostgreSQL

Content:
Trong PostgreSQL 13 trở lên, tính năng B-Tree Index Deduplication (nbtree deduplication) được kích hoạt mặc định. Cơ chế này tự động nén các giá trị khóa trùng lặp trong leaf pages của B-Tree index, giúp giảm 73% kích thước chỉ mục trên các cột low-cardinality như status, is_active.

-- Tạo index tối ưu deduplication cho cột status
CREATE INDEX CONCURRENTLY idx_orders_status ON orders (status) WITH (deduplicate_items = on);
```

### Ví Dụ 2 — Spring Boot How-to
`nodes/spring-boot-virtual-threads.txt`:
```text
Item: Cấu Hình Virtual Threads Cho Spring Boot 3.3
Type: How-to
Domain: Spring Boot

Content:
Mục tiêu: Kích hoạt Virtual Threads trong Spring Boot 3.3+ để tăng thông lượng I/O blocking.

Bước 1: Kích hoạt trong application.yml
spring:
  threads:
    virtual:
      enabled: true

Bước 2: Thay thế synchronized bằng ReentrantLock để tránh Thread Pinning.
```
