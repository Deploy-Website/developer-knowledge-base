# Biểu Mẫu: Ghi Chép Thô Tiến Trình Điều Tra (Raw Investigation Notes)

Biểu mẫu tối ưu hóa cho tốc độ ghi chép nhanh trong quá trình điều tra kỹ thuật (Debugging, Root Cause Analysis, Query Optimization). Kỹ sư chỉ cần điền các câu hỏi, giả thuyết, lệnh đã chạy và kết quả thô mà không cần trau chuốt câu từ.

---

````markdown
# Raw Investigation Notes: [Tên Cuộc Điều Tra / Chủ Đề]

> **Mã điều tra (ID)**: inv-[YYYYMM]-[short-slug]  
> **Ngày bắt đầu**: YYYY-MM-DD  
> **Người thực hiện**: [Tên kỹ sư / Nhóm]  
> **Lĩnh vực**: [PostgreSQL / Java / Spring Boot / AWS / System Design]  
> **Môi trường**: [Production / Staging / Test Lab]  
> **Trạng thái hiện tại**: [In Progress / Partially Resolved / Resolved / Blocked]  

---

## 1. Vấn Đề Ban Đầu (Initial Problem Statement)
- Hiện tượng quan sát được:
- Bối cảnh / Hệ thống bị ảnh hưởng:
- Dấu hiệu cảnh báo hoặc log ngoại lệ ban đầu:

---

## 2. Các Câu Hỏi Đặt Ra (Questions to Investigate)
- [ ] Q1: ...
- [ ] Q2: ...

---

## 3. Nhật Ký Tiến Trình Thí Nghiệm (Chronological Log)

### [Thời gian / Bước 1]: [Mô tả ngắn gọn bước thực hiện]
- **Câu hỏi**:
- **Giả thuyết (Hypothesis)**:
- **Hành động / Lệnh đã chạy (Commands / Code / SQL)**:
  ```bash
  # Lệnh thực thi
  ```
- **Kết quả quan sát (Observations / Metrics / Plan)**:
  ```text
  Kết quả trả về, metrics hoặc log
  ```
- **Phân tích (Analysis)**:
- **Đánh giá**: [Thất bại / Không hiệu quả / Có tiến triển / Thành công]
- **Quyết định kế tiếp (Next Step)**:

---

### [Thời gian / Bước 2]: [Mô tả ngắn gọn bước tiếp theo]
- **Câu hỏi**:
- **Giả thuyết (Hypothesis)**:
- **Hành động / Lệnh đã chạy**:
- **Kết quả quan sát**:
- **Phân tích**:
- **Quyết định kế tiếp**:

---

## 4. Kết Quả & Đúc Kết Tạm Thời (Current Outcome)
- **Giải pháp tạm thời / Cuối cùng (nếu có)**:
- **Các giả thuyết bị bác bỏ (Failed Hypotheses)**:
- **Các câu hỏi còn bỏ ngỏ (Open Questions)**:
- **Tài liệu đính kèm liên quan**: [attachments/...]
````
