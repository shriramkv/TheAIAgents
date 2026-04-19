import os
from typing import List, Dict
from shared.base_agent import BaseAgent
from shared.llm import call_llm
from shared.utils import load_config
from tools.twitter_monitor import fetch_twitter_posts
from tools.reddit_monitor import fetch_reddit_posts
from tools.data_cleaner import clean_text
from analysis.sentiment import classify_sentiment
from analysis.anomaly_detector import detect_spike

class BrandMonitoringAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="BrandMonitor")
        self.config = load_config()
        self.logs = []

    def _add_log(self, message: str):
        self.log_step(message)
        self.logs.append(message)

    def run(self, brand_keyword: str) -> Dict:
        """
        Executes the full brand monitoring pipeline.
        """
        self.logs = []
        self._add_log(f"Starting monitoring for brand: {brand_keyword}")

        # 1. Data Collection
        self._add_log("Collecting posts from Twitter and Reddit...")
        twitter_posts = fetch_twitter_posts(brand_keyword, limit=self.config.get("max_posts", 20))
        reddit_posts = fetch_reddit_posts(brand_keyword, limit=self.config.get("max_posts", 20))
        all_posts = twitter_posts + reddit_posts
        self._add_log(f"Collected total {len(all_posts)} posts.")

        if not all_posts:
            self._add_log("No posts found for this keyword.")
            return {
                "posts": [],
                "sentiment_summary": "N/A",
                "anomaly_detection": "N/A",
                "final_report": "No data found to generate report.",
                "logs": "\n".join(self.logs)
            }

        # 2. Text Cleaning & Sentiment Analysis
        self._add_log("Cleaning text and analyzing sentiment...")
        processed_data = []
        sentiments = []
        for post in all_posts:
            cleaned = clean_text(post["text"])
            sentiment = classify_sentiment(cleaned)
            post["cleaned_text"] = cleaned
            post["sentiment"] = sentiment
            processed_data.append(post)
            sentiments.append(sentiment)
        
        positive_count = sentiments.count("Positive")
        neutral_count = sentiments.count("Neutral")
        negative_count = sentiments.count("Negative")
        
        sentiment_summary = (
            f"Positive: {positive_count} | "
            f"Neutral: {neutral_count} | "
            f"Negative: {negative_count}"
        )
        self._add_log(f"Sentiment Analysis Complete: {sentiment_summary}")

        # 3. Anomaly Detection
        self._add_log("Running anomaly detection...")
        anomaly_result = detect_spike(sentiments)
        self._add_log(f"Anomaly Detection Result: {anomaly_result['explanation']}")

        # 4. Final Report Generation
        self._add_log("Generating final structured report...")
        final_report = self._generate_report(
            brand_keyword, 
            processed_data, 
            positive_count, 
            neutral_count, 
            negative_count, 
            anomaly_result['explanation']
        )
        self._add_log("Monitoring cycle completed.")

        return {
            "posts": processed_data,
            "sentiment_summary": sentiment_summary,
            "anomaly_detection": anomaly_result['explanation'],
            "final_report": final_report,
            "logs": "\n".join(self.logs)
        }

    def _generate_report(self, brand_name, posts, pos, neu, neg, anomaly_expl) -> str:
        prompt_path = os.path.join("prompts", "report_generator.txt")
        if not os.path.exists(prompt_path):
            return "Report prompt template missing."
            
        with open(prompt_path, "r") as f:
            template = f.read()
            
        sample_posts_str = "\n".join([f"- {p['cleaned_text'][:100]}... ({p['sentiment']})" for p in posts[:3]])
        
        prompt = template.format(
            brand_name=brand_name,
            total_posts=len(posts),
            positive_count=pos,
            neutral_count=neu,
            negative_count=neg,
            anomaly_explanation=anomaly_expl,
            sample_posts=sample_posts_str
        )
        
        try:
            return call_llm(prompt, system_prompt="You are a professional brand analyst.")
        except Exception as e:
            self._add_log(f"Report generation failed: {e}")
            return "Error generating report."

if __name__ == "__main__":
    # Quick standalone test
    agent = BrandMonitoringAgent()
    result = agent.run("Tesla")
    print("\n--- FINAL REPORT ---\n")
    print(result["final_report"])
