import json
import os
from typing import List, Dict, Any

class AuditStorage:
    """
    Handles persistent storage of audit logs in a JSON file.
    """
    def __init__(self, log_file: str):
        self.log_file = log_file
        self._ensure_log_file()

    def _ensure_log_file(self):
        """
        Creates the log file and necessary directories if they don't exist.
        """
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                json.dump([], f)

    def save(self, log_entry: Dict[str, Any]):
        """
        Appends a new log entry to the JSON file.
        """
        try:
            # Read existing logs
            with open(self.log_file, "r") as f:
                logs = json.load(f)
            
            # Append new entry
            logs.append(log_entry)
            
            # Save back to file
            with open(self.log_file, "w") as f:
                json.dump(logs, f, indent=4)
        except (json.JSONDecodeError, FileNotFoundError):
            # If file is corrupted or missing, start fresh
            with open(self.log_file, "w") as f:
                json.dump([log_entry], f, indent=4)

    def load_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all audit logs from the file.
        """
        if not os.path.exists(self.log_file):
            return []
        
        try:
            with open(self.log_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def get_by_trace_id(self, trace_id: str) -> List[Dict[str, Any]]:
        """
        Filters logs by a specific trace ID.
        """
        all_logs = self.load_all()
        return [log for log in all_logs if log.get("trace_id") == trace_id]
