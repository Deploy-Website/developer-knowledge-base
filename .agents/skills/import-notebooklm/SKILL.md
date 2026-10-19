---
name: import-notebooklm
description: Transform NotebookLM research notes into verified, non-duplicated technical documentation and practical labs for an existing MkDocs knowledge base.
---

# NotebookLM Knowledge Integration

## Input

Receive a Markdown file exported or copied from NotebookLM.

The input is research material, NOT verified truth.

## Step 1: Analyze

- Identify important concepts and learning objectives.
- Extract the book title, edition, chapter and section.
- Preserve source references when available.
- Identify unsupported or ambiguous claims.

## Step 2: Verify

- Research applicable official documentation.
- Check PostgreSQL version compatibility.
- Distinguish book claims from current behavior.
- Never invent technical facts or references.

## Step 3: Check Existing Knowledge

Search the MkDocs repository.

For each concept, decide whether to:

- Update an existing page
- Create a new page
- Add a cross-reference
- Skip duplicated or low-value content

## Step 4: Generate Documentation

Create or update:

- Book Note: key lessons from the source material.
- Knowledge Note: reusable explanations and concepts.
- Best Practice: delegate reusable, validated recommendations to **`manage-best-practices`** (tag unverified claims as `[Candidate]`).
- Hands-on Lab: only when practical testing adds value.
- Review Questions: 3–5 questions for active recall.

## Step 5: Validate

- Verify Markdown links and citations.
- Run tests for executable examples when possible.
- Run mkdocs build --strict.
- Report new files, changed files and unverified claims.

## Constraints

- Write in Vietnamese, preserving English technical terms.
- Do not republish long copyrighted book passages.
- Do not invent execution or benchmark results.
- Do not overwrite unrelated existing knowledge.
- Do not deploy without approval.
