#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KCM generating script

This script is used to generate KCM/TCM (Term correlated model).
The task is done by calling many other scripts
"""
from KCM.build.rm_tags import rm_tags
from KCM.build.paragraphs_to_sentences_cht import paragraphs_to_sentences_cht
from KCM.build.sentences_to_terms_cht import PosTokenizer
from KCM.build.terms_to_term_pair_freq import terms_to_term_pair_freq

import json, pymongo
from pymongo import MongoClient
import os, queue, time, logging, errno, argparse
from pathlib import Path
from threading import Thread
from djangoApiDec.djangoApiDec import timing, removeInputFile
from ngram import NGram

this_dir, this_filename = os.path.split(__file__)
BASE_DIR = os.path.abspath(this_dir)

class KCM(object):
    """docstring for KCM"""

    '''args
    lang                help='language, english or chinese (eng/cht)', required=True)
    io_dir             help='input output directory, required=True)
    max_file_count      help='maximum number of input files, 0 for no limit, type=int, default=0)
    thread_count        help='number of thread used, type=int, default=1)
    '''

    def __init__(self, lang, io_dir, max_file_count=0, thread_count=1,  uri=None):
        self.BASE_DIR = BASE_DIR
        self.lang = lang
        self.io_dir = os.path.join(io_dir, self.lang)
        self.max_file_count = max_file_count
        self.thread_count = thread_count

        self.client = MongoClient(uri)
        self.db = self.client['nlp']
        self.Collect = self.db['kcm']  

        # ngram search
        self.modelNgram = NGram((i['key'] for i in self.Collect.find({}, {'key':1, '_id':False})))
        logging.basicConfig(format='%(levelname)s : %(asctime)s : %(message)s', filename='KCM_{}.log'.format(self.lang), level=logging.INFO)
        logging.info('Begin gen_kcm.py')
        logging.info('input {self.max_file_count} files, '
                     'output to {self.io_dir}, '
                     'maximum file count {self.max_file_count}, '
                     'use {self.thread_count} threads'.format(**locals()))

    def get_source_file_list(self):
        """Generate list of term data source files

        Args:
            args: input arguments, use self.lang, self.max_file_count

        Returns:
            list of source files
        """

        file_list = []  # wiki files
        for (dir_path, dir_names, file_names) in os.walk(self.io_dir):
            for file_name in file_names:
                if self.max_file_count and len(file_list) >= self.max_file_count:
                    break
                if file_name == '.DS_Store' or '.model' in file_name:  # for OS X
                    continue
                file_list.append(os.path.join(dir_path, file_name))
                logging.info(
                    'appended file {}'.format(os.path.join(dir_path, file_name)))

        if not file_list:
            logging.info('no file selected, end of script')
            exit()

        return file_list

    @timing
    def remove_symbols_tags(self, if_name):
        """Remove symbols and tags. Read input file, output to output file.

        Args:
            if_name: input file name
            args: input arguments, use self.io_dir, self.lang

        Returns:
            output file name
        """
        return rm_tags(if_name)

    @timing
    def paragraphs_to_sentences(self, inputData):
        """Generate sentences from paragraphs. Read input file, output to output file

        Args:
            inputData: input data from former process.
            args: input arguments, use self.io_dir, self.lang

        Returns:
            output file name
        """
        return paragraphs_to_sentences_cht(inputData)

    @timing
    def sentences_to_terms(self, if_name, inputData):
        """generate terms from sentences

        Args:
            if_name: input file name
            args: input arguments, use self.io_dir, self.lang

        Returns:
            output file name
        """
        prefix = if_name.split('/')[-1].split('_')[0]
        of_name = '{self.io_dir}/{prefix}_terms_{self.lang}'.format(**locals())
        PosTokenizer(self.BASE_DIR, inputData, of_name, 'w', save=['n', 'l', 'eng', 'i', 'j', 's', 'vn'])

        return of_name

    @removeInputFile
    @timing
    def terms_to_term_pairs(self, if_name):
        """Generate term pairs from terms.

        Args:
            if_name: input file name
            args: input arguments, use self.io_dir, self.lang

        Returns:
            output file name
        """
        of_name = '{self.io_dir}/{self.lang}.model'.format(**locals())
        script_file = 'build/terms_to_term_pair_freq.py'

        terms_to_term_pair_freq(if_name, of_name, min_freq=1, max_term_len=20)


    @timing
    def join_terms_files(self, if_names):
        """Join terms files into one

        Args:
            if_names: input terms files names
            args: input arguments
        """
        of_name = '{self.io_dir}/terms_{self.lang}'.format(**locals())
        with open(of_name, 'w') as output_file:
            for if_name in if_names:
                with open(if_name, 'r') as input_file:
                    for line in input_file:
                        output_file.write(line)

        return of_name


    def gen_terms_file(self, if_name, o_list):
        """Generate terms file

        Args:
            if_name: input wiki source file name
            args: input arguments
            o_list: output list saving generated file name
        """
        result = self.remove_symbols_tags(if_name)
        result = self.paragraphs_to_sentences(result)
        of_name = self.sentences_to_terms(if_name, result)
        o_list.append(of_name)


    def thread_job(self, input_file_queue, o_term_files):
        """Job to be done by thread (generate terms file)

        Args:
            input_file_queue: queue containing input files that needs processing
            args: input arguments
            o_term_files: list for outputting generated term file names
        """
        while True:
            if_name = input_file_queue.get()
            if if_name is None:
                break  # end of thread
            self.gen_terms_file(if_name, o_list=o_term_files)
            input_file_queue.task_done()

    @timing
    def main(self):
        """main function"""
        if_list = self.get_source_file_list()

        term_files = []
        input_file_queue = queue.Queue()
        threads = []
        for i in range(self.thread_count):
            t = Thread(target=self.thread_job, args=(input_file_queue, term_files))
            t.start()
            threads.append(t)

        for if_name in if_list:
            input_file_queue.put(if_name)

        # block till all tasks are done (here means all input file processed)
        input_file_queue.join()

        # stop all threads
        for i in range(self.thread_count):
            input_file_queue.put(None)
            # in thread_job, when input_file_queue.get == None, thread will end
        for t in threads:
            t.join()  # wait till all threads really end

        of_name = self.join_terms_files(term_files)
        self.terms_to_term_pairs(of_name) 
        self.import2DB()

    def setLang(self, lang):
        self.lang = lang
        self.io_dir = os.path.join(io_dir, self.lang)

    def removeDB(self):
        self.Collect.remove({})

    def import2DB(self):
        import pyprind
        
        result = dict()
        with open(os.path.join(self.io_dir, "{0}.model".format(self.lang)) , 'r', encoding='utf8') as f:
            for i in f:
                tmp = i.split()
                result.setdefault(tmp[0], []).append([tmp[1], int(tmp[2])])
                result.setdefault(tmp[1], []).append([tmp[0], int(tmp[2])])

        documentArr = tuple(map( lambda pair:{'key':pair[0], 'value':sorted(pair[1], key=lambda x:-x[1])}, pyprind.prog_percent(result.items())))
        del result

        self.Collect.insert(documentArr)
        self.Collect.create_index([("key", pymongo.HASHED)])

    def get(self, keyword, amount):
        result = self.Collect.find({'key':keyword}, {'value':1, '_id':False}).limit(1)
        if result.count()==0:
            keyword = self.modelNgram.find(keyword)
            result = self.Collect.find({'key':keyword}, {'value':1, '_id':False}).limit(1)
        return result[0]['value'][:amount]

def main():
    import argparse
    """The main routine."""
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='''
        build kcm model and insert it into mongoDB with command line.    
    ''')
    parser.add_argument('-p', metavar='abosolute path', help='give absolute path of wiki input file', required=True)
    args = parser.parse_args()
    k = KCM('cht', args.p)
    k.removeDB()
    k.main()

    print(k.get('臺灣', 10))
    print(k.get('pizza', 10))

if __name__ == "__main__":
    main()