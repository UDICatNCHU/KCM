# -*- coding: utf-8 -*-
"""Input file of paragraphs, output file of sentences (English)"""

import argparse
import re

# http://stackoverflow.com/questions/25735644/python-regex-for-splitting-text-into-sentences-sentence-tokenizing
PATTERN = '(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s'


def paragraph_to_sentences(line):
    """Return input string (paragraph) with sentences split by '\n'

    Args:
        line: input paragraph string

    Returns:
        input paragraph with sentences split by '\n'
    """
    return re.sub(PATTERN, '\n', line)


def get_args():
    """Return the args

    Returns:
        input_file_name, output_file_name
    """
    parser = argparse.ArgumentParser(
        description='Split Paragraphs into separated sentences by \\n')
    parser.add_argument('-i', '--input', help='input file', required=True)
    parser.add_argument('-o', '--output', help='output file', required=True)

    args = parser.parse_args()
    return args.input, args.output


def main():
    """Main function"""
    (if_name, of_name) = get_args()
    with open(if_name, 'r') as input_file:
        with open(of_name, 'w') as output_file:
            for line in input_file:
                output_file.write(paragraph_to_sentences(line))


if __name__ == '__main__':
    main()
