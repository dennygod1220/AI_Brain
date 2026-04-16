#!/usr/bin/env python3
"""
整合測試：使用 Hermes browser tool 進行端到端驗證
流程：browser_navigate → browser_console(outerHTML) → clean_html_to_markdown → save_article
"""
import sys
from pathlib import Path

# Add raw_collector parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import tempfile
from utils.cleaner import clean_html_to_markdown
from collector_core import save_article


def run_integration_test(html_content: str, url: str, title: str, tags: list):
    """手動注入 HTML 模擬 browser 抓取的結果"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Step 1: 清洗 HTML
        cleaned = clean_html_to_markdown(html_content)
        print(f"[Cleaner] Output:\n{cleaned}\n")

        # Step 2: 存入 Markdown
        path = save_article(cleaned, url, title, tags, output_dir=tmpdir)
        print(f"[Collector] Saved to: {path}")

        # Step 3: 驗證
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "---" in content
        assert url in content
        print("[PASS] 整合測試成功")
        return path


if __name__ == "__main__":
    # 模擬 example.com 的 HTML
    sample_html = """
    <html>
    <head><title>Example Domain</title>
    <style>body{background:#eee}</style>
    <script>console.log('evil')</script>
    </head>
    <body>
    <nav>Skip to content</nav>
    <div>
        <h1>Example Domain</h1>
        <p>This domain is for use in documentation examples.</p>
        <a href="https://iana.org/domains/example">Learn more</a>
    </div>
    <footer>Footer text</footer>
    </body>
    </html>
    """

    run_integration_test(
        html_content=sample_html,
        url="https://example.com",
        title="Example Domain",
        tags=["test", "example"]
    )
