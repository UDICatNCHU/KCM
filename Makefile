.PHONY: install init query test build
install:
	sudo apt-get install -y opencc
	pip install -r requirements.txt
test:
	python run_tests.py
build:
	python gen_kcm.py -l=cht -i ChineseWikiRawData/ -o ChineseWikiRawData/ -m=0 -tc=4
query:
	python query/get_top_n_cor_terms_from_text.py -i=ChineseWikiRawData/term_pair_freq_cht -t=$(kw)
init:
	mkdir zhwiki_raw

	# 下載原始的wiki raw data
	cd zhwiki_raw; wget https://dumps.wikimedia.org/zhwiki/20160501/zhwiki-20160501-pages-articles1.xml.bz2

	# # Extract 維基的XML
	cd zhwiki_raw; python ../WikiExtractor.py zhwiki-20160501-pages-articles1.xml.bz2 -o extract_zhwiki1

    # expandJiebaDict這個script會先把wiki_00這類的文章專有名詞先挑出來，加入到結巴的字典裏面，然後再把wiki轉成繁體字然後再挑專有名詞出來，所以會做出繁簡兩種字典擴充包
	bash expandJiebaDict.sh zhwiki_raw/extract_zhwiki1 zhOutput1

	# wiki2
	cd zhwiki_raw; wget https://dumps.wikimedia.org/zhwiki/20160501/zhwiki-20160501-pages-articles2.xml.bz2
	cd zhwiki_raw; python ../WikiExtractor.py zhwiki-20160501-pages-articles2.xml.bz2 -o extract_zhwiki2
	bash expandJiebaDict.sh zhwiki_raw/extract_zhwiki2 zhOutput2

	# wiki3
	cd zhwiki_raw; wget https://dumps.wikimedia.org/zhwiki/20160501/zhwiki-20160501-pages-articles3.xml.bz2
	cd zhwiki_raw; python ../WikiExtractor.py zhwiki-20160501-pages-articles3.xml.bz2 -o extract_zhwiki3
	bash expandJiebaDict.sh zhwiki_raw/extract_zhwiki3 zhOutput3

	# wiki4
	cd zhwiki_raw; wget https://dumps.wikimedia.org/zhwiki/20160501/zhwiki-20160501-pages-articles4.xml.bz2
	cd zhwiki_raw; python ../WikiExtractor.py zhwiki-20160501-pages-articles4.xml.bz2 -o extract_zhwiki4
	bash expandJiebaDict.sh zhwiki_raw/extract_zhwiki4 zhOutput4

	# append extended jieba dictionary to original dict
	cat jieba_expandDict.txt >> dict.txt