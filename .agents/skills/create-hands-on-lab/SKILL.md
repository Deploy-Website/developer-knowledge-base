---
name: create-hands-on-lab
description: >-
  Designs and builds isolated, reproducible hands-on engineering labs with Docker Compose, seed scripts,
  and benchmark queries placed in the labs/ directory (strictly separated from docs/).
---

# Skill: Create Hands-on Lab (create-hands-on-lab)

Use this skill when developing an interactive, reproducible lab to demonstrate or benchmark a technical concept (e.g., PostgreSQL indexing strategies, Java GC tuning, Spring Boot transaction propagation, AWS LocalStack emulation).

## Strict Directory Separation Rule
- **Executable Source Code**: PHẢI nằm trong thư mục `labs/<topic>/<lab-name>/`.
  - Tuyệt đối KHÔNG đặt `docker-compose.yml`, SQL files, bash scripts, hay Java project vào thư mục `docs/`.
- **Documentation Guide**: Tài liệu hướng dẫn tóm tắt nằm trong `docs/<topic>/...` và dẫn link tương đối sang thư mục `labs/`.

## Workflow

### 1. Lab Objective & Criteria
- Xác định mục tiêu thí nghiệm đo lường được:
  - *Ví dụ*: Chứng minh sự khác biệt về execution time và buffer hit giữa `Seq Scan` và `Index Scan` trên bảng 1.000.000 dòng.
- Liệt kê các điều kiện tiền đề (Prerequisites): Docker, Docker Compose, RAM tối thiểu, công cụ client.

### 2. Scaffold the Lab Directory
Tạo thư mục `labs/<topic>/<lab-name>/` với cấu trúc tiêu chuẩn:
```text
labs/<topic>/<lab-name>/
├── docker-compose.yml    # Khởi tạo môi trường isolated với version cụ thể
├── init.sql (hoặc init/) # Seed dữ liệu mẫu (100k - 1M rows với skewed distribution)
├── queries.sql / scripts # Các câu lệnh benchmark hoặc mã nguồn thực thi
└── README.md             # Hướng dẫn chi tiết từng bước tái lập (reproduction)
```

### 3. Reproducible & Robust Setup
- `docker-compose.yml`:
  - Dùng container image có pinned tag cụ thể (ví dụ: `postgres:16-alpine`, không dùng `:latest`).
  - Cấu hình resource limits (CPU, RAM) và volume an toàn.
  - Expose port thích hợp, tránh xung đột port mặc định của host nếu cần.
- Data Seed (`init.sql`):
  - Tự động sinh dữ liệu thực tế bằng các hàm SQL có sẵn (ví dụ: `generate_series()`, `random()`, `md5()`).
  - Luôn chạy `ANALYZE` sau khi seed để cập nhật database statistics.

### 4. Step-by-Step Lab Documentation
Tạo tệp `README.md` bên trong thư mục lab theo cấu trúc:
1. **Mục tiêu & Yêu cầu hệ thống**.
2. **Khởi động môi trường**: `docker compose up -d`.
3. **Các kịch bản thực nghiệm (Scenarios)**: Từng bước chạy lệnh, giải thích kỳ vọng và kết quả thực tế.
4. **Clean up**: `docker compose down -v`.

### 5. Companion Docs Page
- Sử dụng `templates/hands-on-lab-template.md` để tạo bài viết tổng hợp trong `docs/<topic>/`.
- Thêm link liên kết đến `labs/<topic>/<lab-name>/`.
- Chạy kiểm tra:
  ```powershell
  python -m mkdocs build --strict
  ```
