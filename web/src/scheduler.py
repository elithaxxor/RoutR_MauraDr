"""Simple adaptive scan scheduler."""
import sched
import time
from typing import Callable, Dict

class AdaptiveScheduler:
    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.last_results: Dict[str, int] = {}

    def schedule_scan(self, target: str, func: Callable, delay: int = 3600):
        """Schedule a scan function with adaptive delay."""
        risk = self.last_results.get(target, 1)
        interval = max(delay // risk, 60)
        self.scheduler.enter(interval, 1, self.run_job, (target, func, delay))

    def run_job(self, target: str, func: Callable, delay: int):
        result = func(target)
        if isinstance(result, dict):
            score = result.get('score', 1)
            self.last_results[target] = score
        self.schedule_scan(target, func, delay)

    def run(self):
        self.scheduler.run()
