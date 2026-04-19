from typing import Optional, Dict, Any

class TestCase:
    def __init__(
        self,
        name: str,
        input: str,
        expected_output: Optional[str] = None,
        expected_behavior: Optional[Dict[str, Any]] = None
    ):
        """
        Represents a single test case for an agent.
        
        :param name: Human-readable name of the test
        :param input: The prompt or input string for the agent
        :param expected_output: Optional substring or exact string to check in the final answer
        :param expected_behavior: Optional dict containing metadata checks (e.g. max cost, tools called)
        """
        self.name = name
        self.input = input
        self.expected_output = expected_output
        self.expected_behavior = expected_behavior or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "input": self.input,
            "expected_output": self.expected_output,
            "expected_behavior": self.expected_behavior
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestCase':
        return cls(
            name=data.get("name", "Unnamed Test"),
            input=data.get("input", ""),
            expected_output=data.get("expected_output"),
            expected_behavior=data.get("expected_behavior")
        )
