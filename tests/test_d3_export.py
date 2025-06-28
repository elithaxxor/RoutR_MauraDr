import unittest
import tempfile
from pathlib import Path
from web.src.network_map import export_d3_html, build_topology


class TestD3Export(unittest.TestCase):
    def test_export_d3_html(self):
        g = build_topology(['1.1.1.2'], router_ip='1.1.1.1')
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'graph.html'
            export_d3_html(g, p)
            self.assertTrue(p.exists())


if __name__ == '__main__':
    unittest.main()
