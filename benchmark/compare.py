#!/usr/bin/env python3
"""
Benchmark comparison script: Markdown vs Semantic HTML vs JSON vs TOON.
Measures token counts (cl100k_base, o200k_base), character length, byte size,
and token reduction ratios.
"""

import sys
import json
from pathlib import Path

try:
    import tiktoken
except ImportError:
    print("Please install tiktoken: pip install tiktoken")
    sys.exit(1)

BENCH_DIR = Path(__file__).parent.resolve()

def load_file(filename):
    p = BENCH_DIR / filename
    if not p.exists():
        raise FileNotFoundError(f"Missing {p}")
    return p.read_text(encoding="utf-8")

def count_tokens(text, encoding_name):
    enc = tiktoken.get_encoding(encoding_name)
    return len(enc.encode(text))

def main():
    md_content = load_file("dataset.md")
    html_content = load_file("dataset.html")
    json_content = load_file("dataset.json")
    toon_content = load_file("dataset.toon")

    formats = {
        "Semantic HTML": html_content,
        "JSON (Indented)": json_content,
        "Markdown": md_content,
        "TOON": toon_content,
    }

    results = {}

    for name, content in formats.items():
        results[name] = {
            "bytes": len(content.encode("utf-8")),
            "chars": len(content),
            "lines": len(content.splitlines()),
            "tokens_cl100k": count_tokens(content, "cl100k_base"),
            "tokens_o200k": count_tokens(content, "o200k_base"),
        }

    base_html = results["Semantic HTML"]["tokens_cl100k"]
    base_json = results["JSON (Indented)"]["tokens_cl100k"]
    base_md = results["Markdown"]["tokens_cl100k"]
    toon_tokens = results["TOON"]["tokens_cl100k"]

    results["Analysis"] = {
        "savings_vs_html_pct": round((1 - toon_tokens / base_html) * 100, 2),
        "savings_vs_json_pct": round((1 - toon_tokens / base_json) * 100, 2),
        "savings_vs_markdown_pct": round((1 - toon_tokens / base_md) * 100, 2),
        "density_multiplier_vs_html": round(base_html / toon_tokens, 2),
        "density_multiplier_vs_json": round(base_json / toon_tokens, 2),
        "density_multiplier_vs_md": round(base_md / toon_tokens, 2),
    }

    print("\n" + "=" * 75)
    print("  TOON vs MARKDOWN vs JSON vs SEMANTIC HTML TOKEN BENCHMARK")
    print("=" * 75)
    print(f"{'Format':<18} | {'Bytes':<7} | {'Chars':<7} | {'cl100k':<8} | {'o200k':<8} | {'vs TOON'}")
    print("-" * 75)
    for name in ["Semantic HTML", "JSON (Indented)", "Markdown", "TOON"]:
        d = results[name]
        ratio = f"{round(d['tokens_cl100k'] / toon_tokens, 2)}x tokens" if name != "TOON" else "Baseline (1.0x)"
        print(f"{name:<18} | {d['bytes']:<7} | {d['chars']:<7} | {d['tokens_cl100k']:<8} | {d['tokens_o200k']:<8} | {ratio}")
    print("=" * 75)
    print(f"Token Reduction vs Semantic HTML: {results['Analysis']['savings_vs_html_pct']}% less tokens ({results['Analysis']['density_multiplier_vs_html']}x more dense)")
    print(f"Token Reduction vs JSON:          {results['Analysis']['savings_vs_json_pct']}% less tokens ({results['Analysis']['density_multiplier_vs_json']}x more dense)")
    print(f"Token Reduction vs Markdown:      {results['Analysis']['savings_vs_markdown_pct']}% less tokens ({results['Analysis']['density_multiplier_vs_md']}x more dense)")
    print("=" * 75 + "\n")

    out_file = BENCH_DIR / "benchmark_results.json"
    out_file.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"✓ Saved results to: {out_file.name}")

if __name__ == "__main__":
    main()
