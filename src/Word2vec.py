import multiprocessing
import os
import sys
import config

from gensim.models import Word2Vec
from gensim.models.word2vec import PathLineSentences

file_path = config.file_path

if __name__ == '__main__':
    input_dir = file_path
    file_list = os.listdir(file_path)
    for i in range(0, len(file_list)):
        file_list[i] = file_path + file_list[i]

    model = Word2Vec(  # PathLineSentences(input_dir),
        file_list,
        size=200, window=5, min_count=5,
        workers=multiprocessing.cpu_count(), iter=10)
    model.save(file_path+'model.bin')
    model.wv.save_word2vec_format(file_path+'model.txt', binary=False)
