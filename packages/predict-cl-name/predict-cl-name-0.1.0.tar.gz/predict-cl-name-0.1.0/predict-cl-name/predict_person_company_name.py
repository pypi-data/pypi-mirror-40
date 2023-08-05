import pickle
import os

path = os.path.abspath(os.path.join(os.path.dirname("__file__")))
with open(path + "/data/count_vect.pickle", 'rb') as f:
    count_model = pickle.load(f)
with open(path + "/data/classifier.pickle", 'rb') as f:
    model = pickle.load(f)


def predict_name(args):
    xvalid_count = count_model.transform([args])
    prediction = model.predict(xvalid_count)
    if prediction == 0:
        pred_text = "人名"
        return "您输入的是：{}, 预测的结果是：{}".format(args, pred_text)
    else:
        pred_text = "公司或机构"
        return "您输入的是：{}, 预测的结果是：{}".format(args, pred_text)
