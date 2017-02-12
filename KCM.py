# -*- coding: utf-8 -*-
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
	def __init__(self, num, missionType = 'model', ParentDir = ''):
		self.ParentDir = ParentDir
		self.DirPath = ''
		self.WikiModelDirPath = 'WikiRaw'
		self.JsonDirPath = 'json'
		self.missionType = missionType
		self.fname_extension = ''
		self.queryNum = num

	def setMissionType(self, missionType):
		self.missionType = missionType

	def setDirPath(func):
		@wraps(func)
		def wrap(self, *args, **kw):
			self.DirPath = self.ParentDir + (self.WikiModelDirPath if self.missionType == 'model' else self.JsonDirPath)
			self.fname_extension = 'model' if self.missionType == 'model' else 'json'
			return func(self, *args, **kw)
		return wrap

	def hasFile(self, keyword):
		file = Path(self.getFilePath(keyword))
		if file.is_file():
			return True
		else: return False