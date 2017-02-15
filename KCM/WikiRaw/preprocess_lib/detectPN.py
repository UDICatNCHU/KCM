#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import re, sys
class ProperNoun(object):
	"""docstring for ProperNoun"""
	def __init__(self):
		self.SetOfPN = set() # 為了避免重複儲存關鍵字，使用set資料型態去儲存

	def detect(self, line):
		# detect這個method是用正規表示法去抓到有這些括號的字出來，然後回傳一個list型態
		pos = re.findall(r'《.*?》', line)
		if pos != []:
			self.replaceSymbol(pos)
			return pos
		else:
			pos = re.findall(r"\[\[.*?\]\]", line)
			if pos != []:
				self.replaceSymbol(pos)
				return pos
			else:
				pos = re.findall(r'title=\".*?\"', line)
				if pos != []:
					self.replaceSymbol(pos)
					return pos

	def replaceSymbol(self, anList):
		# 因為detect回傳回來的專有名辭彙帶有括號，所以要用replaceSymbol把他清掉
		for i in range(0, len(anList)):
			anList[i] = anList[i].replace('《', '')
			anList[i] = anList[i].replace('》', '')
		for i in range(0, len(anList)):
			anList[i] = anList[i].replace('[[', '')
			anList[i] = anList[i].replace(']]', '')
		for i in range(0, len(anList)):
			anList[i] = anList[i].replace('title=\"', '')
			anList[i] = anList[i].replace('\"', '')
		for i in range(0, len(anList)):
			anList[i] = anList[i].replace('Category:', '')

		return anList
	def splitLineSym(self, anList):
		# 舉例：[[File:Chan 2009 US Open 01.jpg|thumb|right|250px|網球選手[[詹詠然]]參與[[2009年美國網球公開賽]]。]]
		# 裏面有一大堆 | ，splitLineSym就是把他切開然後個別儲存
		if anList!=None:
			newList = []
			for i in anList:
				i = i.split('|')
				newList.extend(i)
			return newList

	def addToSet(self, anList):
		# update可以接受一個list型態的參數加入set
		if anList!=None:
			self.SetOfPN.update(anList)



if __name__ == '__main__':
	p = ProperNoun()
	if len(sys.argv) < 3:
		#sys.argv[0]是模組名稱喔!
		print("Usage:\n\tpython[2] "+sys.argv[0]+" <wiki_00 這類型的檔案> <輸出的客製化jieba字典>")
		sys.exit(1)#0為正常結束，其他數字exit會拋出一個例外，可以被捕獲
	filename = sys.argv[1] # wiki_00這類型的原始檔
	# 一行一行讀取然後抓出關鍵字
	with open(filename, 'r') as f:
		for line in f:
			tmp = p.detect(line)
			tmp2 = p.splitLineSym(tmp)
			p.addToSet(tmp2)

	# 寫入字典檔
	with open(sys.argv[2],'a') as f:
		for i in p.SetOfPN:
			if i != "":
				f.write(i+' nz\n') # nz表示是專有名詞