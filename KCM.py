import os, json, queue, subprocess
from collections import OrderedDict
from pathlib import Path
from functools import wraps

class KCM(object):
	""" A KCM object having api for web to query
	Args:
		filePath: path to ptt json file.

	Returns:
		ptt articles with specific keyword.
	"""
	def __init__(self, missionType = 'model', ParentDir = ''):
		self.ParentDir = ParentDir
		self.DirPath = ''
		self.WikiModelDirPath = 'WikiRaw'
		self.JsonDirPath = 'json'
		self.missionType = missionType
		self.fname_extension = ''

	def setMissionType(self, missionType):
		self.missionType = missionType

	def setDirPath(func):
		@wraps(func)
		def wrap(self, *args, **kw):
			self.DirPath = self.ParentDir + (self.WikiModelDirPath if self.missionType == 'model' else self.JsonDirPath)
			self.fname_extension = 'model' if self.missionType == 'model' else 'json'
			return func(self, *args, **kw)
		return wrap

	def get_cor_term_freq_pq(self, if_name, base_term, min_freq=1):
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


	def return_top_n_cor_terms(self, pq, n=10):
		"""Generate top n correlated terms from priority queue

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
			jsonResult[cor_term] = freq
		return jsonResult

	@setDirPath
	def getFilePath(self, keyword):
		return '{}/{}/{}.{}'.format(self.DirPath, keyword, keyword, self.fname_extension)

	@setDirPath
	def getFolderPath(self, keyword):
		return '{}/{}'.format(self.DirPath, keyword)

	def saveFile(self, keyword, data):
		if self.missionType == 'model':
			pass
		else:
			with open(self.getFilePath(keyword), 'w', encoding='utf8') as f:
				json.dump(data, f)

	def loadFile(self, keyword):
		if self.missionType == 'model':
			return getFilePath(keyword)
		else:
			with open(self.getFilePath(keyword), 'r', encoding='utf8') as f:
				return json.load(f, object_pairs_hook=OrderedDict)

	def hasFile(self, keyword):
		file = Path(self.getFilePath(keyword))
		if file.is_file():
			return True
		else: return False

	def DirectCall(self):
		if self.ParentDir == '':
			return True
		else:
			return False

	def getOrCreate(self, keyword, func, *arg):
		if self.hasFile(keyword):
			data = self.loadFile(keyword)
		elif os.path.exists(self.getFolderPath(keyword)):
			data = func(*arg)
			self.saveFile(keyword, data)
		else:
			data = func(*arg)
			os.makedirs(self.getFolderPath(keyword))
			self.saveFile(keyword, data)

		if self.DirectCall():
			for i in data.items():
				print(i)
		return data