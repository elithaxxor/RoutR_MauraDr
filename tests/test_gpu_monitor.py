import asyncio
import unittest
from unittest import mock

from web.src import gpu_monitor

class TestGPUMonitor(unittest.TestCase):
    def test_parse_nvidia(self):
        async def run():
            with mock.patch("shutil.which", return_value="/usr/bin/nvidia-smi"):
                with mock.patch("web.src.gpu_monitor._run_cmd", return_value="10,512\n"):
                    stats = await gpu_monitor.get_gpu_stats()
                    self.assertEqual(stats, [{"util": 10, "mem": 512}])
        asyncio.run(run())

    def test_no_gpu(self):
        async def run():
            with mock.patch("shutil.which", return_value=None):
                stats = await gpu_monitor.get_gpu_stats()
                self.assertEqual(stats, [])
        asyncio.run(run())

if __name__ == "__main__":
    unittest.main()
