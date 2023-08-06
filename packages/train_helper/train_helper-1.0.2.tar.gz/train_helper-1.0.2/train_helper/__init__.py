import matplotlib.pyplot as plt
from tqdm import tqdm
from random import shuffle
from keras.utils import plot_model
from simple_pickle import *
import os
import numpy as np
from keras.preprocessing.sequence import pad_sequences


def 柱状图(x_input):
    query_count = [len(query) for query in tqdm(x_input)]
    query_count = [(q, query_count.count(q)) for q in tqdm(list(set(query_count)))]
    num_list = [i[1] for i in tqdm(query_count)]
    x = list(range(len(num_list)))
    total_width, n = 0.8, 1
    width = total_width / n
    plt.bar(x, num_list, width=width, label='query')
    for i in range(len(x)):
        x[i] = x[i] + width
    plt.legend()
    plt.show()


def 打乱数据(datalist):
    shuffle(datalist)


def 模型结构(model):
    plot_model(model, to_file='model.png', show_shapes=True)


def 这里():
    return os.path.dirname(__file__)


def 停用词():
    return read_pickle(os.path.join(这里(), 'stopword'))


def 路径(path1,path2):
    return os.path.join(path1, path2)


def 字向量():
    return read_pickle(os.path.join(这里(), 'single_word2vec'))


def 制作词向量(word2vector):
    word_index = {}
    embedding_matrix = []
    embedding_matrix.append(np.zeros(300))
    for i, word in enumerate(word2vector.keys()):
        word_index[word] = i + 1
        embedding_matrix.append(word2vector[word])
    embedding_matrix = np.array(embedding_matrix)
    write_pickle(word_index, 'word_index')
    np.save('embedding_matrix', embedding_matrix)


def 文本转序列(word_index, sentences):
    inputs = []
    for x_in in tqdm(sentences):
        input_x = []
        for word in x_in:
            try:
                input_x.append(word_index[word])
            except:
                input_x.append(0)
        inputs.append(input_x)
    return pad_sequences(inputs, padding='post')
