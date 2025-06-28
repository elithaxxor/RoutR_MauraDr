import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from web.src.certificate import check_certificate


class TestCertificate(unittest.TestCase):
    def test_check_certificate_error(self):
        info = check_certificate('localhost')
        self.assertIn('error', info)

    def _mock_ssl(self, cert):
        """Helper to patch ssl context and socket with provided cert."""
        mock_sock = MagicMock()
        mock_sock.__enter__.return_value = mock_sock
        mock_sock.__exit__.return_value = False
        mock_sock.getpeercert.return_value = cert
        mock_sock.settimeout.return_value = None
        mock_sock.connect.return_value = None
        mock_ctx = MagicMock()
        mock_ctx.wrap_socket.return_value = mock_sock
        return (
            patch('ssl.create_default_context', return_value=mock_ctx),
            patch('socket.socket', return_value=MagicMock()),
        )

    def test_parse_notafter_and_hostname_match(self):
        now = datetime(2023, 1, 1)
        expires = now + timedelta(days=5)
        cert = {
            'notAfter': expires.strftime('%b %d %H:%M:%S %Y GMT'),
            'subject': ((('commonName', 'example.com'),),),
        }
        ssl_patch, sock_patch = self._mock_ssl(cert)
        with ssl_patch, sock_patch, patch('web.src.certificate.datetime') as mock_dt:
            mock_dt.strptime = datetime.strptime
            mock_dt.utcnow.return_value = now
            info = check_certificate('example.com')
        self.assertEqual(info['days_left'], 5)
        self.assertTrue(info['hostname_match'])
        self.assertEqual(info['subject'], 'example.com')

    def test_wildcard_hostname_match(self):
        now = datetime(2023, 2, 1)
        expires = now + timedelta(days=1)
        cert = {
            'notAfter': expires.strftime('%b %d %H:%M:%S %Y GMT'),
            'subject': ((('commonName', '*.example.com'),),),
        }
        ssl_patch, sock_patch = self._mock_ssl(cert)
        with ssl_patch, sock_patch, patch('web.src.certificate.datetime') as mock_dt:
            mock_dt.strptime = datetime.strptime
            mock_dt.utcnow.return_value = now
            info = check_certificate('sub.example.com')
        self.assertTrue(info['hostname_match'])


if __name__ == '__main__':
    unittest.main()
