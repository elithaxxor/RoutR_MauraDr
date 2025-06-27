import unittest
from web.src import plugin_manager

class TestPluginManager(unittest.TestCase):
    def test_enable_disable(self):
        plugins = dict(plugin_manager.list_plugins())
        self.assertIn('example', plugins)
        plugin_manager.disable_plugin('example')
        plugins = dict(plugin_manager.list_plugins())
        self.assertFalse(plugins['example'])
        plugin_manager.enable_plugin('example')
        plugins = dict(plugin_manager.list_plugins())
        self.assertTrue(plugins['example'])

if __name__ == '__main__':
    unittest.main()
