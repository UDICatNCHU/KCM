# -*- coding: utf-8 -*-
"""Input term pair frequency text file, output sqlite database file

If the db file specified by -o does not exist, simply create a db file,
then create table, insert data.

If the db file specified by -o exist, open the db, update or insert data.
"""

import argparse
import logging
import sqlite3
import os



def get_args():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    logging.info('Begin term_pair_freq_to_db.py')
    parser = argparse.ArgumentParser(
        description='Generate sqlite db file from term pair freq file')
    parser.add_argument('-i', '--input_file',
                        help='input term pair freq text file',
                        default='../../result/ChineseV2.model')
    parser.add_argument('-o', '--output_db',
                        help='Output db name (default: %(default)s)',
                        default='../../result/ChineseKCM.db')

    args = parser.parse_args()
    return args


def create_table(c):
    """Create the base term, correlated term, frequency table

    Args:
        c: sqlite database cursor
    """
    # TODO: raise error to indicate that the table already exist
    c.execute('''
        CREATE TABLE base_term_cor_term_freq
        (
          id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
          base_term varchar(100) NOT NULL,
          cor_term varchar(100) NOT NULL,
          freq INTEGER NOT NULL
        );
    ''')


def insert_data_into_db(input_file, c):
    """Insert term pair freq data into database from input file

    Args:
        input_file: Input file object.
        c: sqlite database cursor
    """
    for (line_count, line) in enumerate(input_file):
        try:
            (term1, term2, freq) = line.split()
            c.execute('''
                INSERT INTO base_term_cor_term_freq
                (base_term, cor_term, freq) VALUES (?, ?, ?);
                ''', (term1, term2, freq))
            c.execute('''
                INSERT INTO base_term_cor_term_freq
                (base_term, cor_term, freq) VALUES (?, ?, ?);
                ''', (term2, term1, freq))
        except ValueError:  # text file line data not 'term1 term2 freq'
            logging.info('line {line_count}, incorrect data: "{line}"'
                         .format(**locals()))
            continue


def get_previous_freq(base_term, cor_term, c):
    """The base_term, cor_term already exist in database

    Args:
        base_term: base term
        cor_term: correlated term
        c: database cursor

    Returns:
        freq if the base_term, cor_term combination exist,
        None if not exist
    """
    ret = c.execute('SELECT freq FROM base_term_cor_term_freq '
                    'WHERE base_term = ? AND cor_term = ?',
                    (base_term, cor_term)).fetchall()

    if ret:
        if len(ret) > 1:
            pass
            # TODO: Raise error because the base_term, cor_term combination
            # TODO: should be unique.
        freq = ret[0][0]
        return freq
    else:
        # query returned empty list, which means the combination does not exist
        return None


def update_data_into_db(input_file, c):
    """Update term pair freq data into database from input file

    Args:
        input_file: Input file object.
        c: sqlite database cursor
    """
    for (line_count, line) in enumerate(input_file):
        try:
            (term1, term2, freq) = line.split()
            freq = int(freq)  # str to int

            old_freq = get_previous_freq(term1, term2, c)
            if old_freq:
                freq += old_freq
                c.execute('UPDATE base_term_cor_term_freq SET freq = ? '
                          'WHERE base_term = ? AND cor_term = ?',
                          (freq, term1, term2))
                c.execute('UPDATE base_term_cor_term_freq SET freq = ? '
                          'WHERE base_term = ? AND cor_term = ?',
                          (freq, term2, term1))
            else:
                c.execute('''
                    INSERT INTO base_term_cor_term_freq
                    (base_term, cor_term, freq) VALUES (?, ?, ?);
                    ''', (term1, term2, freq))
                c.execute('''
                    INSERT INTO base_term_cor_term_freq
                    (base_term, cor_term, freq) VALUES (?, ?, ?);
                    ''', (term2, term1, freq))
        except ValueError:  # text file line data not 'term1 term2 freq'
            logging.info('line {line_count}, incorrect data: "{line}"'
                         .format(**locals()))
            continue


def indexing_db(c):
    """Create index for base term

    By creating index for base term, search speed goes from n to O(lg(n))

    Args:
        c: sqlite database cursor
    """
    c.execute('CREATE INDEX idx_base_term '
              'ON base_term_cor_term_freq(base_term, freq DESC, cor_term)')


def main():
    args = get_args()

    # First check if db exist

    if os.path.exists(args.output_db):  # db exist
        conn = sqlite3.connect(args.output_db)
        c = conn.cursor()
        with open(args.input_file, 'r') as input_file:
            update_data_into_db(input_file, c)

    else:  # db not exist
        conn = sqlite3.connect(args.output_db)
        c = conn.cursor()
        with open(args.input_file, 'r') as input_file:
            create_table(c)
            insert_data_into_db(input_file, c)
            indexing_db(c)

    conn.commit()


if __name__ == '__main__':
    main()
