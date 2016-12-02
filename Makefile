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
	mkdir -p WikiRaw/bz2;
	bash langConfig/$(lang).sh	

# initialize the whole process, it will get wikidata and build model.
init: start getWiki build end
start:
	echo $@: `date +%s` > time.log
end:
	echo $@: `date +%s` >> time.log
	python3 build/duration.py
