#author: b8horpet

import unittest

from Physics import *


class TestPhysics(unittest.TestCase):
    def test_CreateWorld(self):
        try:
            w=World()
            self.assertTrue(True)
        except:
            self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
