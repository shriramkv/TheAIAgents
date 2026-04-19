from shared.base_agent import BaseAgent
from shared.logger import logger
from tools.news_fetcher import fetch_news
from tools.deduplicator import remove_duplicates
from tools.clusterer import cluster_news
from processing.summarizer import summarize_article
from processing.formatter import format_newsletter

class NewsGeneratorAgent(BaseAgent):
    """
    Agent that orchestrates the news aggregation and newsletter generation process.
    """
    def __init__(self):
        super().__init__(name="NewsGeneratorAgent")

    def run(self, category: str, tone: str, length: str) -> tuple:
        """
        Full news generation flow.
        Returns (newsletter, logs)
        """
        # 1. Input Log
        self.log_step("Input", f"Category: {category}, Tone: {tone}, Length: {length}")

        # 2. Fetch News
        raw_news = fetch_news(category)
        self.log_step("Raw News", f"Fetched {len(raw_news)} articles.")

        # 3. Deduplicate
        unique_news = remove_duplicates(raw_news)
        self.log_step("Deduplicated News", f"Reduced to {len(unique_news)} unique articles.")

        # 4. Cluster
        clusters = cluster_news(unique_news)
        cluster_info = {topic: [a['title'] for a in arts] for topic, arts in clusters.items()}
        self.log_step("Clusters", str(cluster_info))

        # 5. Summarize
        # We'll update the clusters with summaries
        summarized_clusters = {}
        for topic, articles in clusters.items():
            summarized_clusters[topic] = []
            for article in articles:
                summary = summarize_article(article)
                article_with_summary = article.copy()
                article_with_summary["summary"] = summary
                summarized_clusters[topic].append(article_with_summary)
        
        summary_count = sum(len(arts) for arts in summarized_clusters.values())
        self.log_step("Summaries", f"Generated {summary_count} summaries across {len(summarized_clusters)} topics.")

        # 6. Generate Newsletter
        final_newsletter = format_newsletter(summarized_clusters, tone, length)
        self.log_step("Final Newsletter", "Newsletter generation complete.")

        return final_newsletter, self.get_logs()
