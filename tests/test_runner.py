import io
import json
import unittest
import tempfile
from pathlib import Path
from unittest import mock

from routR.tools.runner import load_jobs


class TestRunner(unittest.TestCase):
    def test_load_jobs_from_stdin(self):
        job_data = {"jobs": [{"tool": "masscan", "args": ["127.0.0.1"]}]}
        buf = io.StringIO(json.dumps(job_data))
        with mock.patch("sys.stdin", buf):
            jobs = load_jobs(None)
        self.assertEqual(jobs, job_data["jobs"])

    def test_load_jobs_from_file(self):
        job_data = {"jobs": [{"tool": "masscan", "args": ["127.0.0.1"]}]}
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "jobs.json"
            p.write_text(json.dumps(job_data))
            jobs = load_jobs(p)
        self.assertEqual(jobs, job_data["jobs"])


if __name__ == "__main__":
    unittest.main()
