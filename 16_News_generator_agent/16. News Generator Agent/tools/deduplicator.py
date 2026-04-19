try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    # Fallback if scikit-learn is not installed
    TfidfVectorizer = None

from shared.logger import logger

def remove_duplicates(news_list: list, threshold: float = 0.8) -> list:
    """
    Remove similar or identical articles using TF-IDF and Cosine Similarity.
    """
    if not news_list:
        return []
    
    if TfidfVectorizer is None:
        logger.warning("scikit-learn not installed. Skipping advanced deduplication.")
        # Simple title-based deduplication as fallback
        seen_titles = set()
        unique_news = []
        for article in news_list:
            if article["title"] not in seen_titles:
                unique_news.append(article)
                seen_titles.add(article["title"])
        return unique_news

    # Prepare data for TF-IDF
    contents = [f"{a['title']} {a['content']}" for a in news_list]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(contents)
    
    # Calculate pairwise cosine similarity
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    to_remove = set()
    for i in range(len(news_list)):
        if i in to_remove:
            continue
        for j in range(i + 1, len(news_list)):
            if similarity_matrix[i, j] > threshold:
                logger.info(f"Removing duplicate article: '{news_list[j]['title']}' (similar to '{news_list[i]['title']}')")
                to_remove.add(j)
                
    unique_news = [article for idx, article in enumerate(news_list) if idx not in to_remove]
    return unique_news
