from random import shuffle
import numpy as np
from sklearn import preprocessing, model_selection
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from settings.config import MergeLog
import pickle

path = os.path.abspath(os.path.join(os.path.dirname("__file__"), os.path.pardir))


def split_data_with_label(corpus):
    """
    将数据划分为训练数据和样本标签
    :param corpus:
    :return:
    """
    # 打乱数据，避免在采样的时候出现类别不均衡现象
    shuffle(corpus)
    texts, labels = [], []
    n = 50000
    for dic in corpus[:n]:
        for key, value in dic.items():
            texts.append(key)
            labels.append(value)
    return texts, labels


def load_corpus(corpus):
    input_x, input_y = split_data_with_label(corpus)
    input_x = np.array(input_x)
    MergeLog.info("......................保存特征数据.....................")
    input_y = np.array(input_y)
    MergeLog.info("..................训练集与测试集数据划分..................")
    train_x, valid_x, train_y, valid_y = model_selection.train_test_split(input_x, input_y, shuffle=True)
    return input_x, input_y, train_x, valid_x, train_y, valid_y


def fun_label(train_y, valid_y):
    # label编码为目标变量
    MergeLog.info("................label编码为目标变量......................")
    encoder = preprocessing.LabelEncoder()
    train_y = encoder.fit_transform(train_y)
    valid_y = encoder.fit_transform(valid_y)
    return train_y, valid_y


def count_vect_t(train_x, input_x):
    MergeLog.info("....................将特征数据转化为词向量................")
    # 创建一个向量计数器对象
    count_vect = TfidfVectorizer(analyzer="char", ngram_range=(2, 3))
    count_vect.fit(input_x)
    f = open(path + "/data/count_vect.pickle", "wb")
    pickle.dump(count_vect, f)
    f.close()
    xtrain_count = count_vect.transform(train_x)
    return xtrain_count


def count_vect_v(valid_x, input_x):
    MergeLog.info("....................将测试数据转化为词向量................")
    # 创建一个向量计数器对象
    count_vect = TfidfVectorizer(analyzer="char", ngram_range=(2, 3))
    count_vect.fit(input_x)
    xvalid_count = count_vect.transform(valid_x)
    return xvalid_count
