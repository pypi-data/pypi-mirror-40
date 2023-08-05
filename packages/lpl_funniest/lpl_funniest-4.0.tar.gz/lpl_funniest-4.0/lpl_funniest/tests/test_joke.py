from unittest import TestCase

import lpl_funniest

class TestJoke(TestCase):
    def test_is_string(self):
        s = lpl_funniest.joke()
        self.assertTrue(isinstance(s, basestring))

    def test_joke1(self):
        lpl_funniest.entry.joke1()

    def test_joke2(self):
        lpl_funniest.entry.joke2()
