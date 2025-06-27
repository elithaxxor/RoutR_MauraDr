"""Aggregate scan results from multiple machines."""
from pathlib import Path
import json
from typing import Dict, List


class ResultDashboard:
    def __init__(self, results_dir: Path):
        self.results_dir = results_dir

    def load_results(self) -> List[Dict]:
        data = []
        for path in self.results_dir.glob('*.json'):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data.append(json.load(f))
            except Exception:
                continue
        return data

    def summarize_ports(self) -> Dict[str, int]:
        summary: Dict[str, int] = {}
        for result in self.load_results():
            for port in result.get('open_ports', []):
                summary[str(port)] = summary.get(str(port), 0) + 1
        return summary

