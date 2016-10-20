.PHONY: install init
install:
	sudo apt-get install -y opencc
	pip install -r requirements.txt
test:
	python run_test.py
run:
	python gen_kcm.py -l=cht -m=0 -tc=4  -i=ChineseWikiRawData/ -o .
