import time
from typing import Dict, Any

class Monitoring:
    """
    Simple in-memory monitoring for API metrics.
    """
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.latencies = []

    def track_request(self):
        self.request_count += 1

    def track_error(self):
        self.error_count += 1

    def track_latency(self, latency: float):
        self.latencies.append(latency)
        # Keep only last 100 latencies for average calculation
        if len(self.latencies) > 100:
            self.latencies.pop(0)

    def get_metrics(self) -> Dict[str, Any]:
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0
        return {
            "total_requests": self.request_count,
            "total_errors": self.error_count,
            "avg_latency_seconds": round(avg_latency, 4),
            "error_rate": f"{(self.error_count / self.request_count * 100):.2f}%" if self.request_count > 0 else "0%"
        }

metrics_tracker = Monitoring()
