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
		self.index = self.db['kcmIndex']
		

	def Build(self):
		import pyprind
		def buildIndex():
			self.index.remove({})
			indexArr = tuple({doc['key']:doc['_id']} for doc in self.Collect.find())
			self.index.insert(indexArr)

		self.Collect.remove({})
		result = dict()

		with open("../WikiRaw/{0}/{0}.model".format(self.lang), 'r', encoding='utf8') as f:
			for i in f:
				tmp = i.split()
				result.setdefault(tmp[0], []).append([tmp[1], int(tmp[2])])
				result.setdefault(tmp[1], []).append([tmp[0], int(tmp[2])])

		documentArr = tuple( dict(key=index, value=value) for index, value in pyprind.prog_percent(result.items()))
		del result

		self.Collect.insert(documentArr)
		buildIndex()

	def get(self, keyword, amount):
		objectID = self.index.find({keyword:{'$exists':True}}).limit(1)
		if objectID.count()==0:
			return []
		result = self.Collect.find({'_id':dict(list(objectID)[0])[keyword]}, {'value':1, '_id':False}).limit(1)
		return sorted(dict(list(result)[0])['value'], key=lambda x:-int(x[1]))[:amount]

	def delDuplicate(self):
		import pyprind
		bar = pyprind.ProgBar( self.Collect.find().count())
		keywordSet = set()
		for i in self.Collect.find():
			keywordSet.add(i['key'])
			bar.update()

		for key in pyprind.prog_percent(keywordSet):
			value = []
			for dupkey in self.Collect.find({"key":key}):
				value += dupkey['value']
				self.Collect.remove({'_id':dupkey['_id']})

			tmpDict = dict()
			for tup in value:
				tmpDict.setdefault(tup[0], 0)+int(tup[1])
			valueArr = [[dictKey, dictValue]for dictKey, dictValue in tmpDict.items()]

			self.Collect.insert({'key':key, 'value':valueArr})


if __name__ == "__main__":
	i = import2Mongo("cht")
	i.Build()
	result = i.get('臺灣', 10)
	print(result)	
	# i.delDuplicate()