import re

def clean_text(text: str) -> str:
    """
    Cleans text by removing URLs, hashtags, and special characters.
    """
    if not text:
        return ""
        
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove hashtags (keeping the word, but removing the #)
    text = re.sub(r'#(\w+)', r'\1', text)
    
    # Remove user mentions (@username)
    text = re.sub(r'@\w+', '', text)
    
    # Remove special characters but keep alphanumeric and basic punctuation
    text = re.sub(r'[^\w\s\.,!\?]', '', text)
    
    # Remove extra whitespace
    text = " ".join(text.split())
    
    return text
