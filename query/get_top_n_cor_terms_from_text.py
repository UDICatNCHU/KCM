"""Print out top N correlated terms from text file"""

import queue
import argparse
import subprocess
from collections import OrderedDict
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from KCM import KCM

def get_args():
    """Get args

    Returns:
        args: the args object, args.term, args.N, args.min_freq, args.lang
    """

    parser = argparse.ArgumentParser(description='Get top N correlated terms')
    parser.add_argument('-i', '--input_file',
                        help='input file', required=True)
    parser.add_argument('-t', '--base_term',
                        help='base term used to search for correlated terms',
                        default=None)
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


def get_cor_term_freq_pq(if_name, base_term, min_freq):
    """Return minimum priority queue of tuple(frequency, correlated terms)

    2 tuple first compare the 1st item, which is the frequency

    Args:
        if_name: input file name
        base_term: base term used to find correlated terms
        min_freq: minimum frequency of correlated terms

    Returns:
        minimum priority queue of (freq, cor_term)
    """
    pq = queue.PriorityQueue()

    # Case1: base_term cor_term freq
    try:
        ret_byte = subprocess.check_output(
            ['grep', '^{base_term} '.format(**locals()), if_name])
        for line in ret_byte.decode().split('\n')[:-1]:  # last is empty line
            (_, cor_term, freq) = line.split(' ')
            if int(freq) < min_freq:
                continue

            pq.put((-int(freq), cor_term))

    except subprocess.CalledProcessError as e:  # grep found nothing
        pass

    # Case2: cor_term base_term freq
    try:
        ret_byte = subprocess.check_output(
            ['grep', ' {base_term} '.format(**locals()), if_name])
        for line in ret_byte.decode().split('\n')[:-1]:  # last is empty line
            (cor_term, _, freq) = line.split(' ')
            if int(freq) < min_freq:
                continue

            pq.put((-int(freq), cor_term))

    except subprocess.CalledProcessError as e:  # grep found nothing
        pass

    return pq


def print_top_n_cor_terms(pq, n):
    """Print top n correlated terms from priority queue

    Args:
        pq: priority queue of tuple(frequency, correlated terms)
        n: number of terms to be printed
    """
    jsonResult = OrderedDict()
    count = 0
    while not pq.empty() and count < n:
        count += 1
        (freq, cor_term) = pq.get()
        freq *= -1
        print('{cor_term} {freq}'.format(**locals()))
        jsonResult[cor_term] = freq
    return jsonResult
    

def get_term_pair_freq_pq(if_name, min_freq):
    """Return minimum priority queue of tuple(frequency, term pairs)

    2 tuple first compare the 1st item, which is the frequency

    Args:
        if_name: input file name
        min_freq: minimum frequency of term pairs

    Returns:
        minimum priority queue
    """
    pq = queue.PriorityQueue()

    with open(if_name, 'r') as file:
        for line in file:
            try:
                (first_term, second_term, freq) = line.split()
            except ValueError:  # line without 3 items
                # print('error line:', line)
                continue
            if int(freq) < min_freq:
                continue
            pq.put((-int(freq), (first_term, second_term)))

    return pq


def print_top_n_term_pairs(pq, n):
    """Print top n term pairs from priority queue

    Args:
        pq: priority queue of tuple(frequency, term pairs)
        n: number of term pairs to be printed
    """
    count = 0
    while not pq.empty() and count < n:
        count += 1
        (freq, (term1, term2)) = pq.get()
        freq *= -1
        print('{term1} {term2} {freq}'.format(**locals()))


def main():
    """Main function"""
    args = get_args()
    kcmObject = KCM()
    if args.base_term:  # print top n correlated terms
        pq = get_cor_term_freq_pq(args.input_file, args.base_term,
                                  args.min_freq)
        kcmObject.start(args.base_term, print_top_n_cor_terms, pq, args.term_count)
    else:  # print top n term pairs
        pq = get_term_pair_freq_pq(args.input_file, args.min_freq)
        print_top_n_term_pairs(pq, args.term_count)


if __name__ == '__main__':
    main()
