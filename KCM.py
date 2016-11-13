import os, json
from pathlib import Path

class KCM(object):
	""" A KCM object having api for web to query
	Args:
		filePath: path to ptt json file.

	Returns:
		ptt articles with specific keyword.
	"""
	def __init__(self):
		self.dirPath = 'json'

	def getTermFilePath(self, keyword):
		return '{}/{}/{}.json'.format(self.dirPath, keyword, keyword)

	def getTermFolderPath(self, keyword):
		return '{}/{}'.format(self.dirPath, keyword)

	def saveFile(self, keyword, data):
		with open(self.getTermFilePath(keyword), 'w', encoding='utf8') as f:
			json.dump(data, f)

	def loadFile(self, filePath):
		with open(filePath, 'r', encoding='utf8') as f:
			return json.load(f)

	def hasFile(self, keyword):
		file = Path(self.getTermFilePath(keyword))
		if file.is_file():
			return True
		else: return False
	def start(self, keyword, func, *arg):
		if self.hasFile(keyword):
			pass
		elif os.path.exists(self.getTermFolderPath(keyword)):
			data = func(*arg)
			self.saveFile(keyword, data)
		else:
			data = func(*arg)
			os.makedirs(self.getTermFolderPath(keyword))
			self.saveFile(keyword, data)