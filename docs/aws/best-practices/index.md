# AWS Cloud Architecture Best Practices Hub

> **Trọng tâm**: Các quy chuẩn thực hành thiết kế và vận hành đám mây chuẩn mực theo AWS Well-Architected Framework, tập trung vào Kiến trúc mạng an toàn (VPC Isolation & PrivateLink), Tối ưu hóa tầng dữ liệu (Amazon Aurora & DynamoDB), Xử lý thông điệp bền vững (SQS FIFO/SNS), và Tối ưu chi phí truyền dữ liệu (Data Transfer & Export).  
> **Nguyên tắc kỹ thuật**: Tuân thủ [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/) và tài liệu kỹ thuật chính hãng AWS Documentation.

---

## 1. Mục Tiêu & Triết Lý Thực Hành AWS

Đám mây AWS cung cấp tài nguyên vô tận, nhưng cũng tiềm ẩn rủi ro chi phí khổng lồ và lỗ hổng bảo mật nếu áp dụng các giải pháp tùy tiện (ví dụ: mở cổng database ra public, dùng static access keys, hoặc export dữ liệu ra ngoài Internet).

Kho lưu trữ Best Practices của AWS tập trung vào:
1. **Bảo mật mặc định (Security by Default)**: 100% traffic nội bộ đi qua AWS PrivateLink / VPC Endpoints, xác thực qua IAM Role (IRSA) với nguyên tắc Least Privilege.
2. **Khả năng chịu lỗi đa vùng (Multi-AZ Resilient Architecture)**: Thiết kế loại bỏ hoàn toàn các điểm nghẽn đơn lẻ (Single Points of Failure - SPOF).
3. **Hiệu năng & Tối ưu hóa chi phí (Cost-Performance Efficiency)**: Tận dụng các tính năng native của AWS (như Aurora Storage Subsystem hoặc `aws_s3` extension) thay vì dựng các máy chủ trung gian cồng kềnh.

---

## 2. Danh Mục Các Thực Hành Đã Chuẩn Hóa (Curated Best Practices)

| Chủ đề / Bài viết | Trọng tâm kỹ thuật | Mức độ bằng chứng | Liên kết chuẩn |
| :--- | :--- | :--- | :--- |
| ☁️ **[Export Dữ Liệu Lớn từ Aurora sang S3](aurora-s3-export.md)** | Chuyển đổi dữ liệu quy mô lớn (> 100GB) bằng `aws_s3.query_export_to_s3()`, phân quyền IAM Role, nén GZIP qua VPC Endpoint S3; loại bỏ chi phí máy trung gian và network egress. | **Context-specific Finding** | AWS Aurora Docs & S3 PrivateLink |

---

## 3. Hệ Thống Cấp Độ Bằng Chứng (Evidence Classification)

Mỗi thực hành trong danh mục được gắn nhãn minh bạch:
- 🟢 **Official Guidance**: Khuyến nghị từ Whitepapers và AWS Well-Architected Framework.
- 🔵 **Verified Experiment**: Đã kiểm chứng qua benchmark thực tế trên môi trường AWS Lab / Production.
- 🟡 **Context-specific Finding**: Tối ưu trong một cấu hình VPC / Dataset quy mô cụ thể.
- ⚪ **Candidate**: Đang trong quá trình thử nghiệm.

---

## 4. Liên Kết Tri Thức Liên Quan

- **Lý thuyết nền tảng**:
  - [AWS Cloud Architecture Knowledge Hub](../index.md)
  - [PostgreSQL Best Practices: JSONB Query Optimization](../../postgresql/best-practices/jsonb-query-optimization.md)
- **Tài liệu chính thức**:
  - [AWS Well-Architected Tool & Lenses](https://aws.amazon.com/architecture/well-architected/)
  - [Amazon Aurora PostgreSQL User Guide](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html)
