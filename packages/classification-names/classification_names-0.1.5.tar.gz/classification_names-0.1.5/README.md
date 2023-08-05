# 人名、公司或机构名分类文档说明

## 总共分为两大模块，训练模块(train_message)和预测模块(predict_person_company_name)

### 训练模块(train_message)包含以下几个模块：

read_person_name ：读取所有人名的模块

read_company_name：读取所有公司或机构模块

split_data_with_label：划分训练集模块

load_corpus：导入所有人名和公司或机构模块

fun_label：把测试标签编码为目标变量

count_vect_t：把训练集（即划分后的样本）转换为特征向量

count_vect_v：把测试集（即划分后的样本）转换为特征向量

train_model：训练模块，传入训练样本，测试样本，进行训练和保存模型

train_main：训练的主模块，传入训练数据即可

### 预测模块(predict_person_company_name)包含以模块：

#### predict_name:传入要预测的人名   或  公司或机构名即可

### 安装使用

#### 1、pip install classification_names

#### 预测模块使用：

from classification_names import predict_person_company_name

predict_person_company_name.predict_name(args)

说明：

args 是要预测的人名  或  公司或机构

#### 训练模块使用：

from classification_names import train_message

train_message.train_main(person_name_lis, company_name_lis, data_n=100000, corpus_n=50000)

说明：

person_name_lis ，是人名数据，列表形式，如:[file1,file2]

company_name_lis ，是公司或机构数据，列表形式，如:[file1,file2]

data_n，表示数据量的大小，默认值为 100000

corpus_n，表示要训练的数据量，默认值为 50000













