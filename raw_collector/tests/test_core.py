import sys
sys.path.insert(0, '..')

import os
import tempfile
from collector_core import save_article


def test_save_article_creates_file():
    test_url = "https://example.com"
    test_title = "Test Article"
    test_content = "This is the content."
    test_tags = ["test", "automation"]

    with tempfile.TemporaryDirectory() as tmpdir:
        path = save_article(test_content, test_url, test_title, test_tags, output_dir=tmpdir)

        assert os.path.exists(path), f"File not created: {path}"
        with open(path, "r", encoding="utf-8") as f:
            file_content = f.read()
            assert "---" in file_content, "Missing frontmatter separator"
            assert "source: https://example.com" in file_content, "Missing source URL"
            assert "title: Test Article" in file_content, "Missing title"
            assert "This is the content." in file_content, "Missing content"
            assert "test" in file_content, "Missing tags"


def test_save_article_filename_sanitization():
    """標題含特殊字元時應被清理乾淨"""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = save_article(
            content="Body",
            url="https://example.com",
            title="My Article: Version 2.0 (Final)",
            tags=["test"],
            output_dir=tmpdir
        )
        filename = os.path.basename(path)
        # 不應包含冒號、括號等
        assert ":" not in filename, f"Colon in filename: {filename}"
        assert "(" not in filename, f"Paren in filename: {filename}"
