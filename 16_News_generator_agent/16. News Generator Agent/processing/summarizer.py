from shared.llm import call_llm
from shared.utils import read_prompt
from shared.logger import logger

def summarize_article(article: dict) -> str:
    """
    Summarize article into key points using LLM.
    """
    logger.info(f"Summarizing article: {article['title']}")
    
    prompt_template = read_prompt("summarization.txt")
    article_content = f"Title: {article['title']}\nContent: {article['content']}"
    
    prompt = prompt_template.format(article_content=article_content)
    
    summary = call_llm(prompt, system_prompt="You are a professional news summarizer.")
    return summary
