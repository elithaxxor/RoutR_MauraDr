import io
import json
import unittest
import tempfile
from pathlib import Path
from unittest import mock
from tempfile import TemporaryDirectory
from pathlib import Path

from routR.tools import runner


class TestRunner(unittest.TestCase):
    def test_load_jobs_from_stdin(self):
        job_data = {"jobs": [{"tool": "masscan", "args": ["127.0.0.1"]}]}
        buf = io.StringIO(json.dumps(job_data))
        with mock.patch("sys.stdin", buf):
            jobs = runner.load_jobs(None)
        self.assertEqual(jobs, job_data["jobs"])

    def test_load_jobs_from_file(self):
        job_data = {"jobs": [{"tool": "masscan", "args": ["127.0.0.1"]}]}
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "jobs.json"
            p.write_text(json.dumps(job_data))
            jobs = runner.load_jobs(p)
        self.assertEqual(jobs, job_data["jobs"])
    def test_main_report_dir(self):
        job_data = {"jobs": []}
        with TemporaryDirectory() as tmpdir:
            job_file = Path(tmpdir) / "jobs.json"
            job_file.write_text(json.dumps(job_data))
            out = io.StringIO()
            with mock.patch("sys.stdout", out):
                runner.main(["--job-file", str(job_file), "--report-dir", tmpdir])
            job_id = out.getvalue().strip()
            report_path = Path(tmpdir) / f"{job_id}.json"
            self.assertTrue(report_path.exists())


if __name__ == "__main__":
    unittest.main()

