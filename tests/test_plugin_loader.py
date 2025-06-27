import unittest
from web.src.plugin_loader import load_plugins

class TestPluginLoader(unittest.TestCase):
    def test_loads_plugins(self):
        plugins = load_plugins()
        names = [p.name.lower() for p in plugins]
        for expected in ['example', 'shodanimport', 'wiglelookup', 'censysimport']:
            self.assertIn(expected, names)
        names = [p.name for p in plugins]
        self.assertIn('example', [n.lower() for n in names])
        self.assertIn('shodanimport', [n.lower() for n in names])

if __name__ == '__main__':
    unittest.main()
