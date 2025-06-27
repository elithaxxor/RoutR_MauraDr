"""API version 2 routes."""

"""API version 2 routes."""
from __future__ import annotations

import uuid
from pathlib import Path
from flask import request, send_file
from flask_restx import Namespace, Resource

from routR.tools.runner import run_jobs, load_jobs, REPORT_DIR
from routR.tools import wrappers

import asyncio

api_v2 = Namespace("api_v2", description="RoutR tools API")


@api_v2.route("/scan")
class Scan(Resource):
    def post(self):
        job_data = request.get_json()
        jobs = job_data.get("jobs", []) if job_data else []
        job_id = str(uuid.uuid4())
        report = asyncio.run(run_jobs(jobs, job_id))
        return {"id": job_id, "results": report["results"]}, 200


@api_v2.route("/report/<string:job_id>")
class Report(Resource):
    def get(self, job_id: str):
        fmt = request.args.get("format", "json")
        path = REPORT_DIR / f"{job_id}.json"
        if not path.exists():
            return {"error": "report not found"}, 404
        if fmt == "json":
            return Path(path).read_text(), 200, {"Content-Type": "application/json"}
        elif fmt == "html":
            return Path(path).read_text(), 200, {"Content-Type": "text/html"}
        elif fmt == "pdf":
            return send_file(str(path), mimetype="application/pdf")
        return {"error": "unsupported format"}, 400


@api_v2.route("/health")
class Health(Resource):
    def get(self):
        tools = [
            "masscan",
            "arp-scan",
            "hydra",
            "gvm-cli",
            "upnpc",
            "nikto",
            "sqlmap",
            "pgrok",
            "hcxdumptool",
        ]
        status = {t: wrappers.is_available(t) for t in tools}
        return {"ready": True, "tools": status}, 200
