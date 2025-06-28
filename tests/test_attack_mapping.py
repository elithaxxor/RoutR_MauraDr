import unittest
from web.src.attack_mapping import correlate_attack


class TestAttackMapping(unittest.TestCase):
    def test_correlate_attack_ports(self):
        data = {'1.1.1.1': {'open_ports': [23]}}
        result = correlate_attack(data)
        self.assertIn('T1041', result['1.1.1.1'].get('attack_techniques', []))


if __name__ == '__main__':
    unittest.main()
