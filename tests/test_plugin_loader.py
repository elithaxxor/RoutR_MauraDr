import unittest
from web.src.plugin_loader import load_plugins

class TestPluginLoader(unittest.TestCase):
    def test_loads_plugins(self):
        plugins = load_plugins()
        names = [p.name.lower() for p in plugins]
        for expected in ['example', 'shodanimport', 'wiglelookup']:
            self.assertIn(expected, names)

if __name__ == '__main__':
    unittest.main()
