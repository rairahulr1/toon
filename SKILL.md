---
name: toon
description: "Token-Oriented Object Notation (TOON) & Semantic HTML standard. Slashes token consumption by 55-80% compared to JSON/HTML for datasets, tables, and trackers, paired with zero-build semantic HTML browser rendering."
---

# `toon` — Token-Oriented Object Notation & Semantic HTML Skill

TOON is a minimal, token-efficient data notation engineered specifically for AI agents, multi-agent systems, and developer documentation. It eliminates repetitive delimiters, structural tag bloat, and column drift, reducing LLM context window consumption by **55–80%** compared to JSON and raw HTML, while pairing seamlessly with **zero-build Semantic HTML5** browser rendering via `toon-renderer.js`.

---

## 1. Syntax Specification

```toon
metadata:
  title: Production Cluster Overview
  as_of: 2026-10-16
  owner: Infrastructure Lead

services[3]{name,runtime,db,p99_ms,tier}:
  auth-gateway,Go 1.22,Redis 7.2,14,Critical
  billing-ledger,Laravel 11,PostgreSQL 16,38,Critical
  event-indexer,Node.js 20,ClickHouse,45,Standard

checklist[3]:
  - P99 latency above 100ms triggers autoscaling.
  - Double-entry ledger state machine verification required.
  - Zero unencrypted inter-service traffic.

notes:
  Indented narrative text or markdown-style descriptive paragraphs.
```

### Syntax Grammar
1. **Tabular Records**:
   - Header: `name[count]{col1,col2,...}:`
   - Explicit row count `[count]` guarantees validation and prevents truncation hallucinations.
   - Column names defined once in `{...}`.
   - Rows are indented with 2 spaces and comma-delimited.
   - Cells containing commas must use semicolons (`;`) or quotation marks.
2. **Lists**:
   - Header: `name[count]:`
   - Items indented with 2 spaces and prefixed with `- `.
3. **Key-Value Metadata**:
   - Indented `key: value` pairs under a root `metadata:` block.
4. **Text / Notes**:
   - Header: `name:`
   - Freeform indented text or markdown paragraphs.

---

## 2. Dual-Mode Architecture

TOON combines lean AI model context consumption with rich, responsive human viewing:

```
               ┌───────────────────────────────┐
               │         document.md           │
               │   (Contains ```toon``` block) │
               └───────────────┬───────────────┘
                               │
                toon sync      ▼
               ┌───────────────────────────────┐
               │        document.html          │
               │   (Semantic HTML5 container   │
               │    + <script type="text/toon">│
               └───────────────┬───────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
   [ Browser User View ]               [ AI Model Ingestion ]
   - Semantic HTML layout              - Extracts only ```toon```
   - Responsive cards & tables         - 55-80% token reduction
   - Zero-build client rendering       - Zero parsing hallucinations
   - Modern accessible styling         - Maximum reasoning context
```

---

## 3. Agent Operational Protocols

### Protocol A: Ingesting Context (Reading)
- **Never parse raw HTML tags for data**: When reading companion `.html` files or documentation, extract strictly the `<script id="data" type="text/toon">` payload or the ````toon ```` block in `.md`.
- **Ignore layout boilerplate**: Discard UI markup, navigational wrappers, and styles to keep your context window lean.

### Protocol B: Generating New Documents
1. Draft `filename.md` following the standard template:
   ```markdown
   # Document Title

   > **Browser Viewable HTML:** [`filename.html`](filename.html)
   > **as_of:** YYYY-MM-DD
   > **owner:** Name

   ---

   ## TOON Specification (Token-Oriented Object Notation)

   ```toon
   [TOON DATA]
   ```
   ```
2. Run `toon sync filename.md` to automatically generate the companion `filename.html`.
3. Validate syntax using `toon validate filename.md`.

### Protocol C: Modifying Existing Files
1. Edit the ````toon```` block in `.md` directly.
2. Run `toon format filename.md` to recompute array row counts `[N]`.
3. Run `toon sync filename.md` to reflect changes in `filename.html`.

---

## 4. Semantic HTML Requirement

When generating or styling companion HTML views:
- **Semantic Structure**: Always use semantic HTML5 elements (`<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>`, `<figure>`, `<figcaption>`, `<time>`, `<data>`) rather than unsemantic `<div>`/`<span>` containers.
- **Client Rendering**: Link `toon-renderer.js` and `style.css` for instant client-side rendering with dark/light theme support.

---

## 5. CLI Tooling Reference

```bash
# Validate syntax and row count integrity
toon validate <file.md|file.html>

# Automatically recount rows and format blocks
toon format <file.md|file.html>

# Generate / update companion HTML view
toon sync <file.md>
```
