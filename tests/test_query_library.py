import unittest
from web.src import query_library

class TestQueryLibrary(unittest.TestCase):
    def test_save_and_get(self):
        query_library.save_query('shodan', 'unittest', 'testquery')
        q = query_library.get_query('shodan', 'unittest')
        self.assertEqual(q, 'testquery')
        queries = query_library.list_queries('shodan')
        self.assertIn('unittest', queries)

if __name__ == '__main__':
    unittest.main()
