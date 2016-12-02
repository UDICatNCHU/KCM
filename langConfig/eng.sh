mkdir -p WikiRaw/eng;
# 下載原始的wiki raw data
cd WikiRaw/bz2; wget https://dumps.wikimedia.org/enwiki/20161120/enwiki-20161120-pages-articles1.xml-p000000010p000030302.bz2;

# Extract 維基的XML
cd ../;python2 WikiPreProcessor.py -wiki bz2/enwiki-20161120-pages-articles1.xml-p000000010p000030302.bz2 -o eng

# mv extended jieba dictionary to dictionary directory
# mv WikiRaw/cht/jieba_expandDict_trad.txt dictionary/