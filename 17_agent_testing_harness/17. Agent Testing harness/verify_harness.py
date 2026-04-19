import os
from harness.test_runner import TestRunner
from harness.test_case import TestCase
from app import MockAgent
from shared.utils import load_yaml

def verify():
    print("Starting verification of Agent Testing Harness...")
    
    # 1. Load config
    config = load_yaml("config.yaml")
    
    # 2. Load sample tests
    raw_tests = load_yaml("tests/sample_tests.yaml")
    test_cases = [TestCase.from_dict(t) for t in raw_tests]
    
    # 3. Initialize components
    runner = TestRunner(config)
    agent = MockAgent()
    
    # 4. Run all tests
    print(f"Running {len(test_cases)} test cases...")
    report = runner.run_all(agent, test_cases)
    
    print("\nTest Results Summary:")
    print(f"Total: {report['total_tests']}")
    print(f"Passed: {report['passed']}")
    print(f"Failed: {report['failed']}")
    print(f"Errors: {report['errors']}")
    
    # 5. Check if reports directory was created
    if os.path.exists("reports") and len(os.listdir("reports")) > 0:
        print("\n✅ Verification Successful: Reports generated.")
    else:
        print("\n❌ Verification Failed: No reports found.")

if __name__ == "__main__":
    verify()
