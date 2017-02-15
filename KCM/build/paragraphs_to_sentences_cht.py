# -*- coding: utf-8 -*-
def paragraphs_to_sentences_cht(if_name, of_name):
    """Input file of paragraphs, output file of sentences (Chinese)"""
    def paragraph_to_sentences(line):
        """Return input string (paragraph) with sentences split by '\n'

        Args:
            line: input paragraph string

        Returns:
            input paragraph with sentences split by '\n'
        """
        return line.replace('。', '。\n')
    """Main function"""
    with open(if_name, 'r') as input_file:
        with open(of_name, 'w') as output_file:
            for line in input_file:
                output_file.write(paragraph_to_sentences(line))