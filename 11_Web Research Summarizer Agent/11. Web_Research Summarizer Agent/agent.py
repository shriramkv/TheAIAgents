import os
from typing import List, Dict, Any, Tuple
from shared.base_agent import BaseAgent
from shared.utils import read_prompt, load_config
from tools.search_tool import search_web
from tools.scraper import fetch_page_content
from tools.content_extractor import extract_main_content

class WebResearchAgent(BaseAgent):
    """
    Agent that performs end-to-end web research and summarization.
    """
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.num_results = self.config.get("num_search_results", 5)
        self.max_pages = self.config.get("max_pages_to_scrape", 3)

    def run(self, topic: str) -> Tuple[str, List[str], str]:
        """
        Executes the research pipeline.
        Returns: (final_report, sources, reasoning_trace)
        """
        self.logger.clear()
        self.logger.info(f"Starting research on: {topic}")

        # 1. Query Expansion
        expanded_queries = self._expand_query(topic)
        self.logger.info(f"Expanded queries: {expanded_queries}")

        # 2. Search
        all_results = []
        for q in expanded_queries:
            self.logger.info(f"Searching for: {q}")
            results = search_web(q, num_results=self.num_results)
            all_results.extend(results)

        # Deduplicate results by URL
        unique_results = {r['url']: r for r in all_results if r['url']}.values()
        unique_results = list(unique_results)[:self.max_pages]  # Limit to max pages
        
        sources = [r['url'] for r in unique_results]
        self.logger.info(f"Top sources identified: {sources}")

        # 3. Scrape & Extract & Summarize
        summaries = []
        for res in unique_results:
            url = res['url']
            self.logger.info(f"Processing source: {url}")
            
            html = fetch_page_content(url)
            if not html:
                self.logger.error(f"Failed to fetch content from {url}")
                continue
            
            content = extract_main_content(html)
            if not content or len(content) < 100:
                self.logger.error(f"Insufficient content extracted from {url}")
                continue

            self.logger.info(f"Summarizing content from {url}...")
            summary = self._summarize_content(topic, url, content)
            summaries.append(summary)

        if not summaries:
            self.logger.error("No valid summaries could be generated from the identified sources.")
            return "Failed to generate report due to lack of source content.", sources, self.logger.get_logs()

        # 5. Synthesis
        self.logger.info("Synthesizing final report...")
        final_report = self._synthesize_report(topic, summaries)
        self.logger.info("Research complete.")

        return final_report, sources, self.logger.get_logs()

    def _expand_query(self, topic: str) -> List[str]:
        prompt_tmpl = read_prompt("prompts/query_expansion.txt")
        prompt = prompt_tmpl.format(topic=topic)
        response = self.llm.call_llm(prompt)
        # Parse lines and clean
        queries = [q.strip() for q in response.split('\n') if q.strip()]
        # Fallback to original topic if no queries generated
        return queries[:5] if queries else [topic]

    def _summarize_content(self, topic: str, url: str, content: str) -> str:
        prompt_tmpl = read_prompt("prompts/summarizer.txt")
        # Truncate content for prompt safely
        truncated_content = content[:10000]
        prompt = prompt_tmpl.format(topic=topic, url=url, content=truncated_content)
        return self.llm.call_llm(prompt)

    def _synthesize_report(self, topic: str, summaries: List[str]) -> str:
        prompt_tmpl = read_prompt("prompts/synthesizer.txt")
        combined_summaries = "\n\n---\n\n".join(summaries)
        prompt = prompt_tmpl.format(topic=topic, summaries=combined_summaries)
        return self.llm.call_llm(prompt)
