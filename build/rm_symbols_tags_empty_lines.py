# -*- coding: utf-8 -*-
"""Input text file, remove symbols, tags and empty lines, output to file"""

import re
import argparse


def is_empty_line(line):
    """Return true if input string is an empty line

    Args:
        line: input string

    Returns:
        True if input is empty line, otherwise False
    """
    return line.rstrip() == ''


def has_tag(line):
    """Return true if input string has doc tag (<doc...> or </doc>)

    Args:
        line: input string

    Returns:
        True if input has doc tag, otherwise False
    """
    return '<doc' in line or '</doc>' in line


def symbols_removed(line):
    """Return input string with symbols ([]《 》) removed

    Args:
        line: input string

    Returns:
        input string with symbols removed
    """
    symbols = re.escape('[]《 》')
    return re.sub('[{symbols}]'.format(**locals()), '', line)


def get_args():
    """Return the args

    Returns:
        input_file_name, output_file_name
    """
    parser = argparse.ArgumentParser(
        description='Remove symbols, tags, and empty lines.')
    parser.add_argument('-i', '--input', help='input file', required=True)
    parser.add_argument('-o', '--output', help='output file', required=True)

    args = parser.parse_args()
    return args.input, args.output


def main():
    """Main function"""
    if_name, of_name = get_args()
    print('-----------------------')
    print(if_name)
    print('-----------------------')
    with open(if_name, 'r', encoding='utf-8') as input_file:
        with open(of_name, 'a', encoding='utf-8') as output_file:
            for line in input_file:
                if is_empty_line(line):
                    continue
                if has_tag(line):
                    continue
                output_file.write(symbols_removed(line))


if __name__ == '__main__':
    main()
