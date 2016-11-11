"""Unittests for paragraphs_to_sentences_eng.py"""

import unittest

from build.paragraphs_to_sentences_eng import paragraph_to_sentences


class TestParagraphsToSentencesEng(unittest.TestCase):
    def test_paragraph_to_sentences(self):
        input = 'Through the nearly 800 years which Portugal was a monarchy,' \
                'the kings held various other titles and pretensions. ' \
                'Two Kings of Portugal, Ferdinand I and Afonso V,' \
                'also claimed the crown of Castile. ' \
                'When the House of Habsburg came into power, ' \
                'the Kings of Spain, and Naples, also became Kings of Portugal. ' \
                'The House of Braganza brought numerous titles to the Portuguese Crown,' \
                'including King of Brazil and then Emperor of Brazil.'

        expec = 'Through the nearly 800 years which Portugal was a monarchy,' \
                'the kings held various other titles and pretensions.\n' \
                'Two Kings of Portugal, Ferdinand I and Afonso V,' \
                'also claimed the crown of Castile.\n' \
                'When the House of Habsburg came into power, ' \
                'the Kings of Spain, and Naples, also became Kings of Portugal.\n' \
                'The House of Braganza brought numerous titles to the Portuguese Crown,' \
                'including King of Brazil and then Emperor of Brazil.'

        self.maxDiff = None
        self.assertEqual(paragraph_to_sentences(input), expec)


if __name__ == '__main__':
    unittest.main()
