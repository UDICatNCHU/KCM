mkdir -p WikiRaw/cht;
# 下載原始的wiki raw data
cd WikiRaw/bz2; wget https://dumps.wikimedia.org/zhwiki/20161120/zhwiki-20161120-pages-articles1.xml.bz2;wget https://dumps.wikimedia.org/zhwiki/20161120/zhwiki-20161120-pages-articles2.xml.bz2;wget https://dumps.wikimedia.org/zhwiki/20161120/zhwiki-20161120-pages-articles3.xml.bz2;wget https://dumps.wikimedia.org/zhwiki/20161120/zhwiki-20161120-pages-articles4.xml.bz2;

# Extract 維基的XML
cd ../;python2 WikiPreProcessor.py -wiki bz2/zhwiki-20161120-pages-articles1.xml.bz2 -o cht -l=cht ;python2 WikiPreProcessor.py -wiki bz2/zhwiki-20161120-pages-articles2.xml.bz2 -o cht -l=cht ;python2 WikiPreProcessor.py -wiki bz2/zhwiki-20161120-pages-articles3.xml.bz2 -o cht -l=cht ;python2 WikiPreProcessor.py -wiki bz2/zhwiki-20161120-pages-articles4.xml.bz2 -o cht -l=cht

# mv extended jieba dictionary to dictionary directory
mv WikiRaw/cht/jieba_expandDict_trad.txt dictionary/