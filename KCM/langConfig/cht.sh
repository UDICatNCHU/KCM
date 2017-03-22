mkdir -p WikiRaw/cht

mkdir -p WikiRaw/bz2

# 下載原始的wiki raw data
wget https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles1.xml.bz2 -P ${1}/WikiRaw/bz2
wget https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles2.xml.bz2 -P ${1}/WikiRaw/bz2
wget https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles3.xml.bz2 -P ${1}/WikiRaw/bz2
wget https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles4.xml.bz2 -P ${1}/WikiRaw/bz2

# Extract 維基的XML
python2 ${2}/WikiRaw/WikiPreProcessor.py -wiki ${1}/WikiRaw/bz2/zhwiki-20161120-pages-articles1.xml.bz2 -b ${2} -o ${1}/WikiRaw/cht -l=cht 
python2 ${2}/WikiRaw/WikiPreProcessor.py -wiki ${1}/WikiRaw/bz2/zhwiki-20161120-pages-articles2.xml.bz2 -b ${2} -o ${1}/WikiRaw/cht -l=cht 
python2 ${2}/WikiRaw/WikiPreProcessor.py -wiki ${1}/WikiRaw/bz2/zhwiki-20161120-pages-articles3.xml.bz2 -b ${2} -o ${1}/WikiRaw/cht -l=cht 
python2 ${2}/WikiRaw/WikiPreProcessor.py -wiki ${1}/WikiRaw/bz2/zhwiki-20161120-pages-articles4.xml.bz2 -b ${2} -o ${1}/WikiRaw/cht -l=cht

# mv extended jieba dictionary to dictionary directory
#mv WikiRaw/cht/jieba_expandDict_trad.txt dictionary/
