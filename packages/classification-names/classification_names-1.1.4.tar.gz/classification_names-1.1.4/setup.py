# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: it-wqll
# Mail: wangqiang6480@163.com
# Created Time:  2018-4-16 19:17:34
#############################################

from setuptools import setup, find_packages

setup(
    name="classification_names",  # 这里是pip项目发布的名称
    version="1.1.4",  # 版本号，数值大的会优先被pip
    keywords=("pip", "classification_names"),
    description="人名,公司或机构名称分类",
    long_description="",
    license="MIT Licence",

    url="https://gitlab.kingdomai.com/wangqiang/name_classification/wangqiang/classification_names",  # 项目相关文件地址，一般是github
    author="it-wqll",
    author_email="wangqiang6480@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["numpy==1.15.4", "scikit_learn==0.20.2", "atlas==0.27.0"]  # 这个项目需要的第三方库
)
