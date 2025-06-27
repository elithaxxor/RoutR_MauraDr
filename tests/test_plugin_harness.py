import tempfile
import textwrap
import unittest
from pathlib import Path

from web.src import plugin_harness

class TestPluginHarness(unittest.TestCase):
    def test_validate_plugin(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'p.py'
            p.write_text(textwrap.dedent('''
                def register():
                    return {"ok": True}
            '''))
            self.assertTrue(plugin_harness.validate_plugin(p))
            results = plugin_harness.run_tests([p])
            self.assertTrue(results[str(p)])
