#just a file to test pytest
from unittest import TestCase

class TryTesting(TestCase):
    def alwaysTrue(self):
        self.assertLess(1, 7)
        self.assertTrue(True)
