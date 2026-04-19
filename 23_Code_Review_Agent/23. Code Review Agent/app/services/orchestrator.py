from typing import Dict, Any
import asyncio
from app.services.analysis_service import StaticAnalyzer
from app.services.security_service import SecurityAnalyzer
from app.services.llm_service import LLMService
from app.models import ReviewResponse, Issue, ComplexityAnalysis

class ReviewOrchestrator:
    def __init__(self):
        self.static_analyzer = StaticAnalyzer()
        self.security_analyzer = SecurityAnalyzer()
        self.llm_service = LLMService()

    async def review(self, code: str, language: str) -> ReviewResponse:
        # Run static analysis and LLM review in parallel (conceptually, though LLM is blocking IO)
        # Since LLMService is synchronous for now, we'll run them sequentially or use run_in_executor if needed.
        # For simplicity in this iteration, we run sequentially.
        
        # 1. Static Analysis
        static_results = self.static_analyzer.analyze(code, language)
        
        # 2. Security Analysis
        security_issues = self.security_analyzer.analyze(code, language)
        
        # 3. LLM Review
        llm_results = self.llm_service.review_code(code, language)
        
        # 4. Merge Results
        return self._merge_results(static_results, security_issues, llm_results)

    def _merge_results(self, static: Dict[str, Any], security_issues: list, llm: Dict[str, Any]) -> ReviewResponse:
        # Merge Issues
        all_issues = []
        
        # Convert LLM issues to Issue objects
        for item in llm.get("issues", []):
            all_issues.append(Issue(**item))
            
        # Add Static Analysis issues
        all_issues.extend(static.get("issues", []))
        
        # Add Security issues
        all_issues.extend(security_issues)
        
        # Merge Complexity
        llm_complexity = llm.get("complexity", {})
        static_complexity = static.get("complexity")
        
        final_complexity = ComplexityAnalysis(
            time_complexity=llm_complexity.get("time_complexity", "Unknown"),
            space_complexity=llm_complexity.get("space_complexity", "Unknown"),
            cyclomatic_complexity=static_complexity.cyclomatic_complexity if static_complexity else None,
            maintainability_index=static_complexity.maintainability_index if static_complexity else None
        )
        
        return ReviewResponse(
            issues=all_issues,
            complexity=final_complexity,
            efficiency_recommendations=llm.get("efficiency_recommendations", []),
            style_suggestions=llm.get("style_suggestions", []),
            refactoring_suggestions=llm.get("refactoring_suggestions", []),
            summary=llm.get("summary", "Review completed.")
        )
