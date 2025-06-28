import unittest
from web.src.certificate import check_certificate


class TestCertificate(unittest.TestCase):
    def test_check_certificate_error(self):
        info = check_certificate('localhost')
        self.assertIn('error', info)


if __name__ == '__main__':
    unittest.main()
