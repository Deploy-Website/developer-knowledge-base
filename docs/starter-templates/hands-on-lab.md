# Biểu Mẫu: Tài Liệu Hướng Dẫn Thí Nghiệm (Hands-on Lab Template)

Biểu mẫu chuẩn để viết bài hướng dẫn thực nghiệm và đo lường cho các Hands-on Lab. Lưu ý rằng toàn bộ source code thực thi (Docker Compose, SQL scripts, code test) phải nằm trong thư mục `labs/` bên ngoài `docs/`.

---

````markdown
# [Tên Lab]: Thí nghiệm Thực hành & Đo lường

> **Lĩnh vực**: [PostgreSQL / Java / Spring Boot / AWS / System Design]  
> **Đường dẫn mã nguồn lab**: `labs/<topic>/<lab-name>/`  
> **Thời gian dự kiến**: [15 - 30 phút]  
> **Môi trường**: Docker / Docker Compose / Local CLI  

---

## 1. Mục tiêu Thí nghiệm (Lab Objective)

- **Bài toán cần giải quyết**: Mô tả hiện tượng thực tế cần tái lập hoặc kiểm chứng (ví dụ: So sánh thời gian thực thi giữa Bitmap Heap Scan và Seq Scan trên 1 triệu records).
- **Kết quả đo lường kỳ vọng (Expected Metrics)**:
  - Latency / Execution Time (ms)
  - Buffer Hits vs Disk Reads
  - Resource consumption (Memory / CPU)

---

## 2. Chuẩn bị Môi trường (Environment Setup)

Toàn bộ mã nguồn thực thi được đặt cô lập bên ngoài thư mục tài liệu tại:  
👉 **`labs/<topic>/<lab-name>/`**

### Yêu cầu tiên quyết (Prerequisites)
- Docker Desktop hoặc Docker Engine với Docker Compose v2+.
- Client tool tương ứng (ví dụ: `psql`, `curl`, `jq`).

### Khởi động Lab
```bash
cd labs/<topic>/<lab-name>
docker compose up -d
```

---

## 3. Các Bước Thực nghiệm (Step-by-Step Scenarios)

### Kịch bản 1: [Tên kịch bản 1 - Baseline Measurement]
1. Thực thi câu lệnh / script:
   ```sql
   -- Query test baseline
   ```
2. Phân tích kết quả thu được:
   - Thông số quan sát.
   - Hiện tượng kỹ thuật diễn ra bên dưới.

### Kịch bản 2: [Tên kịch bản 2 - Optimized Scenario]
1. Áp dụng kỹ thuật tối ưu (Tạo index, tinh chỉnh memory, đổi thread pool):
   ```sql
   -- Query test sau tối ưu
   ```
2. So sánh đối chiếu với Kịch bản 1.

---

## 4. Bảng Kết quả So sánh & Đo lường (Benchmark & Metrics)

| Chỉ số quan trắc | Kịch bản 1 (Trước) | Kịch bản 2 (Sau) | Mức cải thiện |
| :--- | :--- | :--- | :--- |
| **Execution Time** | ... ms | ... ms | **Giảm x%** |
| **Buffer Cache Read** | ... pages | ... pages | **Tối ưu x%** |
| **I/O Overhead** | ... | ... | ... |

---

## 5. Đúc kết Kiến trúc & Bài học Production (Architectural Lessons)

- **Khi nào áp dụng giải pháp này**: ...
- **Những tác dụng phụ (Side-effects)**: ...
- **Dọn dẹp môi trường (Teardown)**:
  ```bash
  docker compose down -v
  ```
````
