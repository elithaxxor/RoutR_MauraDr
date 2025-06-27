"""Schedule periodic exports of scan results."""
import sched
import time
from typing import Callable

from .utils import export_results, export_results_csv


class ExportScheduler:
    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def schedule(self, func: Callable[[], dict], interval: int = 3600, csv: bool = False):
        self.scheduler.enter(interval, 1, self._run_job, (func, interval, csv))

    def _run_job(self, func: Callable[[], dict], interval: int, csv: bool):
        data = func()
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        if csv:
            export_results_csv(data, f"scan_{timestamp}.csv")
        else:
            export_results(data, f"scan_{timestamp}.json")
        self.schedule(func, interval, csv)

    def run(self):
        self.scheduler.run()
