import time
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

from .test_case import TestCase
from .loop_detector import LoopDetector
from .cost_tracker import CostTracker
from .failure_simulator import FailureSimulator
from shared.logger import logger
from shared.utils import save_json

class TestRunner:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Orchestrates the execution of agent tests.
        """
        self.config = config or {}
        self.loop_detector = LoopDetector(self.config.get("loop_detection", {}))
        self.cost_tracker = CostTracker(self.config.get("cost_tracking", {}))
        self.failure_simulator = FailureSimulator(self.config.get("failure_simulation", {}))
        
        self.results = []

    def run_test(self, agent_adapter: Any, test_case: TestCase) -> Dict[str, Any]:
        """
        Runs a single test case against an agent.
        """
        logger.info(f"Running test: {test_case.name}")
        start_time = time.time()
        
        # Reset trackers for this specific test
        self.cost_tracker.reset()
        
        # Inject failure simulator if the agent supports it
        # Note: This depends on the agent implementation being able to accept wrapped tools
        if hasattr(agent_adapter, "inject_tools"):
            from .mock_tools import MOCK_TOOLS
            wrapped_tools = {
                name: self.failure_simulator.inject_failure(name, func)
                for name, func in MOCK_TOOLS.items()
            }
            agent_adapter.inject_tools(wrapped_tools)

        try:
            # 1. Execute Agent
            response = agent_adapter.run(test_case.input)
            
            # 2. Extract Data
            output = response.get("output", "")
            steps = response.get("steps", [])
            metadata = response.get("metadata", {})
            
            # 3. Track Cost
            usage_report = self.cost_tracker.track(metadata)
            
            # 4. Detect Loops
            loop_report = self.loop_detector.check(steps)
            
            # 5. Validate Output
            status = "PASS"
            failure_reason = ""
            
            if test_case.expected_output:
                if test_case.expected_output.lower() not in output.lower():
                    status = "FAIL"
                    failure_reason = f"Expected '{test_case.expected_output}' not found in output."
            
            if loop_report["loop_detected"]:
                status = "FAIL"
                failure_reason = loop_report["reason"]

            result = {
                "test_name": test_case.name,
                "status": status,
                "input": test_case.input,
                "actual_output": output,
                "expected_output": test_case.expected_output,
                "failure_reason": failure_reason,
                "steps": steps,
                "cost_stats": usage_report,
                "loop_detected": loop_report["loop_detected"],
                "duration_sec": round(time.time() - start_time, 2)
            }
            
            self.results.append(result)
            logger.info(f"Test {test_case.name} finished: {status}")
            return result

        except Exception as e:
            logger.error(f"Error running test {test_case.name}: {str(e)}")
            error_result = {
                "test_name": test_case.name,
                "status": "ERROR",
                "error": str(e),
                "duration_sec": round(time.time() - start_time, 2)
            }
            self.results.append(error_result)
            return error_result

    def run_all(self, agent_adapter: Any, test_cases: List[TestCase]) -> Dict[str, Any]:
        """
        Runs all test cases and generates a final report.
        """
        self.results = []
        overall_start = time.time()
        
        for tc in test_cases:
            self.run_test(agent_adapter, tc)
            
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(self.results),
            "passed": len([r for r in self.results if r["status"] == "PASS"]),
            "failed": len([r for r in self.results if r["status"] == "FAIL"]),
            "errors": len([r for r in self.results if r["status"] == "ERROR"]),
            "total_duration_sec": round(time.time() - overall_start, 2),
            "results": self.results
        }
        
        # Save report
        report_path = f"reports/report_{uuid.uuid4().hex[:8]}.json"
        save_json(summary, report_path)
        logger.info(f"Report generated: {report_path}")
        
        return summary
