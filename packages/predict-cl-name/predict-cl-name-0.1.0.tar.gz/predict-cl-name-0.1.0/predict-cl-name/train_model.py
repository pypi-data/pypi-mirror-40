from sklearn import metrics
import pickle
import os
import time
from settings.config import MergeLog
path = os.path.abspath(os.path.join(os.path.dirname("__file__"), os.path.pardir))


def train_model(classifier, feature_vector_train, label, feature_vector_valid, valid_y):
    # fit the training dataset on the classifier
    MergeLog.info(".....................开始训练模型...........................")
    start_time = time.time()
    classifier.fit(feature_vector_train, label)
    MergeLog.info("模型训练结束,模型训练时间：{}s".format(time.time() - start_time))
    predictions = classifier.predict(feature_vector_valid)
    MergeLog.info("预测结果: {}".format(predictions))
    count = 0  # 统计预测正确的结果个数
    for left, right in zip(predictions, valid_y):
        if left == right:
            count += 1
    MergeLog.info("模型预测正确的结果个数: %d" % count)
    # save model
    MergeLog.info("............保存模型..............")
    f = open(path + "/data/classifier.pickle", "wb")
    pickle.dump(classifier, f)
    f.close()
    return "准确率：{}, 训练集：{},  测试集：{}".format(metrics.accuracy_score(predictions, valid_y),
                                            classifier.score(feature_vector_train, label),
                                            classifier.score(feature_vector_valid, valid_y))
