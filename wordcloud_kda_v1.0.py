#!/usr/bin/python
# -*- coding: utf-8 -*-

print('------------- START Word_Cloud_KDA -------------')

# ライブラリのインポート
import os
import sys
import traceback
import datetime
import matplotlib.pyplot as plt
import pandas as pd

from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
from chardet.universaldetector import UniversalDetector

d = datetime.datetime.today()
msg = ' INFO: library import done'
print(d.strftime("%Y-%m-%d %H:%M:%S") + msg)

# 日本語文字フォントファイルのパス（MSゴシック以外に変えてもOK）
font_file_path = r"C:/WINDOWS/Fonts/msgothic.ttc"


# 関数の定義
# 文字コード確認関数
def check_encode(target_file):
    detector = UniversalDetector()
    with open(target_file, 'rb') as f:
        detector.reset()
        for line in f.readlines():
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result['encoding']


# Word Cloud作成関数
def create_wordcloud(target_file, file_encode):
    # ファイル読み込み
    try:
        f = open(target_file, 'r', encoding=file_encode)
        target_texts = f.readlines()
        f.close()
    except:
        msg = ' ERROR: ファイルの読み込みに失敗しました。文字化け等の問題が無いことを確認ください。'
        d = datetime.datetime.today()
        print(d.strftime("%Y-%m-%d %H:%M:%S") + msg)

        print('対象ファイル:')
        print(target_file)
        print('')

        print('エラーメッセージ:')
        print(traceback.format_exc())

        msg2 = 'なお、本プログラムの対象ファイルの推奨文字コードは UTF-8 です。'
        msg3 = '対象の文章を、メモ帳などのテキストエディターに UTF-8 で保存して、再度実行してみてください。'

        print(msg2)
        print(msg3)
        print('')
        print('Enterキーを押して終了します')
        input()
        sys.exit(1)

    # 文章を分解
    t = Tokenizer()
    words = []
    for s in target_texts:
        for token in t.tokenize(s):
            s_token = token.part_of_speech.split(',')
            # 一般名詞、自立動詞、自立形容詞を抽出
            # ただし、「し」等の１文字の動詞を除く
            if (s_token[0] == '名詞' and s_token[1] == '一般') \
            or (s_token[0] == '動詞' and s_token[1] == '自立' and len(token.surface) >= 2) \
            or (s_token[0] == '形容詞' and s_token[1] == '自立'):
                words.append(token.surface)

    # WordCloudの描画
    words_space = ' '.join(map(str, words))
    wc = WordCloud(background_color="white", font_path=font_file_path, width=1000, height=600)
    wc.generate(words_space)
    plt.figure(figsize=(15, 9))
    plt.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False, length=0)
    plt.imshow(wc)
    plt.savefig('wordcloud_'+target_file.split('.txt')[0]+'.png')
    plt.close()

    # 単語の出現数のリスト
    word_count = pd.DataFrame(pd.DataFrame([words]).T[0].value_counts()).reset_index()
    word_count.columns = ['word', 'count']
    out_csv = 'wordcloud_'+target_file.split('.txt')[0]+'.csv'
    try:
        word_count.to_csv(out_csv, index=False, encoding='cp932')
    except:
        word_count.to_csv(out_csv, index=False, encoding='utf-8')
    return 0


# main処理
if __name__ == '__main__':

    # フォントファイルの存在確認
    if not os.path.isfile(font_file_path):
        msg = ' ERROR: フォントファイル（' + font_file_path + '）が見つかりません。'
        d = datetime.datetime.today()
        print(d.strftime("%Y-%m-%d %H:%M:%S") + msg)
        print('Enterキーを押して終了します')
        input()
        sys.exit(1)

    msg = ' INFO: font file check done'
    d = datetime.datetime.today()
    print(d.strftime("%Y-%m-%d %H:%M:%S") + msg)

    # txt形式ファイルの取得
    txt_files = []
    files_in_current_dir = os.listdir('.')
    for x in files_in_current_dir:
        if x.endswith('.txt'):
            txt_files.append(x)

    # txt形式ファイルが1つもない場合は終了
    if len(txt_files) == 0:
        msg = ' ERROR:「.txt」形式のファイルがフォルダ内に見つかりません。'
        d = datetime.datetime.today()
        print(d.strftime("%Y-%m-%d %H:%M:%S") + msg)
        print('Enterキーを押して終了します')
        input()
        sys.exit(1)

    msg = ' INFO: target text files:' + ' ' + str(txt_files)
    d = datetime.datetime.today()
    print(d.strftime("%Y-%m-%d %H:%M:%S") + msg)

    # ループ処理
    for target_file in txt_files:
        # 文字コード確認
        encode = check_encode(target_file)
        # Word Cloud作成
        create_wordcloud(target_file, encode)
        msg = ' INFO: ' + target_file + ' is done'
        d = datetime.datetime.today()
        print(d.strftime("%Y-%m-%d %H:%M:%S") + msg)

    msg = ' INFO: program execution is done'
    d = datetime.datetime.today()
    print(d.strftime("%Y-%m-%d %H:%M:%S") + msg)
    print('Enterキーを押して終了します')
    input()
    print('------------- END Word_Cloud_KDA -------------')
    sys.exit(0)
