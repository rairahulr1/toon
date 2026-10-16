# TOON — Token-Oriented Object Notation

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Zero Build](https://img.shields.io/badge/Build-Zero%20Dependency-brightgreen.svg)]()
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-Compatible-purple.svg)](SKILL.md)
[![Token Savings](https://img.shields.io/badge/Token%20Reduction-67%25%20vs%20HTML-orange.svg)](#benchmarks)

> **Minimal, token-efficient data notation for AI agents, paired with zero-build Semantic HTML5 rendering.**

---

## 💡 Why TOON?

Modern AI agents and developer workflows suffer from a data representation dilemma:
- **Markdown Tables** consume extra tokens with column padding, pipe delimiters (`|---|---|`), and cause alignment hallucinations during model generation.
- **JSON** repeats key names on every row, blowing up LLM context windows with punctuation and whitespace.
- **Semantic HTML** provides accessibility and browser presentation, but costs **3x more tokens** when passed to an LLM.

**TOON (Token-Oriented Object Notation)** solves this by introducing a **dual-mode architecture**:
1. **For the AI**: A hyper-dense, schema-first notation with explicit counts (`services[20]{name,mesh,runtime}:`) that prevents hallucinated row counts and cuts context size by **55–70%**.
2. **For the Human**: A companion **Semantic HTML5** view (`document.html`) that parses the TOON data directly in the browser via `toon-renderer.js` with zero build tools, bundlers, or static site generators.

---

## 📊 Side-by-Side Comparison

Here is how the exact same 20-service microservices architecture dataset is represented across formats:

### 1. Pure XML (`1,858 tokens` — 2.94x larger)
```xml
<services>
  <service>
    <name>auth-gateway</name>
    <service_mesh>Istio</service_mesh>
    <runtime>Go 1.22</runtime>
    <database>Redis 7.2</database>
    <p99_latency_ms>14</p99_latency_ms>
    <uptime_pct>99.99</uptime_pct>
    <tier>Critical</tier>
  </service>
  <!-- Repeated 20 times -->
</services>
```
*Disadvantage*: XML provides clean semantic tags, but repetitive opening and closing tags blow up token count by nearly 300%.

### 2. Semantic HTML (`1,911 tokens` — 3.03x larger)
```html
<section>
  <h2>Services</h2>
  <table>
    <thead><tr><th scope="col">Name</th>...</tr></thead>
    <tbody>
      <tr><td>auth-gateway</td><td>Istio</td>...</tr>
    </tbody>
  </table>
</section>
```
*Disadvantage*: Massive token consumption; repetitive `<tr>`, `<td>`, and attribute boilerplate waste context.

### 3. Indented JSON (`1,473 tokens` — 2.33x larger)
```json
{
  "services": [
    {
      "name": "auth-gateway",
      "service_mesh": "Istio",
      "runtime": "Go 1.22",
      "database": "Redis 7.2",
      "p99_latency_ms": 14,
      "uptime_pct": 99.99,
      "tier": "Critical"
    }
  ]
}
```
*Disadvantage*: Repetitive keys on every object consume tokens; deep nested brackets clutter context.

### 4. Markdown Table (`696 tokens`)
```markdown
| Name | Service Mesh | Runtime | Database | P99 Latency (ms) | Uptime (%) | Tier |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| auth-gateway | Istio | Go 1.22 | Redis 7.2 | 14 | 99.99 | Critical |
| ... | ... | ... | ... | ... | ... | ... |
```
*Disadvantage*: Pipe delimiters and whitespace padding consume tokens; large tables routinely cause delimiter misalignment.

### 5. TOON (`631 tokens` — Baseline 1.0x)
```toon
services[20]{name,service_mesh,runtime,database,p99_latency_ms,uptime_pct,tier}:
  auth-gateway,Istio,Go 1.22,Redis 7.2,14,99.99,Critical
  billing-ledger,Linkerd,PHP 8.3 Laravel,PostgreSQL 16,38,99.95,Critical
  ...
```
*Advantage*: Schema declared once; explicit `[20]` prevents hallucinations; 100% compact comma-delimited data rows. Can be wrapped in **XML-style semantic container tags** (`<metadata>`, `<dataset>`, `<rules>`) for unambiguous LLM boundary recognition without token bloat.

---

## 📈 Measured Benchmarks

Measured using the standard OpenAI `cl100k_base` and `o200k_base` tokenizers on identical 20-service datasets:

| Format | File Size (Bytes) | Characters | Tokens (`cl100k`) | Tokens (`o200k`) | Token Ratio | Savings vs Format |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Semantic HTML** | 6,684 | 6,684 | **1,911** | 1,916 | 3.03x | **66.98% less tokens** |
| **Pure XML** | 6,336 | 6,336 | **1,858** | 1,905 | 2.94x | **66.04% less tokens** |
| **JSON (Indented)** | 4,730 | 4,730 | **1,473** | 1,487 | 2.33x | **57.16% less tokens** |
| **Markdown Table** | 2,145 | 2,145 | **696** | 704 | 1.10x | **9.34% less tokens** |
| **TOON** | **1,769** | **1,769** | **631** | **638** | **1.0x (Baseline)** | — |

> 🚀 **Takeaway**: Reading a TOON dataset takes **1/3 the tokens** of raw HTML and **less than half** the tokens of standard JSON, leaving more context window for your agent's reasoning.

---

## 🏗️ Architecture: Dual-Mode Operation

```
                      ┌─────────────────────────────────┐
                      │          document.md            │
                      │   (Contains ```toon``` block)   │
                      └────────────────┬────────────────┘
                                       │
                        toon sync      ▼
                      ┌─────────────────────────────────┐
                      │          document.html          │
                      │   (Semantic HTML5 skeleton      │
                      │    + <script type="text/toon">) │
                      └────────────────┬────────────────┘
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            ▼                                                     ▼
   [ Browser User View ]                                 [ AI Agent Ingestion ]
   - Semantic HTML5 structure                            - Ingests only ```toon```
   - Responsive cards & tables                           - 67% token savings vs HTML
   - Dark/Light mode CSS                                 - Zero column-drift errors
   - Client-side DOM render                              - Maximum token economy
```

---

## 📦 Installation & Setup

### 1. Install CLI
Clone and symlink the standalone Python CLI:
```bash
git clone https://github.com/rairahulr1/toon.git
cd toon
mkdir -p ~/.local/bin
ln -s $(pwd)/bin/toon ~/.local/bin/toon
```

Verify installation:
```bash
toon --help
```

### 2. Install as an Agent Skill
For **OpenCode**, **Claude Code**, **Command Code**, or **Antigravity**:
```bash
# Add to your project's .agents/skills/ directory
mkdir -p .agents/skills/toon
cp path/to/toon/SKILL.md .agents/skills/toon/SKILL.md
```

---

## 🛠️ CLI Commands

```bash
# Validate TOON syntax, column consistency, and row counts
toon validate document.md

# Auto-recount rows [N] and format indentation
toon format document.md

# Synchronize and generate the companion Semantic HTML view
toon sync document.md

# Run the benchmark suite
python3 benchmark/compare.py
```

---

## 📄 File Template

Create `spec.md`:
````markdown
# Project Architecture & Radar

> **Browser Viewable HTML:** [`spec.html`](spec.html)
> **as_of:** 2026-10-16
> **owner:** Engineering Team

---

## TOON Specification (Token-Oriented Object Notation)

```toon
metadata:
  title: Project Radar
  version: 1.0.0

clusters[2]{name,region,replicas}:
  prod-us-east,us-east-1,12
  prod-eu-west,eu-west-1,8

checklist[2]:
  - Ensure zero unencrypted egress.
  - Multi-region DB replication active.
```
````

Then run:
```bash
toon sync spec.md
```
Open `spec.html` in your browser to see a responsive, interactive dashboard rendered instantly with zero build setup.

---

## 📜 License

MIT License. Crafted with efficiency for the multi-agent AI era.
