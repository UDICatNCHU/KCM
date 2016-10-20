"""Unittest for sentences_to_terms_eng.py"""

import unittest
from collections import namedtuple

from test_sentences_to_terms import TestSentencesToTerms


class TestSentencesToTermsEng(TestSentencesToTerms):
    @classmethod
    def setUpClass(cls):
        Data = namedtuple('Data', ['input', 'expected'])
        cls.data_tuple = (
            Data('An apple a day, keeps the doctor away.',
                 '/apple/day/doctor'),
            Data('The Monarchs of Portugal ruled from the establishment of the Kingdom of Portugal',
                 '/monarch/portugal/establishment/kingdom/portugal')
        )

        cls.common_init(lang='eng')

    def test_term_as_expected(self):
        self._test_term_as_expected()


if __name__ == '__main__':
    unittest.main()
