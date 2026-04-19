import logging
import sys
from typing import Optional

class HITLLogger:
    def __init__(self, name: str = "HITL_Agent"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Use a simple format that matches the requirements
        formatter = logging.Formatter('%(message)s')
        
        # Console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def log_input(self, user_input: str):
        self.logger.info(f"\n[INPUT]\n{user_input}")

    def log_action(self, action: str):
        self.logger.info(f"\n[ACTION GENERATED]\n{action}")

    def log_risk(self, is_high: bool):
        status = "YES" if is_high else "NO"
        self.logger.info(f"\n[RISK DETECTED] {status}")

    def log_approval_request(self, method: str):
        self.logger.info(f"\n[APPROVAL REQUEST SENT] via {method}")

    def log_approval_status(self, approved: bool):
        status = "APPROVED" if approved else "REJECTED"
        self.logger.info(f"\n[APPROVAL STATUS] {status}")

    def log_result(self, result: str):
        self.logger.info(f"\n[FINAL RESULT]\n{result}")

    def info(self, msg: str):
        self.logger.info(msg)

    def error(self, msg: str):
        self.logger.error(f"[ERROR] {msg}")

logger = HITLLogger()
