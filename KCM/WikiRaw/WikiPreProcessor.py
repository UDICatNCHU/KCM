# -*- coding: utf-8 -*-
import os, argparse, subprocess, re
def get_args():
	"""Return args"""

	parser = argparse.ArgumentParser(
		description='Generate KCM (correlation model).')
	parser.add_argument('-wiki', '--wikiFile',
						help='input raw wiki data file name (default: %(default)s)',
						required=True)
	parser.add_argument('-b', '--BASE_DIR',
						help='BASE_DIR path (default: %(default)s)',
						required=True)
	parser.add_argument('-o', '--output_dir',
						help='ouput data directory path (default: %(default)s)',
						required=True)
	parser.add_argument('-l', '--lang', choices=['eng', 'cht'],
						help='language you can choose (eng/cht)(default: %(default)s)',
						required=True)
	args = parser.parse_args()
	return args

class PreProcess(object):
	"""docstring for ClassName"""

	def __init__(self, arg):
		def getFolderPre():
			folderPre = re.search(r'wiki(.)+',self.wikiFile.split('.')[0])
			return str(folderPre.group(0))
		self.BASE_DIR = arg.BASE_DIR
		self.output_dir = arg.output_dir
		self.wikiFile = arg.wikiFile
		self.lang = arg.lang
		self.folderPre = getFolderPre()
		subprocess.call(['python2', self.BASE_DIR + '/WikiRaw/preprocess_lib/WikiExtractor.py', self.wikiFile, '-o', self.output_dir])


	def rename_extrac_files_and_expand_jiebaDict(self):
		"""Rename extracted wiki dir, etc AA, AB. And also get proper Noun from those Wiki text into dictionary to do Word Segmentation.

		Returns:
			None.
		"""

		file_list = []  # wiki files
		for (dir_path, dir_names, file_names) in os.walk(self.output_dir):
			if dir_names == []:
				langDir = dir_path.split('/')[0]

			for dirName in dir_names:
				# wikiextract出來之後，結果會是AA、AB等等的資料夾名稱
				# 因為AA、AB名子會重複，所以把wiki包的字尾接在AA後面以便識別
				if len(dirName) == 2:
					subprocess.call(['mv', dir_path+'/'+dirName, dir_path+'/'+dirName + self.folderPre])

		if not file_list:
			exit()

		return file_list

	# def language(self, dir_path, file_name, langDir):
	# 	if self.lang == 'cht':
	# 		subprocess.call(['python2', self.BASE_DIR + '/WikiRaw/preprocess_lib/detectPN.py', dir_path + '/' + file_name, langDir + '/' + 'jieba_expandDict_s.txt'])
	# 		subprocess.call(['opencc', '-i', dir_path + '/' + file_name, '-o', dir_path + '/' + file_name + '_tradCHT'])
	# 		subprocess.call(['python2', self.BASE_DIR + '/WikiRaw/preprocess_lib/detectPN.py', dir_path + '/' + file_name, langDir + '/' + 'jieba_expandDict_trad.txt'])
	# 		# detectPN 這個script會先把wiki_00這類的文章專有名詞先挑出來，加入到結巴的字典裏面，然後再把wiki轉成繁體字然後再挑專有名詞出來，所以會做出繁簡兩種字典擴充包
	# 	elif self.lang == 'eng':
	# 		subprocess.call(['python2', self.BASE_DIR + '/WikiRaw/preprocess_lib/detectPN.py', dir_path + '/' + file_name, langDir + '/' + 'jieba_expandDict_eng.txt'])


def main():
    """Main function"""
    args = get_args()
    p = PreProcess(args)
    p.rename_extrac_files_and_expand_jiebaDict()

if __name__ == '__main__':
    main()
