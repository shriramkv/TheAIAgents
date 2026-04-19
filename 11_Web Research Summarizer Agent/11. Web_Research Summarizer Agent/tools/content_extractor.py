from bs4 import BeautifulSoup
import re

def extract_main_content(html: str) -> str:
    """
    Extracts clean text from raw HTML by removing noise like ads, navigation, and boilerplate.
    """
    if not html:
        return ""

    soup = BeautifulSoup(html, 'html.parser')

    # Remove script and style elements
    for script_or_style in soup(["script", "style", "nav", "footer", "header", "aside"]):
        script_or_style.decompose()

    # Heuristic: focus on main or article tags if they exist
    main_content = soup.find('main') or soup.find('article') or soup.body
    
    if not main_content:
        return ""

    # Get text
    text = main_content.get_text(separator=' ')

    # Basic cleaning
    # Break into lines and remove leading/trailing whitespace
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    # Limit to first 4000 words or so to avoid LLM token issues
    return text[:15000]
