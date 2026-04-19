import os
from typing import Optional
from shared.base_agent import BaseAgent
from shared.llm import call_llm
from shared.logger import logger
from risk.risk_evaluator import is_high_risk
from approval.slack_notifier import send_slack_approval
from approval.email_notifier import send_email_approval
from approval.approval_handler import approval_handler

class HumanInTheLoopAgent(BaseAgent):
    def __init__(self, name: str = "HITL_Agent"):
        super().__init__(name)
        self.system_prompt = self._load_prompt()

    def _load_prompt(self) -> str:
        prompt_path = "prompts/agent.txt"
        if os.path.exists(prompt_path):
            with open(prompt_path, "r") as f:
                return f.read()
        return "You are an AI agent. Output ACTION: <action>."

    def run(self, user_input: str) -> str:
        """
        FULL FLOW:
        1. Input: User request
        2. Generate Action: LLM decides
        3. Risk Check: is_high_risk(action)
        4. Request Approval: if risky
        5. Wait for Response: wait_for_approval
        6. Decision: Execute or Abort
        7. Return Result
        """
        # 1. Log Input
        self.log_input(user_input)

        # 2. Generate Action
        llm_response = call_llm(user_input, system_prompt=self.system_prompt)
        
        # Extract ACTION from LLM response
        action = self._extract_action(llm_response)
        self.logger.log_action(action)

        # 3. Risk Check
        risky = is_high_risk(action)
        self.logger.log_risk(risky)

        if risky:
            # 4. Request Approval
            message = f"Agent wants to perform: {action}\nApprove?"
            
            # Send via notified methods (Slack and Email)
            req_id_slack = send_slack_approval(message)
            req_id_email = send_email_approval(message)
            
            # We'll use the slack ID (or a unique combo) for waiting
            request_id = req_id_slack if req_id_slack != "ERROR" else "SIM_ID"
            
            # 5. Wait for Response
            approved = approval_handler.wait_for_approval(request_id)
            
            # 6. Decision
            if not approved:
                result = f"Action aborted: '{action}' was rejected or timed out."
                self.log_result(result)
                return result
            
            self.logger.info("Human approved. Proceeding with execution...")

        # 7. Execute Action (Simulation)
        result = self._execute_action(action)
        self.log_result(result)
        return result

    def _extract_action(self, llm_response: str) -> str:
        """Simple extractor for 'ACTION: <something>' line."""
        for line in llm_response.split('\n'):
            if line.upper().startswith("ACTION:"):
                return line[7:].strip()
        return llm_response # Fallback

    def _execute_action(self, action: str) -> str:
        """Simulate execution of the action."""
        # In a real system, this would call tools/APIs
        return f"Successfully executed action: '{action}'"

if __name__ == "__main__":
    # Test block
    agent = HumanInTheLoopAgent()
    agent.run("Send a high priority email to boss@company.com")
