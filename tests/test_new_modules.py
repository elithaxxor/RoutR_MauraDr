import importlib
import unittest

MODULES = [
    'web.src.gui',
    'web.src.integrations.vuln_scanners',
    'web.src.firmware',
    'web.src.scheduler',
    'web.src.notifications'
]


class TestImports(unittest.TestCase):
    def test_imports(self):
        for mod in MODULES:
            importlib.import_module(mod)


if __name__ == '__main__':
    unittest.main()
