---
name: summarize-book
description: >-
  Distills core architecture insights, mental models, failure modes, and practical trade-offs from
  foundational software engineering and distributed systems books into structured notes.
---

# Skill: Summarize Book (summarize-book)

Use this skill when distilling knowledge from engineering books (such as *Designing Data-Intensive Applications*, *Database Internals*, *Effective Java*, *Building Microservices*) into the knowledge base.

## Workflow

### 1. Metadata & Thesis Capture
- Thu thập metadata chính xác: Tên sách (English title), Tác giả, Năm xuất bản, Ấn bản (Edition), ISBN.
- Định hình Luận điểm cốt lõi (Core Thesis): Cuốn sách này giải quyết những thách thức kiến trúc nền tảng nào trong kỹ thuật phần mềm?

### 2. Architectural Concepts & Mental Models
- Không chép lại toàn bộ văn bản hoặc tóm tắt sơ sài từng chương theo mục lục.
- Tổng hợp theo **mô hình tư duy (Mental Models)** và **nguyên lý thiết kế**:
  - Consensus & Replication algorithms (Raft, Paxos, Quorum).
  - Storage Engines (LSM-Tree vs B-Tree).
  - Transaction Isolation Levels & Anomaly phenomena (Dirty Read, Non-repeatable Read, Phantom, Write Skew).
  - CAP & PACELC Theorem trong thực tế.

### 3. Production Mapping
- Ánh xạ trực tiếp từ lý thuyết trong sách sang các công nghệ đang có trong knowledge base:
  - B-Tree/WAL trong sách -> Cách PostgreSQL hiện thực hóa `Shared Buffers`, `WAL Writer`, `Autovacuum`.
  - Isolation levels trong sách -> Mức `Read Committed` mặc định và `Serializable Snapshot Isolation (SSI)` của PostgreSQL.
  - Concurrency models -> Virtual Threads và ReentrantLock trong Java.
  - Event-driven patterns -> AWS SNS, SQS, Kinesis và Spring Cloud Stream.

### 4. Drafting the Document & Best Practice Candidates
- Sử dụng template tại `templates/book-note-template.md`.
- Trình bày dạng bảng so sánh (Comparison tables), sơ đồ Mermaid biểu diễn dòng thông tin, và ghi chú cảnh báo (Admonitions).
- **Trích xuất ứng viên Best Practice (`Candidate`)**: Nhận diện các nguyên lý hoặc mẫu kiến trúc kinh điển có tiềm năng tái sử dụng. Không tự động phong mọi lời khuyên trong sách thành chuẩn mực sản xuất phổ quát nếu chưa đối chiếu phiên bản công nghệ hiện tại; chuyển các đề xuất sang **`manage-best-practices`** với Evidence Level `[Candidate]`.
- Giữ nguyên thuật ngữ tiếng Anh gốc của tác giả để tiện tra cứu tài liệu chuyên sâu.

### 5. Verification & Strict Build
- Đảm bảo trích dẫn chính xác chương, thuật ngữ gốc của sách.
- Chạy kiểm tra:
  ```powershell
  python -m mkdocs build --strict
  ```
