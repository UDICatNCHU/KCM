# -*- coding: utf-8 -*-
"""Input text file of terms, output text file of term pair and frequency"""

import argparse
import itertools
import collections
import logging


def get_term_list(line, term_len):
    """Return a term list with the specific term length

    Args:
        line: input line of terms, should be '/term1/term2/...'
        term_len: desire length of the return terms

    Returns:
        list of terms of term_len
    """
    black_list = ('',)
    # don't know why terms str such as
    # /sylvester/speech/issue/letter/s/sweetie-pie//s//name
    # will be generated, so filter '' here

    return [term for term in line[1:-1].split('/')
            if term not in black_list and len(term) == term_len]
    # remove line[0]: '/' and line[last]: '\n'
    # python2 cht version used to use pat = u'[\u4e00-\u9fa5]'  一 to 龥
    # and remove term that (re.search(pat, y.decode('utf-8')) == None)
    # not sure if it's still needed in python3


def get_term_lists(line, term1_len, term2_len):
    """Return a tuple of 2 term list with the specific term lengths

    Args:
        line: input line of terms, should be '/term1/term2/...'
        term1_len: desire length of the 1st return terms
        term2_len: desire length of the 2nd return terms

    Returns:
        tuple of 2 list of terms of term1_len, term2_len respectively
    """
    black_list = ('',)

    terms = [term for term in line[1:-1].split('/') if term not in black_list]

    term1s = [term for term in terms if len(term) == term1_len]
    term2s = [term for term in terms if len(term) == term2_len]

    return (term1s, term2s)


def yield_term_pairs_from_term_lists(term1s, term2s):
    """Return generator of all combinations of (term1, term2)

    This function generates all the combinations of (term1 from term1s, term2..)

    Args:
        term1s: list of term1s
        term2s: list of term2s

    Returns:
        generator of term pairs (term1, term2)
    """
    for term1 in term1s:
        for term2 in term2s:
            yield (term1, term2)


def yield_term_pairs_from_term_list(term_list):
    """Return generator of all combinations of tuple(term_pair)

    ['an', 'apple', 'a'] generates ['a', 'an'], ['a', 'apple'], ...
    Pairs will always be ['apple', 'doctor'], not ['doctor', 'apple'].

    Args:
        term_list: list of terms

    Returns:
        generator of term pairs
    """
    for term_pair in itertools.combinations(term_list, 2):
        if term_pair[0] == term_pair[1]:  # two terms are identical
            continue
        yield sorted(list(term_pair))


def yield_term_pair_freq_str(if_name, min_freq, term1_len, term2_len):
    """Generate term pair frequency str

    Args:
        if_name: name of input file of '/term1/term2\n/t1/t2/t3\n....'
        min_freq: minimum frequency of a term pair to be stored
        term1_len: length of term1
        term2_len: length of term2
    """
    tp_f_d = collections.defaultdict(int)
    with open(if_name, 'r') as input_file:
        for line in input_file:
            if term1_len == term2_len:
                term_len = term1_len
                terms = get_term_list(line, term_len)
                for t1, t2 in yield_term_pairs_from_term_list(terms):
                    tp_f_d['{t1} {t2}'.format(**locals())] += 1

            else:  # term1 len != term2 len
                (term1s, term2s) = get_term_lists(line, term1_len, term2_len)
                for t1, t2 in yield_term_pairs_from_term_lists(term1s, term2s):
                    tp_f_d['{t1} {t2}'.format(**locals())] += 1

    for tp_str, f in tp_f_d.items():
        if not f < min_freq:
            yield '{tp_str} {f}\n'.format(**locals())


def get_args():
    """Return the args

    Returns:
        (input_file_name, output_file_name, min_freq, max_term_len)

        min_freq: the minimum frequency of a term pair to be stored
    """
    parser = argparse.ArgumentParser(
        description='generate term pairs from terms')
    parser.add_argument('-i', '--input', help='input file', required=True)
    parser.add_argument('-o', '--output', help='output file', required=True)
    parser.add_argument('-m', '--min_freq',
                        help='minimum frequency (default: %(default)s)',
                        type=int, default=3)
    parser.add_argument('-l', '--max_term_len',
                        help='maximum length of terms (default: %(default)s)',
                        type=int, default=10)

    args = parser.parse_args()
    return args.input, args.output, args.min_freq, args.max_term_len


def main():
    """Main function"""
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

    logging.info('Begin of script')
    (if_name, of_name, min_freq, max_term_len) = get_args()
    with open(of_name, 'w') as output_file:
        for term1_len in range(1, max_term_len + 1):
            for term2_len in range(term1_len, max_term_len + 1):
                # generate term_pair_freq_(term1_len)-(term2_len)?
                logging.info('begin term1 length: {term1_len}, '
                             'term2 length: {term2_len}'
                             '\n\n'.format(**locals()))

                for tp_f_str in yield_term_pair_freq_str(if_name, min_freq,
                                                         term1_len, term2_len):
                    output_file.write(tp_f_str)

                logging.info('term1 length: {term1_len}, '
                             'term2 length: {term2_len} finished\n\n'
                             .format(**locals()))


if __name__ == "__main__":
    main()
