# -*- coding: utf-8 -*-
import os, argparse, subprocess
def get_args():
    """Return args"""

    parser = argparse.ArgumentParser(
        description='Generate KCM (correlation model).')
    parser.add_argument('-i', '--input_dir',
                        help='input raw data directory (default: %(default)s)',
                        required=True)
    parser.add_argument('-wiki', '--wikiFile',
                        help='input raw wiki data file name (default: %(default)s)',
                        required=True)
    parser.add_argument('-o', '--output_dir',
                        help='ouput data directory path (default: %(default)s)',
                        required=True)
    args = parser.parse_args()
    return args
def rename_extrac_files_and_expand_jiebaDict(args, folderPre):
    """Rename extracted wiki dir, etc AA, AB. And also get proper Noun from those Wiki text into dictionary to do Word Segmentation.

    Args:
        args: input arguments, use args.input_dir.
        folderPre: Prefix of folder.

    Returns:
        None.
    """

    file_list = []  # wiki files
    for (dir_path, dir_names, file_names) in os.walk(args.input_dir):
        if dir_names == []:
            langDir = dir_path.split('/')[0]
            for file_name in file_names:
                subprocess.call(['python2', 'preprocess_lib/detectPN.py', dir_path + '/' + file_name, langDir + '/' + 'jieba_expandDict_s.txt'])
                subprocess.call(['opencc', '-i', dir_path + '/' + file_name, '-o', dir_path + '/' + file_name + '_tradCHT'])
                subprocess.call(['python2', 'preprocess_lib/detectPN.py', dir_path + '/' + file_name, langDir + '/' + 'jieba_expandDict_trad.txt'])
                # detectPN 這個script會先把wiki_00這類的文章專有名詞先挑出來，加入到結巴的字典裏面，然後再把wiki轉成繁體字然後再挑專有名詞出來，所以會做出繁簡兩種字典擴充包

        for dirName in dir_names:
            subprocess.call(['mv', dir_path+'/'+dirName, dir_path+'/'+dirName + folderPre])

    if not file_list:
        exit()

    return file_list

def main():
    """Main function"""
    args = get_args()
    subprocess.call(['python2', 'preprocess_lib/WikiExtractor.py', args.wikiFile, '-o', args.output_dir])
    folderPre = args.wikiFile.split('.')[0]
    rename_extrac_files_and_expand_jiebaDict(args, folderPre)

if __name__ == '__main__':
    main()