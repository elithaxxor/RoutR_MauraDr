import unittest
from web.src.baseline import check_baseline


class TestBaseline(unittest.TestCase):
    def test_check_baseline_flags_ports(self):
        host_data = {'1.1.1.1': {'open_ports': [21, 80]}}
        result = check_baseline(host_data, {'recommended_ports_closed': [21, 80]})
        alerts = result['1.1.1.1'].get('baseline_alerts')
        self.assertTrue(alerts)


if __name__ == '__main__':
    unittest.main()
