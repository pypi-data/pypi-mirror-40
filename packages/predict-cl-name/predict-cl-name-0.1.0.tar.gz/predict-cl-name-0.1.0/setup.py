# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: it-wqll
# Mail: wangqiang6480@163.com
# Created Time:  2018-4-16 19:17:34
#############################################

from setuptools import setup, find_packages

setup(
    name="predict-cl-name",  # 这里是pip项目发布的名称
    version="0.1.0",  # 版本号，数值大的会优先被pip
    keywords=("pip", "predict-cl-name", "featureextraction"),
    description="An feature extraction algorithm",
    long_description="An feature extraction algorithm, improve the FastICA",
    license="MIT Licence",

    url="https://gitlab.kingdomai.com/wangqiang/person_company_name_classification/tree/wangqiang/predict-cl-name",  # 项目相关文件地址，一般是github
    author="it-wqll",
    author_email="wangqiang6480@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["numpy==1.15.4", "scikit_learn==0.20.2", "atlas==0.27.0"]  # 这个项目需要的第三方库
)
