#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from pymongo import MongoClient
class import2Mongo(object):
	"""docstring for import2Mongo"""
	def __init__(self, lang, uri=None):
		self.lang = lang
		self.client = MongoClient(uri)
		self.db = self.client['nlp']
		self.Collect = self.db['kcm']
		

	def Build(self):
		import pyprind

		self.Collect.remove({})
		result = dict()

		with open("../WikiRaw/{0}/{0}.model".format(self.lang), 'r', encoding='utf8') as f:
			for i in f:
				tmp = i.split()
				result.setdefault(tmp[0], []).append(tmp[1:])
				result.setdefault(tmp[1], []).append(tmp[0::2])

		documentArr = tuple( dict(key=index, value=value) for index, value in pyprind.prog_percent(result.items()))
		del result

		self.Collect.insert(documentArr)

	def get(self, keyword, amount):
		result = self.Collect.find({'key':keyword}, {'value':1, '_id':False}).limit(1)
		if result.count() == 0:
			return []
		return sorted(dict(list(result)[0])['value'], key=lambda x:-int(x[1]))[:amount]

if __name__ == "__main__":
	i = import2Mongo("cht")
	i.Build()
	result = i.get('臺灣', 10)
	print(result)	