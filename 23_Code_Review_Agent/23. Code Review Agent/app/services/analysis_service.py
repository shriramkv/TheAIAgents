import tempfile
import os
import subprocess
import json
from typing import Dict, Any, List
import radon.complexity as radon_cc
import radon.metrics as radon_metrics
from app.models import Issue, ComplexityAnalysis

class StaticAnalyzer:
    def __init__(self):
        pass

    def analyze(self, code: str, language: str) -> Dict[str, Any]:
        if language.lower() != "python":
            return {
                "issues": [],
                "complexity": ComplexityAnalysis(time_complexity="Unknown", space_complexity="Unknown")
            }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        try:
            pylint_issues = self._run_pylint(temp_file_path)
            complexity_metrics = self._run_radon(code)
            
            return {
                "issues": pylint_issues,
                "complexity": complexity_metrics
            }
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def _run_pylint(self, file_path: str) -> List[Issue]:
        issues = []
        # Run pylint as a subprocess to capture output easily
        # Using a custom format to parse easily: msg_id:line:column:msg:symbol
        pylint_args = [
            "pylint",
            file_path,
            "--output-format=json",
            "--disable=C0111,C0103" # Disable missing docstring and invalid name for snippets
        ]
        
        try:
            result = subprocess.run(pylint_args, capture_output=True, text=True)
            if result.stdout:
                try:
                    pylint_output = json.loads(result.stdout)
                    for item in pylint_output:
                        severity_map = {
                            "fatal": "major",
                            "error": "major",
                            "warning": "medium",
                            "convention": "minor",
                            "refactor": "minor",
                            "info": "minor"
                        }
                        issues.append(Issue(
                            category="Static Analysis",
                            description=f"{item['message-id']}: {item['message']}",
                            line_number=item['line'],
                            severity=severity_map.get(item['type'], "medium"),
                            confidence_score=1.0, # Static analysis is deterministic
                            suggestion=f"Fix {item['symbol']}"
                        ))
                except json.JSONDecodeError:
                    pass # Pylint might output non-json if something goes wrong
        except Exception as e:
            print(f"Error running pylint: {e}")
            
        return issues

    def _run_radon(self, code: str) -> ComplexityAnalysis:
        try:
            # Cyclomatic Complexity
            cc_blocks = radon_cc.cc_visit(code)
            total_cc = sum(block.complexity for block in cc_blocks)
            avg_cc = total_cc / len(cc_blocks) if cc_blocks else 0
            
            # Maintainability Index
            mi_score = radon_metrics.mi_visit(code, multi=True)
            
            return ComplexityAnalysis(
                time_complexity="O(?)", # Radon doesn't give Big O
                space_complexity="O(?)",
                cyclomatic_complexity=int(avg_cc), # Average CC
                maintainability_index=mi_score
            )
        except Exception as e:
            print(f"Error running radon: {e}")
            return ComplexityAnalysis(time_complexity="Unknown", space_complexity="Unknown")
