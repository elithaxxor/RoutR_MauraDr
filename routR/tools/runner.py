"""Tool dispatcher for running scans concurrently."""

from __future__ import annotations

import argparse
import asyncio
import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional
import sys

from . import wrappers

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)


async def _run_job(job: Dict[str, Any]) -> Dict[str, Any]:
    tool = job.get("tool")
    args = job.get("args", [])
    func = getattr(wrappers, f"run_{tool}", None)
    if not func:
        return {"error": f"unknown tool {tool}"}
    result = await func(*args)
    return {tool: result}


async def run_jobs(jobs: List[Dict[str, Any]], job_id: str) -> Dict[str, Any]:
    tasks = [asyncio.create_task(_run_job(j)) for j in jobs]
    results: List[Dict[str, Any]] = await asyncio.gather(*tasks)
    report = {"id": job_id, "results": results}
    path = REPORT_DIR / f"{job_id}.json"
    path.write_text(json.dumps(report, indent=2))
    return report


def load_jobs(path: Optional[Path]) -> List[Dict[str, Any]]:
    data = json.load(path.open()) if path else json.load(sys.stdin)
    return data.get("jobs", [])


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="RoutR tool runner")
    parser.add_argument("--job-file", type=Path, help="JSON job description")
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path("reports"),
        help="directory to store generated reports",
    )
    args = parser.parse_args(argv)

    global REPORT_DIR
    REPORT_DIR = args.report_dir
    REPORT_DIR.mkdir(exist_ok=True)

    jobs = load_jobs(args.job_file)
    job_id = str(uuid.uuid4())
    asyncio.run(run_jobs(jobs, job_id))
    print(job_id)


if __name__ == "__main__":
    main()
