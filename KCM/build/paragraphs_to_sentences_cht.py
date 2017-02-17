# -*- coding: utf-8 -*-
def paragraphs_to_sentences_cht(if_name):
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
    for line in if_name:
        yield paragraph_to_sentences(line)