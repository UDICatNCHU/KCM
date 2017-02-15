mkdir -p WikiRaw/eng;
# 下載原始的wiki raw data
cd WikiRaw/bz2; wget https://dumps.wikimedia.org/enwiki/20161201/enwiki-20161201-pages-articles.xml.bz2;

# Extract 維基的XML
cd ../;python2 WikiPreProcessor.py -wiki bz2/enwiki-20161201-pages-articles.xml.bz2 -o eng -l=eng

# mv extended jieba dictionary to dictionary directory
# mv WikiRaw/eng/jieba_expandDict_eng.txt dictionary/
