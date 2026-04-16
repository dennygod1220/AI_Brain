import sys
sys.path.insert(0, '..')

from utils.cleaner import clean_html_to_markdown


def test_cleaner_removes_scripts():
    html = "<html><script>alert(1)</script><body><p>Hello World</p></body></html>"
    result = clean_html_to_markdown(html)
    assert "alert(1)" not in result
    assert "Hello World" in result


def test_cleaner_removes_styles():
    html = "<html><style>.css{}</style><body><h1>Title</h1></body></html>"
    result = clean_html_to_markdown(html)
    assert ".css" not in result
    assert "Title" in result


def test_cleaner_removes_nav_footer():
    html = "<html><nav>NavBar</nav><body><p>Content</p></body><footer>FooterText</footer></html>"
    result = clean_html_to_markdown(html)
    assert "NavBar" not in result
    assert "FooterText" not in result
    assert "Content" in result
