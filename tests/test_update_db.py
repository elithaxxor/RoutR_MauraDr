import json
import unittest
from unittest import mock
from pathlib import Path

from web.src import update_db

class TestUpdateDB(unittest.TestCase):
    def test_update_db(self):
        data = {"Example": {"1.0": []}}
        fake = mock.MagicMock()
        fake.__enter__.return_value.read.return_value = json.dumps(data).encode()
        fake.__enter__.return_value.__iter__.return_value = []
        with mock.patch("web.src.update_db.urlopen", return_value=fake):
            self.assertTrue(update_db.update_database("http://example"))
            self.assertTrue(Path(update_db.CVE_DB).exists())
            with open(update_db.CVE_DB, "r", encoding="utf-8") as f:
                saved = json.load(f)
            self.assertEqual(saved, data)
