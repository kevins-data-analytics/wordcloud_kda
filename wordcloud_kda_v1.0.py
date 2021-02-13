#!/usr/bin/python
# -*- coding: utf-8 -*-

print('------------- START Word_Cloud_KDA -------------')
# ライブラリのインポート
import os
import sys
import datetime
import matplotlib.pyplot as plt
import pandas as pd

from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
from chardet.universaldetector import UniversalDetector

d = datetime.datetime.today()
print(d.strftime("%Y-%m-%d %H:%M:%S")+' INFO: libruary import done')

# 日本語文字フォントファイルのパス（MSゴシック以外に変えてもOK）
font_file_path=r"C:/WINDOWS/Fonts/msgothic.ttc"


# 関数の定義
## 文字コード確認関数
def check_encode(target_file):
    encode_dict = {}
    detector = UniversalDetector()
    with open(target_file, 'rb') as f:
        detector.reset()
        for line in f.readlines():
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result['encoding']

## Word Cloud作成関数
def create_wordcloud(target_file, file_encode):
    # ファイル読み込み
    f = open(target_file, 'r', encoding=file_encode)
    target_texts = f.readlines()
    f.close()

    # 文章を分解
    t = Tokenizer()
    words=[]
    for s in target_texts:
        for token in t.tokenize(s):
                split_token = token.part_of_speech.split(',')
                # 一般名詞、自立動詞（「し」等の１文字の動詞を除く）、自立形容詞を抽出
                if (split_token[0] == '名詞' and split_token[1] == '一般') \
                or (split_token[0] == '動詞' and split_token[1] == '自立' and len(token.surface)>=2) \
                or (split_token[0] == '形容詞' and split_token[1] == '自立'):
                    words.append(token.surface)

    # WordCloudの描画
    words_space = ' '.join(map(str, words))
    wc = WordCloud(background_color="white", font_path=font_file_path, width=1000,height=600)
    wc.generate(words_space)
    plt.figure(figsize=(15,9))
    plt.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False, length=0)
    plt.imshow(wc)
    plt.savefig('wordcloud_'+target_file.split('.txt')[0]+'.png')
    plt.close()
    
    # 単語の出現数のリスト
    word_count=pd.DataFrame(pd.DataFrame([words]).T[0].value_counts()).reset_index()
    word_count.columns=['word','count']
    try:
        word_count.to_csv('wordcloud_'+target_file.split('.txt')[0]+'.csv', index=False, encoding='cp932')
    except:
        word_count.to_csv('wordcloud_'+target_file.split('.txt')[0]+'.csv', index=False, encoding='utf-8')
    return 0

# main処理
if __name__ == '__main__':
    
    # フォントファイルの存在確認
    if not os.path.isfile(font_file_path):
        print('フォントファイル（'+font_file_path+'）が見つかりません。')
        print('Enterキーを押して終了します')
        input()
        sys.exit(1)
    
    d = datetime.datetime.today()
    print(d.strftime("%Y-%m-%d %H:%M:%S")+' INFO: font file check done')
    
    # txt形式ファイルの取得
    txt_files=[]
    files_in_current_dir=os.listdir('.')
    for x in files_in_current_dir:
        if x.endswith('.txt'):
            txt_files.append(x)
    
    if len(txt_files)==0:
        print('「.txt」形式のファイルがフォルダ内に見つかりません。')
        print('Enterキーを押して終了します')
        input()
        sys.exit(1)
    
    d = datetime.datetime.today()
    print(d.strftime("%Y-%m-%d %H:%M:%S")+' INFO: target text files:'+' '+str(txt_files))
    
    # ループ処理
    for target_file in txt_files:
        # 文字コード確認
        encode=check_encode(target_file)
        # Word Cloud作成
        create_wordcloud(target_file, encode)
        d = datetime.datetime.today()
        print(d.strftime("%Y-%m-%d %H:%M:%S")+' INFO: '+target_file+' is done')
    
    #sys.exit(0)
    d = datetime.datetime.today()
    print(d.strftime("%Y-%m-%d %H:%M:%S")+' INFO: program execution is done')
    print('Enterキーを押して終了します')
    input()
    print('------------- END Word_Cloud_KDA -------------')
    sys.exit(0)
