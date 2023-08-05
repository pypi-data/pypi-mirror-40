import pickle

with open("count.pickle", 'rb') as f:
    count_model = pickle.load(f)

with open("classifier.pickle", 'rb') as f:
    model = pickle.load(f)


def predict_name(args):
    try:
        xvalid_count = count_model.transform([args])
        prediction = model.predict(xvalid_count)
        print("预测是：{}类".format(prediction))
        if prediction == 0:
            pred_text = "人名"
            print("您输入的是：{}, 是：{}".format(args, pred_text))
            return pred_text
        else:
            pred_text = "公司或机构"
            print("您输入的是：{}, 是：{}".format(args, pred_text))
            return pred_text
    except Exception as err:
        raise err
