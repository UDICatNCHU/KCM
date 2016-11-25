# Keyword Correlation Model (KCM 關鍵字相關性模型)[![Build Status](https://travis-ci.com/UDICatNCHU/KCM.svg?token=XRWFynWvo8Gsjgh9wqTN&branch=master)](https://travis-ci.com/UDICatNCHU/KCM)

This repository contains python scripts to generate KCM/TCM (Keyword/Term Correlating Model) from text file generated by [WikiExtractor](https://github.com/attardi/wikiextractor), which extracts plain text from wiki dumps.  

The python scripts tries to follow the coding convention from [google python style guide](https://google.github.io/styleguide/pyguide.html).


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisities

1. OS：Ubuntu / OSX would be nice
2. environment：need python3 `sudo apt-get update; sudo apt-get install; python3 python3-dev`

### Installing

```
1. git clone https://david30907d@bitbucket.org/udiclab/term_classification.git
2. 使用虛擬環境：
  1. `virtualenv venv`
  2. `. venv/bin/activate`
3. sudo make install
```


## Running & Testing

## Run

* 整體使用方法：
  * 建立KCM模型： `make init lang=cht` ( This command must be executed in the directory which has `Makefile` )，lang是語言的參數，後面的cht可以換成其他語言的代號（目前上無其他語言可選）。

  * 查詢KCM模型：`make query lang={語言} kw={關鍵字}`
* 個別執行方法：
  * Generate Chinese KCM from all wiki files with 4 threads：`python3 build/gen_kcm.py -l=cht -i [path] -o [path] -m=0 -tc=4`

  * Generate sqlite db file from term_pair-freq text file：`python3 build/term_pair_freq_to_db.py -i=TERM_PAIR_FREQ_FILE -o=DB_FILE`

  * Get top n correlated terms from kcm database：`python3 build/get_top_n_cor_terms_from_db.py -i=KCM_DB -t=BASE_TERM -N=HOW_MANY_COR_TERMS`


  * Get top 10 correlated terms from kcm text：`python3 build/get_top_n_cor_terms_from_text.py -i=KCM_TEXT -t=BASE_TERM`

  * Get top 10 correlated term pairs from text：`python3 build/get_top_n_cor_terms_from_text.py -i=KCM_MODEL`




### Break down into end to end tests


1. 執行全部的測試：`python3 run_tests.py`

### And coding style tests

目前沒有coding style tests...

### Results

執行美國隊長的查詢：`make query lang=cht kw=美國隊長`
```
('復仇者', 113)
('和', 105)
('他', 66)
('中', 60)
('電影', 59)
('後', 56)
('漫畫', 54)
('他們', 49)
('英雄', 48)
('人', 46)

```

## Deployment

目前只是一般的python程式，git clone佈署即可

## Built With

* python3.2
* python3.3
* python3.4
* python3.5

## Versioning

For the versions available, see the [tags on this repository](https://github.com/david30907d/KCM/releases).

## Contributors

* **范耀中** [教授](http://web.nchu.edu.tw/~yfan/)
* **黃思穎**
* **陳聖軒**
* **Yen-Ju Lee**
* **張泰瑋** [david](https://github.com/david30907d)

## License

目前還不清楚能不能open source，所以暫不添加License

## Acknowledgments

* 感謝fxsjy的jieba斷詞系統
* 感謝Google工程師釋出的word2vec
