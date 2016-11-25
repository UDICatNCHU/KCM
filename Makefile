.PHONY: install init query test build getWiki
install:
	sudo apt-get install -y opencc
	pip install -r requirements.txt
test:
	python run_tests.py
build:
	python gen_kcm.py -l=$(lang) -i WikiRaw/$(lang) -o WikiRaw/$(lang) -m=0 -tc=4
query:
	python query/get_top_n_cor_terms_from_text.py -i=WikiRaw/$(lang)/$(lang).model -t=$(kw)

getWiki:
	mkdir -p WikiRaw/cht;
	mkdir -p WikiRaw/bz2;
	# 下載原始的wiki raw data
	cd WikiRaw/bz2; wget https://dumps.wikimedia.org/zhwiki/20160501/zhwiki-20160501-pages-articles1.xml.bz2;wget https://dumps.wikimedia.org/zhwiki/20160501/zhwiki-20160501-pages-articles2.xml.bz2;wget https://dumps.wikimedia.org/zhwiki/20160501/zhwiki-20160501-pages-articles3.xml.bz2;wget https://dumps.wikimedia.org/zhwiki/20160501/zhwiki-20160501-pages-articles4.xml.bz2;

	# # Extract 維基的XML
	cd WikiRaw;python2 WikiPreProcessor.py -i cht -wiki bz2/zhwiki-20160501-pages-articles1.xml.bz2 -o cht ;python2 WikiPreProcessor.py -i cht -wiki bz2/zhwiki-20160501-pages-articles2.xml.bz2 -o cht ;python2 WikiPreProcessor.py -i cht -wiki bz2/zhwiki-20160501-pages-articles3.xml.bz2 -o cht ;python2 WikiPreProcessor.py -i cht -wiki bz2/zhwiki-20160501-pages-articles4.xml.bz2 -o cht

	# append extended jieba dictionary to original dict
	# cat jieba_expandDict.txt >> dict.txt

# initialize the whole process, it will get wikidata and build model.
init: start getWiki build end
start:
	echo $@: `date +%s` > time.log
end:
	echo $@: `date +%s` >> time.log
	python build/duration.py
