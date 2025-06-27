import io
import json
import unittest
from unittest import mock

from routR.tools.runner import load_jobs


class TestRunner(unittest.TestCase):
    def test_load_jobs_from_stdin(self):
        job_data = {"jobs": [{"tool": "masscan", "args": ["127.0.0.1"]}]}
        buf = io.StringIO(json.dumps(job_data))
        with mock.patch("sys.stdin", buf):
            jobs = load_jobs(None)
        self.assertEqual(jobs, job_data["jobs"])


if __name__ == "__main__":
    unittest.main()
