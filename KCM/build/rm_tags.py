# -*- coding: utf-8 -*-
import re
def rm_tags(if_name, of_name):
    """Input text file, remove symbols, tags and empty lines, output to file"""
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
    """Main function"""
    with open(if_name, 'r', encoding='utf-8') as input_file:
        with open(of_name, 'a', encoding='utf-8') as output_file:
            for line in input_file:
                if is_empty_line(line):
                    continue
                if has_tag(line):
                    continue
                output_file.write(symbols_removed(line))