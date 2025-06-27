import asyncio
import unittest
from unittest import mock

from routR.tools import wrappers


class TestWrappers(unittest.TestCase):
    def test_is_available(self):
        with mock.patch("shutil.which", return_value="/usr/bin/tool"):
            self.assertTrue(wrappers.is_available("masscan"))
        with mock.patch("shutil.which", return_value=None):
            self.assertFalse(wrappers.is_available("masscan"))

    def test_run_tool_missing(self):
        async def run():
            result = await wrappers.run_masscan("127.0.0.1")
            self.assertIn("error", result)

        with mock.patch("routR.tools.wrappers.is_available", return_value=False):
            asyncio.run(run())

    def test_run_hcxdumptool_missing(self):
        async def run():
            result = await wrappers.run_hcxdumptool("wlan0", "out.pcap")
            self.assertIn("error", result)

        with mock.patch("routR.tools.wrappers.is_available", return_value=False):
            asyncio.run(run())
