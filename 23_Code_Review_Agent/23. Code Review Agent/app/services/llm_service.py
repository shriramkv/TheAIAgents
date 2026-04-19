import os
import json
from typing import Dict, Any
from openai import OpenAI
from app.models import ReviewResponse

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"

    def review_code(self, code: str, language: str) -> Dict[str, Any]:
        system_prompt = (
            "You are an expert Senior Software Engineer and Code Reviewer. "
            "Your task is to review code for SOLID principles, logic correctness, "
            "time/space complexity, efficiency, style, and refactoring opportunities. "
            "You must return the result in a valid JSON format that matches the specified schema."
        )
        
        user_prompt = f"""
Review the following {language} code:

```
{code}
```

Provide a detailed review in the following JSON format:
{{
  "issues": [
    {{
      "category": "SOLID" | "Logic" | "Style" | "Efficiency",
      "description": "Detailed description of the issue",
      "line_number": int | null,
      "severity": "major" | "medium" | "minor",
      "confidence_score": float (0.0 to 1.0),
      "suggestion": "How to fix it"
    }}
  ],
  "complexity": {{
    "time_complexity": "Big O notation (e.g., O(n))",
    "space_complexity": "Big O notation (e.g., O(1))"
  }},
  "efficiency_recommendations": ["rec1", "rec2"],
  "style_suggestions": ["sugg1", "sugg2"],
  "refactoring_suggestions": [
    {{
      "description": "What to refactor",
      "original_code": "Code snippet to replace",
      "refactored_code": "New code",
      "explanation": "Why this is better"
    }}
  ],
  "summary": "Brief summary of the review"
}}
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            
            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response from LLM")
                
            return json.loads(content)
            
        except Exception as e:
            print(f"Error calling LLM: {e}")
            # Return a fallback error response
            return {
                "issues": [{
                    "category": "System",
                    "description": f"LLM Review failed: {str(e)}",
                    "severity": "major",
                    "confidence_score": 1.0,
                    "suggestion": "Check API key and connectivity"
                }],
                "complexity": {"time_complexity": "Unknown", "space_complexity": "Unknown"},
                "efficiency_recommendations": [],
                "style_suggestions": [],
                "refactoring_suggestions": [],
                "summary": "Review failed due to internal error."
            }
