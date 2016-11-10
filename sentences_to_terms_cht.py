"""Input text file of sentences, output text file of terms (Chinese)

Output format: '/詞1/詞2/詞2\n...'
"""

import jieba
import jieba.posseg as pseg
import argparse
import os.path, sys


def PosTokenizer(input, output, mission, save=None, remove=None):
    # jieba.enable_parallel()
    # jieba.set_dictionary('dict.txt.big.txt')
    jieba.load_userdict('dictionary/dict.txt.big.txt')
    jieba.load_userdict("dictionary/NameDict_Ch_v2")
    f = open(input, 'r')
    f2 = open(output, 'a')
    if save != None and remove != None:
        print('can\'t set save and remove at once')
    elif mission == 't':
        for sentence in f:
            if sentence != '\n':
                words = pseg.cut(sentence)
                for word, flag in words:
                    if word != '\n':
                        if remove != None and str(flag)[0] not in remove and str(flag) not in remove:
                            f2.write("/" + word + " " + flag)
                        elif save != None and str(flag)[0] in save:
                            f2.write("/" + word + " " + flag)
                        else:
                            f2.write("/" + word + " " + flag)
                    else:
                        f2.write('\n')

    elif mission == 'w' and (save != None or remove != None):
        for sentence in f:
            if sentence != '\n':
                words = pseg.cut(sentence)
                for word, flag in words:
                    if word != '\n':
                        if remove != None and str(flag)[0] not in remove and str(flag) not in remove:
                            f2.write("/" + word)
                        elif save != None and str(flag)[0] in save:
                            f2.write("/" + word)
                    else:
                        f2.write('\n')


    elif mission == 'w' and save == None and remove == None:
        for sentence in f.readlines():
            if sentence != '\n':
                words = jieba.cut(sentence, cut_all=False)
                for word in words:
                    if word != '\n':
                        f2.write(word + ' ')
                    else:
                        f2.write('\n')

    f.close()
    f2.close()


if __name__ == '__main__':
    """
    prog : 程式名稱
    formatter_class : help信息输出格式
    description : -help 所顯示的文本
    """
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]),
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=__doc__)

    parser.add_argument("input", help="input file")

    # add_argument_group 這個function是為了讓-h的時候顯示的參數可以依照組別去放
    groupO = parser.add_argument_group('Output')
    groupO.add_argument("-o", "--output", default="output", help="output file")

    groupP = parser.add_argument_group('Processing')
    # w只存斷詞後結果，t是跟著詞性一起存
    groupP.add_argument("-m", "--model", default="w", choices=["w", "t"],
                        help="w:only save word , t: save word along with Part of Speech")
    groupP.add_argument("-s", "--save", nargs='+', help="only save specific POS. [Priority: Save > remove]")
    groupP.add_argument("-r", "--remove", nargs='+', help="only remove specific POS. [Priority: Save > remove]")

    # 解析參數
    args = parser.parse_args()
    PosTokenizer(args.input, args.output, args.model, save=args.save, remove=args.remove)
