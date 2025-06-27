import importlib
import unittest

MODULES = [
    'web.src.gui',
    'web.src.integrations.vuln_scanners',
    'web.src.integrations.shodan',
    'web.src.integrations.wigle',
    'web.src.integrations.shodan_client',
    'web.src.integrations.censys_client',
    'web.src.firmware',
    'web.src.scheduler',
    'web.src.notifications',
    'web.src.network_info',
    'web.src.router_ssh',
    'web.src.quick_scan',
    'web.src.net_services',

    'web.src.config_backup',

    # Newly added feature modules
    'web.src.dependency_updates',
    'web.src.report_generator',
    'web.src.wireless_scanner',
    'web.src.container_audit',
    'web.src.inventory_import',
    'web.src.correlation',
    'web.src.export_scheduler',
# Additional feature modules
    'web.src.role_tokens',
    'web.src.result_dashboard',
    'web.src.ipv6_support',
    'web.src.plugin_marketplace',
    'web.src.mobile_companion',

]


class TestImports(unittest.TestCase):
    def test_imports(self):
        for mod in MODULES:
            importlib.import_module(mod)


if __name__ == '__main__':
    unittest.main()
