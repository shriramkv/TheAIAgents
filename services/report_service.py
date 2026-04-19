from typing import List, Dict

class ReportService:
    """
    Service for generating detailed interview reports.
    """
    def __init__(self, client, model_name: str):
        """
        Initialize with OpenAI client and model name.
        
        Args:
            client: OpenAI client instance
            model_name (str): Name of the LLM model to use
        """
        self.client = client
        self.model_name = model_name

    def generate_final_report(self, history: List[Dict]) -> str:
        """
        Generate a comprehensive markdown report based on interview history.
        
        Args:
            history (List[Dict]): List of interview turns (question, answer, feedback).
            
        Returns:
            str: Markdown formatted report.
        """
        system = "You are an expert interview coach. Generate a comprehensive interview report based on the following conversation history."
        user_content = "Conversation History:\n"
        for item in history:
            user_content += f"Q: {item['question']}\nA: {item['answer']}\nFeedback: {item.get('feedback', '')}\n\n"
        
        user_content += (
            "Please provide a report in Markdown format with the following sections:\n"
            "1. **Executive Summary**: Brief overview of performance.\n"
            "2. **Strengths**: Key areas where the candidate excelled.\n"
            "3. **Areas for Improvement**: Specific actionable advice.\n"
            "4. **Scores**: Rate (0-10) on Technical Knowledge, Communication, and Problem Solving.\n"
            "5. **Final Verdict**: Hire / No Hire / Strong Hire recommendation."
        )
        
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user_content}
        ]
        
        try:
            resp = self.client.chat.completions.create(
                model=self.model_name, 
                messages=messages, 
                max_tokens=1000
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"Error generating report: {e}")
            return "Error generating report."
