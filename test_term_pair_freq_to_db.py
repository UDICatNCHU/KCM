import os
import unittest

import sqlite3
from term_pair_freq_to_db import create_table
from term_pair_freq_to_db import update_data_into_db


class MyTestCase(unittest.TestCase):
    def test_insert_data_into_db(self):
        pass

    def test_update_data_into_db(self):
        # preparation
        with open('temp.txt', 'w') as temp_file:
            temp_file.write('5566 金鐘獎 10\n')

        conn = sqlite3.connect('temp.db')
        c = conn.cursor()

        create_table(c)

        with open('temp.txt', 'r') as input_file:
            update_data_into_db(input_file, c)

        result = c.execute('SELECT base_term, cor_term, freq '
                           'FROM base_term_cor_term_freq').fetchall()

        # must remove files before assert
        # os.remove('temp.txt')
        # os.remove('temp.db')

        self.assertEqual(result,
                         [('5566', '金鐘獎', 10), ('金鐘獎', '5566', 10)])

        # This is an update
        with open('temp.txt', 'r') as input_file:
            # add 10 to 5566 金鐘獎
            update_data_into_db(input_file, c)

        result = c.execute('SELECT base_term, cor_term, freq '
                           'FROM base_term_cor_term_freq').fetchall()

        # must remove files before assert
        os.remove('temp.txt')
        os.remove('temp.db')

        self.assertEqual(result,
                         [('5566', '金鐘獎', 20), ('金鐘獎', '5566', 20)])


if __name__ == '__main__':
    unittest.main()
