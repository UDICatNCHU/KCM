"""Base class for TestSentencesToTermsCht and TestSentencesToTermsEng"""

import unittest
import os
import subprocess


class TestSentencesToTerms(unittest.TestCase):
    @classmethod
    def gen_input_file(cls):
        with open('input_file', 'w') as input_file:
            for data in cls.data_tuple:
                input_file.write('{0}\n'.format(data.input))

    @classmethod
    def save_results(cls):
        with open('output_file', 'r') as output_file:
            cls.result_list = [x.rstrip() for x in output_file]
            # rstrip for removing \n
        os.remove('output_file')

    @classmethod
    def common_init(cls, lang):
        cls.gen_input_file()
        subprocess.call(['python', 'build/sentences_to_terms_{0}.py'.format(lang),
                         'input_file', '-o', 'output_file', '-m', 'w', '-s',
                         'n'])
        os.remove('input_file')

        cls.save_results()

    def _test_term_as_expected(self):
        for index, result in enumerate(self.result_list):
            self.assertEqual(self.data_tuple[index].expected, result)
