from shared.logger import logger

def cluster_news(news_list: list) -> dict:
    """
    Group similar articles into topics.
    For this 'simple similarity' requirement, we'll use keyword-based grouping
    or simply group by metadata if available. 
    In a production setting, this could use K-Means or LDA.
    """
    if not news_list:
        return {}

    logger.info("Clustering news articles into topics.")
    
    # Simple keyword-based clustering
    clusters = {}
    
    # We'll use the 'category' field if present, otherwise group into 'Top Stories'
    for article in news_list:
        topic = article.get("category", "General")
        if topic not in clusters:
            clusters[topic] = []
        clusters[topic].append(article)
            
    return clusters
