# -*- coding: utf-8 -*-
"""Print out top n correlated terms from database"""

import argparse
import sqlite3


def get_top_n_terms(db_name, base_term, min_freq, term_count=None):
    """Return list of top n correlated terms

    Args:
        db_name: name of sqlite db file
        base_term: base term used to search for correlated terms
        min_freq: minimum occurrence frequency of correlated term
        term_count: number of correlated terms to be returned
    Returns:
        list of (correlated term, frequency string)
    """
    suffix = 'LIMIT ' + str(term_count) if term_count else ''
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    return c.execute('''
            SELECT cor_term, freq FROM base_term_cor_term_freq
            WHERE base_term = ? AND freq > ? ORDER BY freq DESC
           ''' + suffix, (base_term, min_freq)).fetchall()


def get_args():
    """Get args

    Returns:
        args: the args object, args.term, args.N, args.min_freq, args.lang
    """

    parser = argparse.ArgumentParser(description='Get top N correlated terms')
    parser.add_argument('-i', '--input_db',
                        help='input file', required=True)
    parser.add_argument('-t', '--base_term',
                        help='base term used to search for correlated terms',
                        required=True)
    parser.add_argument('-N', '--term_count',
                        help='number of correlated_terms/term_pairs needed\n'
                             '(default: %(default)s)',
                        type=int, default=10)
    parser.add_argument('-m', '--min_freq',
                        help='minimum frequency of correlated terms\n'
                             '(default: %(default)s)',
                        type=int, default=3)

    args = parser.parse_args()
    return args


def main():
    """Main function"""
    args = get_args()
    ret = get_top_n_terms(args.input_db, args.base_term,
                          args.min_freq, args.term_count)
    for data in ret:
        print(data)


if __name__ == '__main__':
    main()
