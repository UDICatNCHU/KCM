"""Unittest for test_sentences_to_terms.py"""

import unittest
from collections import namedtuple

from test_sentences_to_terms import TestSentencesToTerms


# use tests modified from https://github.com/yanyiwu/cppjieba
class TestSentencesToTermsCht(TestSentencesToTerms):
    @classmethod
    def setUpClass(cls):
        Data = namedtuple('Data', ['input', 'expected'])
        cls.data_tuple = (
            Data('我來到北京清華大學',
                 '/北京/清華大學'),
            Data('小明碩士畢業於中國科學院計算所，後在日本京都大學深造',
                 '/小明/碩士/畢業/於/中國科學院/計算所/後/日本京都大學'),
            Data('令狐沖是雲端計算行業的專家',
                 '/令狐沖/雲端/行業/專家'),
        )

        cls.common_init(lang='cht')

    def test_term_as_expected(self):
        self._test_term_as_expected()


if __name__ == '__main__':
    unittest.main()
