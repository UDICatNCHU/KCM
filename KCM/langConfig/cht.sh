mkdir -p WikiRaw/cht;
mkdir -p WikiRaw/bz2;
# 下載原始的wiki raw data
wget http://stackoverflow.com/questions/1078524/how-to-specify-the-location-with-wget -P ${1}/WikiRaw/bz2
# ;wget https://dumps.wikimedia.org/zhwiki/20161120/zhwiki-20161120-pages-articles2.xml.bz2;wget https://dumps.wikimedia.org/zhwiki/20161120/zhwiki-20161120-pages-articles3.xml.bz2;wget https://dumps.wikimedia.org/zhwiki/20161120/zhwiki-20161120-pages-articles4.xml.bz2;
# Extract 維基的XML
python2 ${2}/WikiRaw/WikiPreProcessor.py -wiki ${1}/WikiRaw/bz2/zhwiki-20161120-pages-articles1.xml.bz2 -b ${2} -o ${1}/WikiRaw/cht -l=cht 
# ;python2 WikiPreProcessor.py -wiki bz2/zhwiki-20161120-pages-articles2.xml.bz2 -o cht -l=cht ;python2 WikiPreProcessor.py -wiki bz2/zhwiki-20161120-pages-articles3.xml.bz2 -o cht -l=cht ;python2 WikiPreProcessor.py -wiki bz2/zhwiki-20161120-pages-articles4.xml.bz2 -o cht -l=cht

# mv extended jieba dictionary to dictionary directory
#mv WikiRaw/cht/jieba_expandDict_trad.txt dictionary/