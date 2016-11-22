# -*- coding: utf-8 -*-
"""Run all unittests"""

import subprocess

subprocess.call(['python3', '-m', 'unittest',
                 'test/test_rm_symbols_tags_empty_lines.py',
                 'test/test_paragraphs_to_sentences_eng.py',
                 'test/test_paragraphs_to_sentences_cht.py',
                 'test/test_sentences_to_terms_eng.py',
                 'test/test_sentences_to_terms_cht.py',
                 'test/test_terms_to_term_pairs_freq.py',
                 'test/test_term_pair_freq_to_db.py',
                 ])

