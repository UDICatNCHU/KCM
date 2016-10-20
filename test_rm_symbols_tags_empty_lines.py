"""Unittest for rm_symbols_tags_empty_lines.py"""

import unittest

from rm_symbols_tags_empty_lines import is_empty_line
from rm_symbols_tags_empty_lines import has_tag
from rm_symbols_tags_empty_lines import symbols_removed


class TestRmSymbolsTagsEmptyLines(unittest.TestCase):
    def test_is_empty_line(self):
        s = '''


        '''
        self.assertTrue(is_empty_line(s))
        s = '    a '
        self.assertFalse(is_empty_line(s))

    def test_has_tag(self):
        s = '<doc wertewt>'
        self.assertTrue(has_tag(s))
        s = '</doc>'
        self.assertTrue(has_tag(s))
        s = 'a bwer iwoer'
        self.assertFalse(has_tag(s))

    def test_symbols_removed(self):
        s = '[[aaa]]《《bbb》》'
        s = symbols_removed(s)
        self.assertNotIn('[', s)
        self.assertNotIn(']', s)
        self.assertNotIn('《', s)
        self.assertNotIn('》', s)


if __name__ == '__main__':
    unittest.main()
