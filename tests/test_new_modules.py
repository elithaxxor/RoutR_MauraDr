import importlib
import unittest

MODULES = [
    'web.src.gui',
    'web.src.integrations.vuln_scanners',
    'web.src.integrations.shodan',
    'web.src.integrations.wigle',
    'web.src.integrations.shodan_client',
    'web.src.firmware',
    'web.src.scheduler',
    'web.src.notifications',
    'web.src.network_info',
    'web.src.router_ssh',
    'web.src.quick_scan',
    'web.src.net_services',
    'web.src.config_backup',
]


class TestImports(unittest.TestCase):
    def test_imports(self):
        for mod in MODULES:
            importlib.import_module(mod)


if __name__ == '__main__':
    unittest.main()
