import unittest
from bpmn_crawler import old_crawler


class TestCrawler(unittest.TestCase):

     def test_clone_repository(self):
         self.assertEqual(old_crawler.clone_repository("ViktorStefanko/BPMN_Crawler"), "BPMN_Crawler")
         self.assertNotEqual(old_crawler.clone_repository("ViktorStefanko/"), "BPMN_Crawler")


if __name__ == '__main__':
    unittest.main()
