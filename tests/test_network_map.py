import unittest
from web.src.network_map import build_topology

class TestNetworkMap(unittest.TestCase):
    def test_build_topology(self):
        hosts = ['192.168.1.2', '192.168.1.3']
        graph = build_topology(hosts, router_ip='192.168.1.1', shodan_api_key=None)
        self.assertTrue(graph.has_node('192.168.1.1'))
        self.assertTrue(graph.has_edge('192.168.1.1', '192.168.1.2'))
        self.assertTrue(graph.has_edge('192.168.1.1', '192.168.1.3'))

if __name__ == '__main__':
    unittest.main()
