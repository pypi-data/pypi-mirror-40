from sklearn.naive_bayes import MultinomialNB
from src import data_transfer_split
from src import train_model
from src.get_train_data import ReadName
from settings.config import MergeLog


def main(corpus):
    input_x, input_y, train_x, valid_x, train_y, valid_y = data_transfer_split.load_corpus(corpus)
    train_y, valid_y = data_transfer_split.fun_label(train_y, valid_y)
    xtrain_count = data_transfer_split.count_vect_t(train_x, input_x)
    xvalid_count = data_transfer_split.count_vect_v(valid_x, input_x)
    # 特征为计数向量的朴素贝叶斯
    clf = MultinomialNB()
    MergeLog.info(".....................准备训练模型...........................")
    accuracy = train_model.train_model(clf, xtrain_count, train_y, xvalid_count, valid_y)
    MergeLog.info("NB, Tf-idf Vectors: {}".format(accuracy))


if __name__ == '__main__':
    read = ReadName()
    read.read_person_name()
    read.read_company_name()
    corpus = read.word_list
    main(corpus)
