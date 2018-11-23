import unittest
from bpmn_crawler import crawler


class TestCrawler(unittest.TestCase):

     def test_clone_repository(self):
         self.assertEqual(crawler.clone_repository("ViktorStefanko/BPMN_Crawler"), "BPMN_Crawler")
         self.assertNotEqual(crawler.clone_repository("ViktorStefanko/"), "BPMN_Crawler")


if __name__ == '__main__':
    unittest.main()
