"""Unittest for paragraphs_to_sentences_cht.py"""

import unittest

from build.paragraphs_to_sentences_cht import paragraph_to_sentences


class TestParagraphsToSentencesCht(unittest.TestCase):
    def test_paragraph_to_sentences(self):
        input = '宗教是對神明的信仰與崇敬，或者一般而言，宗教就是一套信仰，' \
                '是對宇宙存在的解釋，通常包括信仰與儀式的遵從。' \
                '宗教常常有一部道德準則，以調整人類自身行爲。'

        expec = '宗教是對神明的信仰與崇敬，或者一般而言，宗教就是一套信仰，' \
                '是對宇宙存在的解釋，通常包括信仰與儀式的遵從。\n' \
                '宗教常常有一部道德準則，以調整人類自身行爲。\n'

        self.maxDiff = None
        self.assertEqual(paragraph_to_sentences(input), expec)


if __name__ == '__main__':
    unittest.main()
