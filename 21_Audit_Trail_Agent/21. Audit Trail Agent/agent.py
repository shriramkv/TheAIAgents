import uuid
from typing import Dict, Any, List
from shared.base_agent import BaseAgent
from shared.llm import call_llm
from shared.utils import load_config
from audit.logger import AuditLogger
from audit.storage import AuditStorage

class AuditedAgent(BaseAgent):
    """
    An agent that logs every internal step to a structured audit trail.
    """
    def __init__(self, name: str = "AuditTrailAgent"):
        super().__init__(name)
        self.config = load_config()
        self.model = self.config.get("model", "gpt-4o-mini")
        
        # Initialize Audit System
        self.storage = AuditStorage(self.config.get("log_file", "logs/audit_log.json"))
        self.logger = AuditLogger(self.storage)

    def _tools(self, tool_name: str, args: str) -> str:
        """
        Mock tool execution for demonstration purposes.
        """
        if tool_name == "calculator":
            try:
                # DANGER: eval is used here ONLY for mock demonstration purposes.
                # In production, use a safe math parser.
                result = eval(args)
                return str(result)
            except Exception as e:
                return f"Error: {str(e)}"
        return f"Tool {tool_name} not found."

    def run(self, user_query: str) -> Dict[str, Any]:
        """
        Execute the agent loop with comprehensive auditing.
        """
        trace_id = str(uuid.uuid4())
        
        # 1. Thought Step
        thought_content = f"Analyzing user query: '{user_query}'. I need to determine if a tool is needed or if I can answer directly."
        self.logger.log_step(
            agent_name=self.name,
            step_type="thought",
            content=thought_content,
            trace_id=trace_id
        )

        # 2. Decision/Action Step: Call LLM to decide
        prompt = f"""
        You are an assistant. User query: {user_query}
        If the query requires calculation, respond with: TOOL: calculator, ARGS: <math expression>
        Otherwise, provide the final answer directly.
        """
        
        llm_output = call_llm([{"role": "user", "content": prompt}], model=self.model)
        response_text = llm_output["response"]
        tokens = llm_output["tokens_used"]

        self.logger.log_step(
            agent_name=self.name,
            step_type="action",
            content="Received LLM response for decision making.",
            trace_id=trace_id,
            metadata={"llm_response": response_text, "tokens_used": tokens}
        )

        # 3. Handle Tool Usage or Direct Answer
        if "TOOL:" in response_text:
            # Parse tool call
            parts = response_text.split(",")
            tool_name = parts[0].split(":")[1].strip()
            tool_args = parts[1].split(":")[1].strip()

            # Log tool call
            self.logger.log_step(
                agent_name=self.name,
                step_type="action",
                content=f"Executing tool: {tool_name}",
                trace_id=trace_id,
                tool=tool_name,
                decision="call_tool",
                metadata={"args": tool_args}
            )

            # Observation Step
            observation = self._tools(tool_name, tool_args)
            self.logger.log_step(
                agent_name=self.name,
                step_type="observation",
                content=f"Tool result: {observation}",
                trace_id=trace_id,
                tool=tool_name
            )

            # Final Thought & Answer
            final_prompt = f"The result of the {tool_name} was {observation}. Based on this, answer the original query: {user_query}"
            final_llm_output = call_llm([{"role": "user", "content": final_prompt}], model=self.model)
            final_answer = final_llm_output["response"]
            
            self.logger.log_step(
                agent_name=self.name,
                step_type="decision",
                content=f"Generating final answer: {final_answer}",
                trace_id=trace_id,
                decision="final_response",
                metadata={"tokens_used": final_llm_output["tokens_used"]}
            )
            
            return {"response": final_answer, "trace_id": trace_id}
        else:
            # Direct Answer
            self.logger.log_step(
                agent_name=self.name,
                step_type="decision",
                content=f"Direct answer provided: {response_text}",
                trace_id=trace_id,
                decision="final_response"
            )
            return {"response": response_text, "trace_id": trace_id}

if __name__ == "__main__":
    agent = AuditedAgent()
    result = agent.run("What is 25 * 4?")
    print(f"Response: {result['response']}")
    print(f"Trace ID: {result['trace_id']}")
