import unittest
import random

### Test Statement
from say import Statement

class TestAgent(unittest.TestCase):
    def test_cmp(self):
        self.assertTrue(Statement(5, 3) < Statement(5, 4))
        self.assertTrue(Statement(2, 4) < Statement(3, 2))
        self.assertTrue(Statement(3, 4) < Statement(2, 1))
        self.assertTrue(Statement(3, 1) < Statement(4, 1))

        self.assertTrue(Statement(5, 2) < Statement(6, 3))
        self.assertTrue(Statement(5, 3) < Statement(6, 2))

        self.assertTrue(Statement(5, 4) > Statement(5, 3))
        self.assertTrue(Statement(3, 2) > Statement(2, 4))
        self.assertTrue(Statement(2, 1) > Statement(3, 4))
        self.assertTrue(Statement(4, 1) > Statement(3, 1))

        self.assertTrue(Statement(6, 3) > Statement(5, 2))
        self.assertTrue(Statement(6, 2) > Statement(5, 3))

        self.assertTrue(Statement(2, 3) == Statement(2, 3))
        self.assertTrue(Statement(2, 3) != Statement(2, 5))

        self.assertTrue(Statement(3, 5) > Statement(1, 6))

        self.assertTrue(Statement(4, 4) >= Statement(2, 1))

    def test_cmp_sound(self):
        for i in range(100):
            a = Statement(random.randrange(1, 20), random.randint(1, 6))
            b = Statement(random.randrange(1, 20), random.randint(1, 6))

            if a == b: continue
            if a > b: self.assertLess(a, b)
            if a < b: self.assertGreater(a, b)

if __name__ == "__main__":
    unittest.main()
