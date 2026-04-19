import tempfile
import os
import subprocess
import json
from typing import List
from app.models import Issue

class SecurityAnalyzer:
    def __init__(self):
        pass

    def analyze(self, code: str, language: str) -> List[Issue]:
        if language.lower() != "python":
            return []

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        issues = []
        try:
            # Run bandit
            # -f json: output as json
            # -q: quiet
            bandit_args = ["bandit", "-f", "json", "-q", temp_file_path]
            
            result = subprocess.run(bandit_args, capture_output=True, text=True)
            
            # Bandit returns exit code 1 if issues are found, so we don't check returncode for 0
            if result.stdout:
                try:
                    bandit_output = json.loads(result.stdout)
                    for item in bandit_output.get('results', []):
                        issues.append(Issue(
                            category="Security",
                            description=f"{item['test_id']}: {item['issue_text']}",
                            line_number=item['line_number'],
                            severity=item['issue_severity'].lower(), # bandit uses LOW, MEDIUM, HIGH
                            confidence_score=1.0 if item['issue_confidence'] == 'HIGH' else 0.8,
                            suggestion=f"Fix security issue: {item['test_name']}"
                        ))
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            print(f"Error running bandit: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                
        return issues
