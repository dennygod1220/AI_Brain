from bs4 import BeautifulSoup


def clean_html_to_markdown(html_content: str) -> str:
    """
    將 HTML 轉換為純文字，移除 Script, Style, Nav 等噪音。
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # 移除噪音標籤
    for noise in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
        noise.decompose()

    # 取得文字並進行初步處理
    text = soup.get_text(separator='\n')
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return '\n'.join(lines)
