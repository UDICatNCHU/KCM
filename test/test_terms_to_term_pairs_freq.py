"""Unittest for terms_to_term_pairs_freq.py"""

import unittest
from collections import namedtuple

from build.terms_to_term_pair_freq import get_term_list
from build.terms_to_term_pair_freq import yield_term_pairs_from_term_list


class TestTermsToTermPairs(unittest.TestCase):
    def test_get_term_list(self):
        Data = namedtuple('Data', ['input_line', 'term_len', 'expected'])
        data_tuple = (
            Data('/宗教/神明/信仰/宗教/信仰/宇宙/信仰////\n', 2,
                 ['宗教', '神明', '信仰', '宗教', '信仰', '宇宙', '信仰']),
            Data('/宗教\n', 2,
                 ['宗教'])
        )

        for data in data_tuple:
            self.assertEqual(get_term_list(data.input_line, data.term_len),
                             data.expected)

    def test_yield_term_pairs_from_term_list(self):
        Data = namedtuple('Data', ['input', 'expected'])
        data_tuple = (
            Data(['宗教', '神明', '信仰'],
                 (['宗教', '神明'], ['信仰', '宗教'], ['信仰', '神明'])),
            # if only one term is given, there will be no output
            Data(['宗教'],
                 ()),
            # identical terms should not be able to generate term pairs
            Data(['山東省', '湖北省', '山東省'],
                 (['山東省', '湖北省'], ['山東省', '湖北省']))
        )

        for data in data_tuple:
            self.assertEqual(tuple(yield_term_pairs_from_term_list(data.input)),
                             data.expected)


if __name__ == '__main__':
    unittest.main()
