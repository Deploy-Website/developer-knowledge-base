#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
import_notes.py - TXT Notes Importer for Developer Knowledge Base

Automates importing technical notes from `nodes/*.txt` into structured MkDocs
documentation under `docs/<domain>/<category>/<slug>.md`, updating `mkdocs.yml`
navigation, and tracking idempotency via `nodes/.import-manifest.json`.
"""

import os
import sys
import re
import json
import hashlib
import unicodedata
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# Safe console output encoding for Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parents[4]
NODES_DIR = REPO_ROOT / "nodes"
DOCS_DIR = REPO_ROOT / "docs"
MKDOCS_YML = REPO_ROOT / "mkdocs.yml"
MANIFEST_FILE = NODES_DIR / ".import-manifest.json"

# Supported type mappings
TYPE_MAPPING = {
    "best practice": ("Best Practice", "best-practices"),
    "best practices": ("Best Practice", "best-practices"),
    "best-practice": ("Best Practice", "best-practices"),
    "best-practices": ("Best Practice", "best-practices"),
    "thực hành": ("Best Practice", "best-practices"),
    "concept": ("Concept", "concepts"),
    "concepts": ("Concept", "concepts"),
    "khái niệm": ("Concept", "concepts"),
    "how-to": ("How-to", "how-to"),
    "howto": ("How-to", "how-to"),
    "how to": ("How-to", "how-to"),
    "hướng dẫn": ("How-to", "how-to"),
    "investigation": ("Investigation", "investigations"),
    "investigations": ("Investigation", "investigations"),
    "điều tra": ("Investigation", "investigations"),
    "troubleshooting": ("Troubleshooting", "troubleshooting"),
    "troubleshoot": ("Troubleshooting", "troubleshooting"),
    "sự cố": ("Troubleshooting", "troubleshooting"),
    "lab": ("Lab", "labs"),
    "labs": ("Lab", "labs"),
    "hands-on lab": ("Lab", "labs"),
    "hands on lab": ("Lab", "labs"),
    "recipe": ("Recipe", "recipes"),
    "recipes": ("Recipe", "recipes"),
    "code recipe": ("Recipe", "recipes"),
    "sql recipe": ("Recipe", "recipes"),
}

# Supported domain mappings
DOMAIN_MAPPING = {
    "postgresql": ("PostgreSQL", "postgresql"),
    "postgres": ("PostgreSQL", "postgresql"),
    "pg": ("PostgreSQL", "postgresql"),
    "java": ("Java", "java"),
    "openjdk": ("Java", "java"),
    "jvm": ("Java", "java"),
    "spring boot": ("Spring Boot", "spring-boot"),
    "spring-boot": ("Spring Boot", "spring-boot"),
    "spring": ("Spring Boot", "spring-boot"),
    "aws": ("AWS", "aws"),
    "amazon web services": ("AWS", "aws"),
    "system design": ("System Design", "system-design"),
    "system-design": ("System Design", "system-design"),
    "distributed systems": ("System Design", "system-design"),
}

def remove_accents(input_str: str) -> str:
    """Removes Vietnamese accents for clean URL slugs."""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def slugify(text: str) -> str:
    """Generates a clean URL-friendly slug."""
    text = remove_accents(text).lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text).strip('-')
    return text

def calculate_sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def load_manifest() -> dict:
    if MANIFEST_FILE.exists():
        try:
            with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARN] Could not read manifest: {e}. Starting fresh.")
    return {"version": "1.0", "imports": {}}

def save_manifest(manifest: dict):
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

def read_file_safely(filepath: Path) -> str:
    encodings = ["utf-8-sig", "utf-8", "latin-1", "cp1252"]
    for enc in encodings:
        try:
            with open(filepath, "r", encoding=enc) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Could not decode {filepath} with any supported encoding.")

def parse_txt_file(filepath: Path) -> dict:
    """Parses Item, Type, Domain, and Content from TXT note."""
    raw_text = read_file_safely(filepath)
    lines = raw_text.splitlines()

    item = None
    doc_type = None
    domain = None
    content_lines = []
    in_content = False

    for line in lines:
        if not in_content:
            stripped = line.strip()
            item_match = re.match(r"^Item:\s*(.+)$", stripped, re.IGNORECASE)
            type_match = re.match(r"^Type:\s*(.+)$", stripped, re.IGNORECASE)
            domain_match = re.match(r"^Domain:\s*(.+)$", stripped, re.IGNORECASE)
            content_match = re.match(r"^Content:\s*(.*)$", stripped, re.IGNORECASE)

            if item_match:
                item = item_match.group(1).strip()
            elif type_match:
                doc_type = type_match.group(1).strip()
            elif domain_match:
                domain = domain_match.group(1).strip()
            elif content_match:
                in_content = True
                rem = content_match.group(1)
                if rem:
                    content_lines.append(rem)
        else:
            content_lines.append(line)

    content = "\n".join(content_lines).strip()

    if not item:
        raise ValueError(f"Missing required field 'Item:' in {filepath}")
    if not doc_type:
        raise ValueError(f"Missing required field 'Type:' in {filepath}")
    if not content:
        raise ValueError(f"Missing content after 'Content:' in {filepath}")

    # Normalize Type
    type_key = doc_type.lower().strip()
    if type_key not in TYPE_MAPPING:
        raise ValueError(f"Unsupported Type '{doc_type}' in {filepath}. Allowed: {list(set([v[0] for v in TYPE_MAPPING.values()]))}")
    canonical_type, type_folder = TYPE_MAPPING[type_key]

    # Normalize Domain
    canonical_domain = None
    domain_folder = None
    if domain:
        domain_key = domain.lower().strip()
        if domain_key in DOMAIN_MAPPING:
            canonical_domain, domain_folder = DOMAIN_MAPPING[domain_key]
        else:
            raise ValueError(f"Unknown Domain '{domain}' in {filepath}. Please specify one of: PostgreSQL, Java, Spring Boot, AWS, System Design.")
    else:
        # Infer domain from content & item
        combined_text = (item + "\n" + content).lower()
        matched_domains = []
        if "postgres" in combined_text or "psql" in combined_text or "jsonb" in combined_text or "wal" in combined_text:
            matched_domains.append(("PostgreSQL", "postgresql"))
        if "spring" in combined_text or "webclient" in combined_text or "hikari" in combined_text:
            matched_domains.append(("Spring Boot", "spring-boot"))
        elif "java" in combined_text or "jvm" in combined_text or "virtual thread" in combined_text:
            matched_domains.append(("Java", "java"))
        if "aws" in combined_text or "aurora" in combined_text or "s3" in combined_text or "dynamodb" in combined_text:
            matched_domains.append(("AWS", "aws"))
        if "system design" in combined_text or "distributed" in combined_text or "idempotency" in combined_text:
            matched_domains.append(("System Design", "system-design"))

        if len(matched_domains) == 1:
            canonical_domain, domain_folder = matched_domains[0]
            print(f"[INFO] Inferred domain '{canonical_domain}' for {filepath.name}")
        else:
            raise ValueError(f"Domain is missing and could not be unambiguously inferred for {filepath.name}. Ambiguity matches: {[d[0] for d in matched_domains]}")

    return {
        "item": item,
        "type": canonical_type,
        "type_folder": type_folder,
        "domain": canonical_domain,
        "domain_folder": domain_folder,
        "content": content,
        "source_hash": calculate_sha256(raw_text),
        "raw_text": raw_text
    }

def format_markdown(parsed: dict, rel_source_path: str) -> str:
    """Converts parsed note into high-quality structured Markdown according to Type."""
    item = parsed["item"]
    doc_type = parsed["type"]
    domain = parsed["domain"]
    content = parsed["content"]
    now_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Frontmatter + Title & Metadata Header
    md_header = f"""---
title: "{item}"
domain: "{domain}"
type: "{doc_type}"
source_note: "{rel_source_path}"
imported_at: "{now_date}"
---

# {item}

> **Lĩnh vực (Domain)**: {domain}  
> **Phân loại (Type)**: {doc_type}  
> **Tài liệu nguồn (Source)**: `{rel_source_path}`  
> **Ngày nhập (Import Date)**: {now_date}  

---
"""

    # Format body sections according to Type specifications
    if doc_type == "Best Practice":
        body = f"""
## 1. Summary (Tóm Tắt Khuyến Nghị)

> [!NOTE]
> **Executive Summary**:  
> {item} — Khuyến nghị chuẩn mực sản xuất nhằm tối ưu hóa hiệu năng, độ tin cậy và bảo vệ tài nguyên trong môi trường {domain}.

---

## 2. Problem / Context (Bối Cảnh & Vấn Đề Giải Quyết)

Mô tả bài toán kỹ thuật và các triệu chứng gặp phải trong môi trường thực tế:

{content}

---

## 3. Recommended Approach (Giải Pháp Khuyến Nghị)

Các giải pháp chuẩn mực được khuyến nghị áp dụng:
- Thiết lập cấu hình và mẫu thiết kế chuẩn theo tài liệu chính thức.
- Tuân thủ các nguyên tắc thiết kế phòng vệ và tối ưu tài nguyên.

---

## 4. Why It Works (Nguyên Lý & Cơ Chế Kỹ Thuật)

Giải thích cơ chế hoạt động bên dưới (Under the hood):
- Tối ưu hóa việc phân bổ bộ nhớ và luồng thực thi trong runtime.
- Giảm thiểu tranh chấp tài nguyên (Resource contention) và độ trễ phản hồi (P99 latency).

---

## 5. Implementation (Hướng Dẫn Triển Khai Thực Tế)

Áp dụng các cấu hình hoặc đoạn mã đã kiểm chứng ở trên vào dự án thực tế. Luôn thử nghiệm trên môi trường Staging trước khi triển khai Production.

---

## 6. When to Use (Ngữ Cảnh Áp Dụng)

- Áp dụng khi gặp các điều kiện tải hoặc quy mô dữ liệu tương ứng.
- Phù hợp với các hệ thống yêu cầu tính sẵn sàng và khả năng chịu tải cao.

---

## 7. When Not to Use (Chống Chỉ Định & Anti-patterns)

> [!WARNING]
> Không áp dụng khuyến nghị này một cách rập khuôn nếu kích thước tải quá nhỏ hoặc không phù hợp với giả định kiến trúc ban đầu.

---

## 8. Trade-offs (Đánh Đổi Kỹ Thuật)

| Khía cạnh | Lợi ích đạt được | Chi phí / Đánh đổi |
| :--- | :--- | :--- |
| **Hiệu năng (Performance)** | Tối ưu độ trễ, tăng Throughput | Chi phí CPU / RAM bổ sung nếu cấu hình sai |
| **Vận hành (Operations)** | Hệ thống ổn định, tự phục hồi | Cần giám sát bổ sung qua Telemetry |

---

## 9. Validation & References

- **Kiểm chứng**: Kiểm tra kế hoạch thực thi, log metric hoặc benchmark sau khi áp dụng.
- **Tài liệu chính thức**: Tham chiếu documentation chính thức của {domain}.
"""
    elif doc_type == "How-to":
        body = f"""
## 1. Goal (Mục Tiêu)

Hướng dẫn từng bước thực hiện **{item}** trong môi trường {domain}.

---

## 2. Prerequisites (Điều Kiện Tiên Quyết)

- Phiên bản môi trường tương thích ({domain}).
- Quyền truy cập hoặc công cụ CLI / IDE cần thiết.

---

## 3. Step-by-step Instructions (Hướng Dẫn Chi Tiết)

{content}

---

## 4. Verification (Kiểm Chứng Kết Quả)

- Kiểm tra trạng thái dịch vụ hoặc thực thi lệnh xác nhận kết quả.
- Đảm bảo các chỉ số hoạt động ổn định và không phát sinh lỗi bất thường.

---

## 5. Troubleshooting (Xử Lý Sự Cố Thường Gặp)

- Nếu gặp lỗi kết nối hoặc quyền hạn, kiểm tra lại cấu hình mạng và thông số môi trường.

---

## 6. References (Tài Liệu Tham Khảo)

- Tham chiếu tài liệu chính thức của {domain}.
"""
    elif doc_type == "Concept":
        body = f"""
## 1. Overview (Tổng Quan)

{content}

---

## 2. Why It Matters (Ý Nghĩa Kiến Trúc)

Hiểu rõ cơ chế này giúp kỹ sư đưa ra các quyết định kiến trúc chính xác và phòng tránh các lỗi tiềm ẩn trong vận hành.

---

## 3. How It Works (Cơ Chế Hoạt Động Bên Dưới)

Giải thích chi tiết luồng xử lý và cách engine tương tác với hệ thống.

---

## 4. Common Misconceptions (Các Hiểu Lầm Phổ Biến)

- Không nên nhầm lẫn giữa cơ chế này với các khái niệm tương đồng trong hệ thống khác.

---

## 5. Key Takeaways (Đúc Kết Cốt Lõi)

- Nắm vững bản chất kỹ thuật thay vì ghi nhớ máy móc cú pháp.
- Luôn kiểm chứng với tài liệu chính thức của {domain}.
"""
    elif doc_type == "Investigation":
        body = f"""
## 1. Problem Statement (Mô Tả Sự Cố)

{content}

---

## 2. Chronological Investigation Steps (Tiến Trình Điều Tra)

Ghi nhận các bước thực nghiệm, giả thuyết đã đặt ra và kết quả quan sát thực tế.

---

## 3. Final Resolution (Giải Pháp Chốt Hạ)

Kết luận nguyên nhân gốc rễ và giải pháp triệt để đã được kiểm chứng.

---

## 4. Lessons Learned (Bài Học Rút Ra)

- Bảo tồn lịch sử thử nghiệm để tránh lặp lại sai lầm.
"""
    elif doc_type == "Troubleshooting":
        body = f"""
## 1. Symptoms (Triệu Chứng Sự Cố)

{content}

---

## 2. Diagnostic Steps (Các Bước Chẩn Đoán)

- Thu thập log, execution plan hoặc thread dump để xác định điểm nghẽn.

---

## 3. Root Cause & Resolution (Nguyên Nhân & Cách Khắc Phục)

- Nguyên nhân gốc rễ đã được xác minh.
- Các bước khắc phục sự cố an toàn trên production.

---

## 4. Prevention (Biện Pháp Phòng Ngừa)

- Thiết lập cảnh báo và quy chuẩn kiểm tra định kỳ.
"""
    elif doc_type == "Lab":
        body = f"""
## 1. Learning Objective (Mục Tiêu Thí Nghiệm)

Thực nghiệm đo lường và kiểm chứng: **{item}**.

---

## 2. Environment & Setup (Môi Trường Thử Nghiệm)

{content}

---

## 3. Cleanup & Lessons Learned

- Thu dọn tài nguyên môi trường sau khi hoàn tất benchmark.
"""
    elif doc_type == "Recipe":
        body = f"""
## 1. Purpose (Mục Đích Sử Dụng)

Đoạn mã hoặc câu lệnh truy vấn mẫu chuẩn cho **{item}**.

---

## 2. Ready-to-use Command / Code (Mã Nguồn Thực Thi)

{content}

---

## 3. Parameters & Explanation (Giải Thích Tham Số)

- Chú thích chi tiết các tham số quan trọng và lưu ý an toàn.
"""
    else:
        body = f"\n{content}\n"

    return md_header + body

def update_mkdocs_navigation(domain: str, doc_type: str, item_title: str, rel_doc_path: str) -> bool:
    """
    Safely updates mkdocs.yml navigation with exact Item title and target path.
    Preserves all comments, formatting, and prevents duplicate menu entries.
    """
    with open(MKDOCS_YML, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()

    # Category display name in nav
    category_label = doc_type
    if doc_type == "Best Practice":
        category_label = "Best Practices"
    elif doc_type == "Concept":
        category_label = "Concepts"
    elif doc_type == "How-to":
        category_label = "How-to"
    elif doc_type == "Investigation":
        category_label = "Investigations"
    elif doc_type == "Troubleshooting":
        category_label = "Troubleshooting"
    elif doc_type == "Lab":
        category_label = "Labs"
    elif doc_type == "Recipe":
        category_label = "Recipes"

    # Normalize paths for comparison (forward slashes)
    rel_doc_path = rel_doc_path.replace("\\", "/")

    # Check if this exact target file is already registered in mkdocs.yml
    if rel_doc_path in content:
        # Check if item title also matches
        escaped_title = re.escape(item_title)
        if re.search(rf'"{escaped_title}":\s*{re.escape(rel_doc_path)}', content) or \
           re.search(rf'{escaped_title}:\s*{re.escape(rel_doc_path)}', content):
            print(f"[INFO] Navigation entry already exists for '{item_title}'. Skipping nav update.")
            return True

    # Find the domain section in nav
    domain_pattern = re.compile(rf"^(\s*)-\s+{re.escape(domain)}:\s*$", re.MULTILINE)
    match = domain_pattern.search(content)
    if not match:
        print(f"[ERROR] Could not find Domain '{domain}:' in mkdocs.yml nav.")
        return False

    domain_indent = match.group(1)
    sub_indent = domain_indent + "    "
    item_indent = sub_indent + "    "

    # Find where this domain block ends (next item at domain_indent level or end of nav)
    start_pos = match.end()
    lines_after = content[start_pos:].splitlines()

    domain_end_line_idx = len(lines_after)
    for idx, l in enumerate(lines_after):
        if idx > 0 and re.match(rf"^{domain_indent}-\s+\S+", l):
            domain_end_line_idx = idx
            break

    domain_block = "\n".join(lines_after[:domain_end_line_idx])

    # Check if category_label exists in this domain block
    cat_pattern = re.compile(rf"^(\s*)-\s+{re.escape(category_label)}:\s*$", re.MULTILINE)
    cat_match = cat_pattern.search(domain_block)

    new_entry_line = f'{item_indent}- "{item_title}": {rel_doc_path}'

    if cat_match:
        # Find category block inside domain block
        cat_start = cat_match.end()
        cat_indent = cat_match.group(1)
        cat_lines_after = domain_block[cat_start:].splitlines()

        cat_insert_idx = len(cat_lines_after)
        for c_idx, cl in enumerate(cat_lines_after):
            if c_idx > 0 and re.match(rf"^{cat_indent}-\s+\S+", cl):
                cat_insert_idx = c_idx
                break

        # Check if entry with same path or title already exists in category
        sub_block = "\n".join(cat_lines_after[:cat_insert_idx])
        if rel_doc_path in sub_block:
            print(f"[INFO] Path '{rel_doc_path}' already exists under '{category_label}'. Skipping.")
            return True

        # Insert at the end of category block
        abs_insert_line = len(content[:start_pos].splitlines()) + cat_match.start()
        # Find actual line number in original lines
        orig_cat_line = 0
        cat_found = False
        in_domain = False
        for l_num, l_text in enumerate(lines):
            if re.match(rf"^{domain_indent}-\s+{re.escape(domain)}:\s*$", l_text):
                in_domain = True
            elif in_domain and re.match(rf"^{domain_indent}-\s+\S+", l_text):
                in_domain = False
            elif in_domain and re.match(rf"^{re.escape(cat_indent)}-\s+{re.escape(category_label)}:\s*$", l_text):
                orig_cat_line = l_num
                cat_found = True
                break

        if cat_found:
            # Find the end of this category
            insert_at = orig_cat_line + 1
            while insert_at < len(lines):
                next_l = lines[insert_at]
                if next_l.strip() == "" or next_l.startswith(item_indent):
                    insert_at += 1
                else:
                    break
            lines.insert(insert_at, new_entry_line)
    else:
        # Category doesn't exist yet, insert new category block at end of domain
        orig_domain_line = 0
        for l_num, l_text in enumerate(lines):
            if re.match(rf"^{domain_indent}-\s+{re.escape(domain)}:\s*$", l_text):
                orig_domain_line = l_num
                break

        insert_at = orig_domain_line + 1
        while insert_at < len(lines):
            next_l = lines[insert_at]
            if next_l.startswith(sub_indent) or next_l.startswith(item_indent) or next_l.strip() == "":
                insert_at += 1
            else:
                break

        new_cat_block = [
            f"{sub_indent}- {category_label}:",
            new_entry_line
        ]
        for offset, cl in enumerate(new_cat_block):
            lines.insert(insert_at + offset, cl)

    with open(MKDOCS_YML, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"[SUCCESS] Updated mkdocs.yml navigation with: {item_title} -> {rel_doc_path}")
    return True

def import_single_note(note_path: Path, force: bool = False, dry_run: bool = False) -> dict:
    """Imports a single TXT note file."""
    rel_path = note_path.relative_to(REPO_ROOT).as_posix()
    print(f"\n--- Processing: {rel_path} ---")

    try:
        parsed = parse_txt_file(note_path)
    except Exception as e:
        print(f"[FAILED] Validation error in {rel_path}: {e}")
        return {"status": "FAILED", "file": rel_path, "error": str(e)}

    item = parsed["item"]
    doc_type = parsed["type"]
    type_folder = parsed["type_folder"]
    domain = parsed["domain"]
    domain_folder = parsed["domain_folder"]
    source_hash = parsed["source_hash"]

    # Target file path
    slug = slugify(item)
    dest_dir = DOCS_DIR / domain_folder / type_folder
    dest_file = dest_dir / f"{slug}.md"
    rel_dest_path = dest_file.relative_to(DOCS_DIR).as_posix()

    # Check manifest for idempotency
    manifest = load_manifest()
    entry = manifest.get("imports", {}).get(rel_path)

    if entry and not force:
        if entry.get("source_hash") == source_hash and dest_file.exists():
            print(f"[SKIPPED] Note {rel_path} is already imported and unchanged (Hash: {source_hash[:8]}).")
            return {
                "status": "SKIPPED",
                "file": rel_path,
                "item": item,
                "dest": rel_dest_path,
                "reason": "Idempotent - identical content already imported"
            }

    # Check collision: if destination file exists but was not created from this source
    if dest_file.exists() and not force:
        existing_content = read_file_safely(dest_file)
        if f'source_note: "{rel_path}"' not in existing_content and f'source_note: {rel_path}' not in existing_content:
            print(f"[CONFLICT] Destination file {rel_dest_path} exists and belongs to a different source. Preserving existing file.")
            return {
                "status": "CONFLICT",
                "file": rel_path,
                "item": item,
                "dest": rel_dest_path,
                "reason": f"Destination file {rel_dest_path} already exists and does not match source {rel_path}"
            }

    # Format Markdown
    md_content = format_markdown(parsed, rel_path)

    if dry_run:
        print(f"[DRY-RUN] Would write {len(md_content)} bytes to {rel_dest_path}")
        print(f"[DRY-RUN] Would update navigation: Domain={domain}, Type={doc_type}, Label='{item}'")
        return {
            "status": "DRY_RUN",
            "file": rel_path,
            "item": item,
            "dest": rel_dest_path
        }

    # Write Markdown file
    dest_dir.mkdir(parents=True, exist_ok=True)
    with open(dest_file, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[CREATED/UPDATED] Wrote {dest_file}")

    # Update MkDocs navigation
    nav_ok = update_mkdocs_navigation(domain, doc_type, item, rel_dest_path)
    if not nav_ok:
        print(f"[WARN] Navigation update failed or needs manual review for {rel_dest_path}")

    # Update manifest
    manifest.setdefault("imports", {})[rel_path] = {
        "item": item,
        "type": doc_type,
        "domain": domain,
        "destination": rel_dest_path,
        "source_hash": source_hash,
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "status": "imported"
    }
    save_manifest(manifest)

    return {
        "status": "SUCCESS",
        "file": rel_path,
        "item": item,
        "dest": rel_dest_path
    }

def batch_import(force: bool = False, dry_run: bool = False) -> list:
    """Processes all TXT files in nodes/ directory."""
    if not NODES_DIR.exists():
        print(f"[ERROR] Directory {NODES_DIR} does not exist.")
        return []

    txt_files = sorted([f for f in NODES_DIR.glob("*.txt") if not f.name.startswith(".")])
    if not txt_files:
        print(f"[INFO] No .txt files found in {NODES_DIR}.")
        return []

    print(f"[INFO] Found {len(txt_files)} TXT files in {NODES_DIR}. Starting batch import...")
    results = []

    for f in txt_files:
        res = import_single_note(f, force=force, dry_run=dry_run)
        results.append(res)

    # Print summary report
    print("\n" + "=" * 50)
    print("IMPORT SUMMARY REPORT")
    print("=" * 50)
    created = [r for r in results if r["status"] == "SUCCESS"]
    skipped = [r for r in results if r["status"] == "SKIPPED"]
    conflicts = [r for r in results if r["status"] == "CONFLICT"]
    failed = [r for r in results if r["status"] == "FAILED"]

    print(f"Total processed : {len(results)}")
    print(f"Successfully imported : {len(created)}")
    print(f"Skipped (unchanged)   : {len(skipped)}")
    print(f"Conflicts detected    : {len(conflicts)}")
    print(f"Failed files          : {len(failed)}")

    if failed:
        print("\nFailed Items:")
        for f_item in failed:
            print(f"  - {f_item['file']}: {f_item.get('error')}")

    if conflicts:
        print("\nConflicted Items:")
        for c_item in conflicts:
            print(f"  - {c_item['file']}: {c_item.get('reason')}")

    return results

def run_mkdocs_validation():
    """Runs mkdocs build --strict to validate site integrity."""
    print("\n[VALIDATION] Running 'python -m mkdocs build --strict'...")
    try:
        proc = subprocess.run(
            ["python", "-m", "mkdocs", "build", "--strict"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True
        )
        print("[VALIDATION PASSED] MkDocs strict build succeeded with exit code 0.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[VALIDATION FAILED] Exit code {e.returncode}")
        print("STDOUT:\n", e.stdout)
        print("STDERR:\n", e.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Import TXT technical notes into MkDocs knowledge base.")
    parser.add_argument("--file", "-f", type=str, help="Path to single TXT note to import")
    parser.add_argument("--batch", "-b", action="store_true", help="Import all TXT notes under nodes/")
    parser.add_argument("--force", action="store_true", help="Force re-import even if content hash is unchanged")
    parser.add_argument("--dry-run", action="store_true", help="Simulate import without writing files")
    parser.add_argument("--validate", "-v", action="store_true", help="Run 'mkdocs build --strict' after importing")
    parser.add_argument("--report", action="store_true", help="Show current import manifest status")

    args = parser.parse_args()

    if args.report:
        manifest = load_manifest()
        imports = manifest.get("imports", {})
        print(f"\nImport Manifest ({len(imports)} items recorded):")
        for src, data in imports.items():
            print(f"  • {src} -> {data.get('destination')} [{data.get('type')}] ({data.get('imported_at')[:10]})")
        return

    if args.file:
        note_path = Path(args.file)
        if not note_path.is_absolute():
            note_path = REPO_ROOT / note_path
        if not note_path.exists():
            print(f"[ERROR] File {note_path} not found.")
            sys.exit(1)
        res = import_single_note(note_path, force=args.force, dry_run=args.dry_run)
        if args.validate and res["status"] in ["SUCCESS", "SKIPPED"]:
            run_mkdocs_validation()
    elif args.batch:
        results = batch_import(force=args.force, dry_run=args.dry_run)
        if args.validate and any(r["status"] == "SUCCESS" for r in results):
            run_mkdocs_validation()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
