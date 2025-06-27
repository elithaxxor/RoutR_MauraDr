import unittest
from unittest import mock

from web.src import internet_health


class TestInternetHealth(unittest.TestCase):
    def test_check_connectivity(self):
        with mock.patch("subprocess.run") as run:
            run.return_value.returncode = 0
            self.assertTrue(internet_health.check_connectivity())
            run.assert_called_once()

    def test_monitor_reboot(self):
        with mock.patch("web.src.internet_health.check_connectivity", side_effect=[False, False, True]):
            with mock.patch("web.src.internet_health.reboot_router") as reboot, \
                 mock.patch("web.src.internet_health.send_pushbullet") as notify, \
                 mock.patch("time.sleep"):
                internet_health.monitor(router_ip="1.1.1.1", interval=0, threshold=2, iterations=3)
                reboot.assert_called_once_with("1.1.1.1")
                notify.assert_called_once()


if __name__ == "__main__":
    unittest.main()
