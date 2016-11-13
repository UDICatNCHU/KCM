path2Folder=$1
output=$2

for AA in $path2Folder/*
do
    AA_dir=$(echo $AA |  sed -r 's#'"$path2Folder"'\/##g')
    mkdir -p $output/$AA_dir
    for wikiNum in $AA/*
    do
        wikiNum=$(echo $wikiNum |  sed -r 's#'"$AA"'\/##g')
        # echo $wikiNum
        #echo $output/$AA_dir/$wikiNumir
        # echo $wikiNum
        # echo $AA
        python detectPN.py $AA/$wikiNum jieba_expandDict_s.txt
        opencc -i $AA/$wikiNum -o $output/$AA_dir/$wikiNum\_cc
        python detectPN.py $output/$AA_dir/$wikiNum\_cc jieba_expandDict.txt
    done
done     