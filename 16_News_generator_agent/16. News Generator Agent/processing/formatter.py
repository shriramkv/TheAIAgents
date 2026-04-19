import json
from shared.llm import call_llm
from shared.utils import read_prompt
from shared.logger import logger

def format_newsletter(summaries: dict, tone: str, length: str) -> str:
    """
    Format summaries into the final newsletter using LLM.
    """
    logger.info(f"Generating newsletter with tone='{tone}' and length='{length}'")
    
    prompt_template = read_prompt("newsletter_generator.txt")
    
    # Convert summaries dict to a readable string for the prompt
    summaries_str = ""
    for topic, articles in summaries.items():
        summaries_str += f"\nTOPIC: {topic}\n"
        for art in articles:
            summaries_str += f"- {art['title']}\n  Summary: {art['summary']}\n"
            
    prompt = prompt_template.format(
        summaries=summaries_str,
        tone=tone,
        length=length
    )
    
    newsletter = call_llm(prompt, system_prompt=f"You are an expert newsletter editor writing in a {tone} tone.")
    return newsletter
