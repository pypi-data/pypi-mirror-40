import numpy as np
from random import shuffle
# 导入数据集预处理、特征工程和模型训练所需的库
from sklearn import model_selection, naive_bayes, metrics, preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle


def read_person_name(person_name_list, data_n, word_list):
    try:
        for file in person_name_list:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                for i in range(data_n):
                    text = f.readline()
                    if not text:
                        break
                    word_dict = {}
                    text = text.replace("\n", "")
                    if text not in ["\ufeffBy@萌名", "2018.12.03", " ", "By@萌名"]:
                        word_dict[text] = "人名"
                        word_list.append(word_dict)
    except Exception as err:
        raise err

    return word_list


def read_company_name(company_name_list, data_n, word_list):
    try:
        for file in company_name_list:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                for i in range(data_n):
                    text = f.readline()
                    if not text:
                        break
                    word_dict = {}
                    text = text.replace("\n", "")
                    if text not in ["\ufeffBy@萌名", "2018.12.03", "\n", "By@萌名"]:
                        word_dict[text] = "公司或机构"
                        word_list.append(word_dict)
    except Exception as err:
        raise err
    return word_list


def split_data_with_label(corpus, corpus_n):
    """
    将数据划分为训练数据和样本标签
    :param corpus:
    :return:
    """
    # 打乱数据，避免在采样的时候出现类别不均衡现象
    shuffle(corpus)
    texts, labels = [], []
    try:
        if corpus_n == "all":
            for dic in corpus:
                for key, value in dic.items():
                    texts.append(key)
                    labels.append(value)
    except Exception as err:
        raise err
    else:
        try:
            for dic in corpus[:corpus_n]:
                for key, value in dic.items():
                    texts.append(key)
                    labels.append(value)
        except Exception as err:
            raise err
    return texts, labels


def load_corpus(corpus, corpus_n):
    try:
        input_x, input_y = split_data_with_label(corpus, corpus_n)
        input_x = np.array(input_x)
        input_y = np.array(input_y)
    except Exception as err:
        raise err
    train_x, valid_x, train_y, valid_y = model_selection.train_test_split(input_x, input_y, shuffle=True)
    return input_x, input_y, train_x, valid_x, train_y, valid_y


def fun_label(train_y, valid_y):
    # label编码为目标变量
    encoder = preprocessing.LabelEncoder()
    train_y = encoder.fit_transform(train_y)
    valid_y = encoder.fit_transform(valid_y)
    return train_y, valid_y


def count_vect_t(train_x, input_x):
    # 创建一个向量计数器对象
    count_vect = TfidfVectorizer(analyzer="char", ngram_range=(2, 3))
    count_vect.fit(input_x)
    f = open("count_vect.pickle", "wb")
    pickle.dump(count_vect, f)
    f.close()
    xtrain_count = count_vect.transform(train_x)
    return xtrain_count


def count_vect_v(valid_x, input_x):
    # 创建一个向量计数器对象
    count_vect = TfidfVectorizer(analyzer="char", ngram_range=(2, 3))
    count_vect.fit(input_x)
    xvalid_count = count_vect.transform(valid_x)
    return xvalid_count


def train_model(classifier, feature_vector_train, label, feature_vector_valid, valid_y):
    # fit the training dataset on the classifier
    classifier.fit(feature_vector_train, label)
    predictions = classifier.predict(feature_vector_valid)
    count = 0  # 统计预测正确的结果个数
    for left, right in zip(predictions, valid_y):
        if left == right:
            count += 1
    # save model
    f = open("classifier.pickle", "wb")
    pickle.dump(classifier, f)
    f.close()
    # predict the labels on validation dataset
    return "准确率：{}, 训练集：{},  测试集：{}".format(metrics.accuracy_score(predictions, valid_y),
                                            classifier.score(feature_vector_train, label),
                                            classifier.score(feature_vector_valid, valid_y))


def train_main(person_name_lis, company_name_lis, data_n=100000, corpus_n=50000):
    try:
        person_list = []
        company_list = []
        person_lis = read_person_name(person_name_lis, data_n, person_list)
        company_lis = read_company_name(company_name_lis, data_n, company_list)
        person_lis.extend(company_lis)
        corpus = person_lis
        input_x, input_y, train_x, valid_x, train_y, valid_y = load_corpus(corpus, corpus_n)
        train_y, valid_y = fun_label(train_y, valid_y)
        xtrain_count = count_vect_t(train_x, input_x)
        xvalid_count = count_vect_v(valid_x, input_x)
        # 特征为计数向量的朴素贝叶斯
        clf_count = naive_bayes.MultinomialNB()
        accuracy = train_model(clf_count, xtrain_count, train_y, xvalid_count, valid_y)
        print("NB, Count Vectors: ", accuracy)
    except Exception as err:
        raise err



