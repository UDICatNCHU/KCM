#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from pymongo import MongoClient
class import2Mongo(object):
	"""docstring for import2Mongo"""
	def __init__(self, lang, uri=None):
		self.file = open("../WikiRaw/{0}/{0}.model".format(lang), 'r', encoding='utf8')
		self.client = MongoClient(uri)
		self.db = self.client['nlp']
		self.Collect = self.db['kcm']
		

	def Build(self):
		for i in self.file:
			tmp = i.split()
			self.Collect.update({"key":tmp[0]}, {"$push":{"value":tmp[1:]}}, True)
			self.Collect.update({"key":tmp[1]}, {"$push":{"value":tmp[0::2]}}, True)

	def get(self, keyword, amount):
		result = self.Collect.find({"key":keyword}, {"value":1}).limit(1)
		if result.count() == 0:
			return []
		return sorted(list(result)[0]['value'], key=lambda x:-int(x[1]))[:amount]

i = import2Mongo("cht")
i.Build()
result = i.get('臺灣', 10)
print(result)