#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KCM generating script

This script is used to generate KCM/TCM (Term correlated model).
The task is done by calling many other scripts
"""
import json, pymongo
from pymongo import MongoClient
import os, queue, subprocess, time, logging, errno, argparse
from pathlib import Path
from threading import Thread
from djangoApiDec.djangoApiDec import timing, removeInputFile

class KCM(object):
    """docstring for KCM"""

    '''args
    lang                help='language, english or chinese (eng/cht)', required=True)
    io_dir             help='input output directory, required=True)
    max_file_count      help='maximum number of input files, 0 for no limit, type=int, default=1)
    thread_count        help='number of thread used, type=int, default=1)
    '''

    def __init__(self, max_file_count=1, thread_count=1,  uri=None):
        self.lang = ''
        self.io_dir = ''
        self.max_file_count = max_file_count
        self.thread_count = thread_count

        self.client = MongoClient(uri)
        self.db = self.client['nlp']
        self.Collect = self.db['kcm']  
        self.Collect.remove({})

        logging.basicConfig(format='%(levelname)s : %(asctime)s : %(message)s', filename='KCM_{}.log'.format(self.lang), level=logging.INFO)
        logging.info('Begin gen_kcm.py')
        logging.info('input {self.max_file_count} files, '
                     'output to {self.io_dir}, '
                     'maximum file count {self.max_file_count}, '
                     'use {self.thread_count} threads'.format(**locals()))

    def remove_file_if_exist(self, file_name):
        """Remove file if it exist

        Args:
            file_name: name of the file to be removed
        """
        file = Path(file_name)
        if file.is_file():
            os.remove(file_name)


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
                if file_name == '.DS_Store':  # for OS X
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
        prefix = if_name.replace('/', '-').replace('_', '-')
        of_name = '{self.io_dir}/{prefix}_paragraph_{self.lang}'.format(**locals())
        self.remove_file_if_exist(of_name)

        subprocess.call(['python3', 'build/rm_symbols_tags_empty_lines.py',
                         '-i={}'.format(if_name), '-o={}'.format(of_name)])
        return of_name

    @removeInputFile
    @timing
    def paragraphs_to_sentences(self, if_name):
        """Generate sentences from paragraphs. Read input file, output to output file

        Args:
            if_name: input file name
            args: input arguments, use self.io_dir, self.lang

        Returns:
            output file name
        """
        prefix = if_name.split('/')[-1].split('_')[0]
        of_name = '{self.io_dir}/{prefix}_sentences_{self.lang}'.format(**locals())
        self.remove_file_if_exist(of_name)
        script_file = 'build/paragraphs_to_sentences_{}.py'.format(self.lang)

        subprocess.call(['python3', script_file,
                         '-i', if_name, '-o', of_name])

        return of_name

    @removeInputFile
    @timing
    def sentences_to_terms(self, if_name):
        """generate terms from sentences

        Args:
            if_name: input file name
            args: input arguments, use self.io_dir, self.lang

        Returns:
            output file name
        """
        prefix = if_name.split('/')[-1].split('_')[0]
        of_name = '{self.io_dir}/{prefix}_terms_{self.lang}'.format(**locals())
        self.remove_file_if_exist(of_name)
        script_file = 'build/sentences_to_terms_{}.py'.format(self.lang)

        subprocess.call(['python3', script_file,
                         if_name, '-o', of_name, '-m', 'w', '-s', 'n'])

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
        self.remove_file_if_exist(of_name)
        script_file = 'build/terms_to_term_pair_freq.py'

        subprocess.call(['python3', script_file, '-i', if_name, '-o', of_name])


    # http://stackoverflow.com/questions/13613336/python-concatenate-text-files
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
        of_name = self.remove_symbols_tags(if_name)
        of_name = self.paragraphs_to_sentences(of_name)
        of_name = self.sentences_to_terms(of_name)
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


    def main(self, lang, io_dir):
        """Main function"""
        self.lang = lang
        self.io_dir = io_dir + self.lang

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

    def import2DB(self):
        import pyprind
        
        result = dict()
        with open("WikiRaw/{0}/{0}.model".format(self.lang), 'r', encoding='utf8') as f:
            for i in f:
                tmp = i.split()
                result.setdefault(tmp[0], []).append([tmp[1], int(tmp[2])])
                result.setdefault(tmp[1], []).append([tmp[0], int(tmp[2])])

        documentArr = tuple(map( lambda pair:{'key':pair[0], 'value':pair[1]}, pyprind.prog_percent(result.items())))
        del result

        self.Collect.insert(documentArr)
        self.Collect.create_index([("key", pymongo.HASHED)])

    def get(self, keyword, amount):
        result = self.Collect.find({'key':keyword}, {'value':1, '_id':False}).limit(1)
        if result.count()==0:
            return []
        return sorted(dict(list(result)[0])['value'], key=lambda x:-int(x[1]))[:amount]


if __name__ == '__main__':
    k = KCM(0, 4, None)
    k.main('cht', 'WikiRaw/')

    print(k.get('臺灣', 10))
    print(k.get('pizza', 10))