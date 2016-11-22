"""Input text file of sentences, output text file of terms (English)

Output format: '/term1/term2/term3\n...'
"""

import argparse
import re
import os.path, sys

import nltk
from nltk.stem.wordnet import WordNetLemmatizer


# combine more than one word into a term
# EX: new york ->  new-york
def extract_entity_names(t):
    entity_names = []
    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(('-'.join([child[0] for child in t]), 'NNP'))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))
    else:
        entity_names.append(t)
    return entity_names


# 將單字轉小寫並將動詞及名詞轉換成原型
def normalization(word, flag):
    word = word.lower()
    pat = '[a-z]'
    # 過略標點符號
    if re.search(pat, str(flag[0]).lower()) != None:
        # lemmatize : 把詞變成原型
        if str(flag)[0].lower() == 'n':
            word = WordNetLemmatizer().lemmatize(word, 'n')
        elif str(flag)[0].lower() == 'v':
            word = WordNetLemmatizer().lemmatize(word, 'v')
        return word, flag
    else:
        return '', ''


def SegmentationTos(sentence):
    # term's segmentation
    # 進行英文段詞
    sentence_tokenize = nltk.word_tokenize(sentence)

    # term's tagging
    # 對段完的詞進行詞性標記
    term_tagging = nltk.pos_tag(sentence_tokenize)

    # term's NER(Named Entity Recognition)
    # 對詞性標記完的字進行命名實體識別
    # EX: china -> pos_tag (NNP) -> ne_chunk (GPE)
    temp = nltk.ne_chunk(term_tagging, binary=True)

    return extract_entity_names(temp)


def PosTokenizer(input, output, mission, save=None, remove=None):
    inf = open(input, 'r')
    outf = open(output, 'a')
    if save != None and remove != None:
        print
        'can\'t set save and remove at once'
    elif (mission == "w"):
        for sentence in inf:
            if sentence != '\n':
                entity_names = SegmentationTos(sentence)

                if save == None and remove == None:
                    for word, flag in entity_names:
                        word, flag = normalization(word, flag)

                        if word != '' and word != '\n':
                            outf.write("/" + word)

                    outf.write('\n')

                else:
                    if not save == None:
                        for word, flag in entity_names:
                            word, flag = normalization(word, flag)

                            if word != '' and str(flag)[
                                0].lower() in save and word != '\n':
                                outf.write("/" + word)

                        outf.write('\n')

                    else:
                        for word, flag in entity_names:
                            word, flag = normalization(word, flag)
                            if word != '' and str(flag)[
                                0].lower() not in remove and word != '\n':
                                outf.write("/" + word)

                        outf.write('\n')
    else:
        for sentence in inf:
            if sentence != '\n':
                entity_names = SegmentationTos(sentence)

                if save == None and remove == None:
                    for word, flag in entity_names:
                        word, flag = normalization(word, flag)

                        if word != '' and word != '\n':
                            outf.write(
                                "/" + word + " " + flag.encode(
                                    'utf8'))

                    outf.write('\n')

                else:
                    if not save == None:
                        for word, flag in entity_names:
                            word, flag = normalization(word, flag)

                            if word != '' and str(flag)[
                                0].lower() in save and word != '\n':
                                outf.write("/" + word.encode(
                                    'utf8') + " " + flag)

                        outf.write('\n')

                    else:
                        for word, flag in entity_names:
                            word, flag = normalization(word, flag)
                            if word != '' and str(flag)[
                                0].lower() not in remove and word != '\n':
                                outf.write("/" + word.encode(
                                    'utf8') + " " + flag)

                        outf.write('\n')


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

    groupO = parser.add_argument_group('Output')
    groupO.add_argument("-o", "--output", default="output", help="output file")

    groupP = parser.add_argument_group('Processing')
    groupP.add_argument("-m", "--model", default="w", choices=["w", "t"],
                        help="w:only save word , t: save word and Part of Speech")
    groupP.add_argument("-s", "--save", nargs='+',
                        help="only save specific POS. [Priority: Save > remove]")
    groupP.add_argument("-r", "--remove", nargs='+',
                        help="only remove specific POS. [Priority: Save > remove]")

    # 解析參數
    args = parser.parse_args()
    PosTokenizer(args.input, args.output, args.model, save=args.save,
                 remove=args.remove)
