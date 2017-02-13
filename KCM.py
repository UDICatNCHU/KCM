#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, pymongo
from pymongo import MongoClient
class KCM(object):
	"""docstring for KCM"""
	def __init__(self, lang, uri=None):
		self.lang = lang
		self.client = MongoClient(uri)
		self.db = self.client['nlp']
		self.Collect = self.db['kcm']		

	def Build(self):
		import pyprind
		self.Collect.remove({})
		for lan in self.lang:
			result = dict()
			with open("WikiRaw/{0}/{0}.model".format(lan), 'r', encoding='utf8') as f:
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

if __name__ == "__main__":
	import urllib
	p=urllib.parse.quote('udic@720')
	i = KCM(["cht", 'eng'], 'mongodb://udic:'+p+'@140.120.13.243:27017')
	i.Build()
	result = i.get('臺灣', 10)
	print(result)	
	result = i.get('pizza', 10)
	print(result)	