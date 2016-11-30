.PHONY: install init query test build getWiki
install:
	sudo apt-get install -y opencc
	pip3 install -r requirements.txt
test:
	python3 run_tests.py
build:
	python3 gen_kcm.py -l=$(lang) -i WikiRaw/$(lang) -o WikiRaw/$(lang) -m=0 -tc=4
query:
	python3 query/get_top_n_cor_terms_from_text.py -i=WikiRaw/$(lang)/$(lang).model -t=$(kw)

getWiki:
	mkdir -p WikiRaw/cht;
	mkdir -p WikiRaw/bz2;
	# 下載原始的wiki raw data
	cd WikiRaw/bz2; wget https://dumps.wikimedia.org/zhwiki/20161120/zhwiki-20161120-pages-articles1.xml.bz2;wget https://dumps.wikimedia.org/zhwiki/20161120/zhwiki-20161120-pages-articles2.xml.bz2;wget https://dumps.wikimedia.org/zhwiki/20161120/zhwiki-20161120-pages-articles3.xml.bz2;wget https://dumps.wikimedia.org/zhwiki/20161120/zhwiki-20161120-pages-articles4.xml.bz2;

	# # Extract 維基的XML
	cd WikiRaw;python2 WikiPreProcessor.py -i cht -wiki bz2/zhwiki-20161120-pages-articles1.xml.bz2 -o cht ;python2 WikiPreProcessor.py -i cht -wiki bz2/zhwiki-20161120-pages-articles2.xml.bz2 -o cht ;python2 WikiPreProcessor.py -i cht -wiki bz2/zhwiki-20161120-pages-articles3.xml.bz2 -o cht ;python2 WikiPreProcessor.py -i cht -wiki bz2/zhwiki-20161120-pages-articles4.xml.bz2 -o cht

	# mv extended jieba dictionary to dictionary directory
	mv WikiRaw/cht/jieba_expandDict_trad.txt dictionary/

# initialize the whole process, it will get wikidata and build model.
init: start getWiki build end
start:
	echo $@: `date +%s` > time.log
end:
	echo $@: `date +%s` >> time.log
	python3 build/duration.py
