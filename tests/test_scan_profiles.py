import unittest
import os
from web.src import scan_profiles

class TestScanProfiles(unittest.TestCase):
    def setUp(self):
        if scan_profiles.PROFILE_FILE.exists():
            scan_profiles.PROFILE_FILE.unlink()

    def tearDown(self):
        if scan_profiles.PROFILE_FILE.exists():
            scan_profiles.PROFILE_FILE.unlink()

    def test_add_list_remove(self):
        scan_profiles.add_profile('test', '192.168.1.0/24', 'low', 60)
        profiles = scan_profiles.list_profiles()
        self.assertEqual(len(profiles), 1)
        self.assertEqual(profiles[0]['name'], 'test')
        scan_profiles.remove_profile('test')
        self.assertEqual(scan_profiles.list_profiles(), [])

if __name__ == '__main__':
    unittest.main()
