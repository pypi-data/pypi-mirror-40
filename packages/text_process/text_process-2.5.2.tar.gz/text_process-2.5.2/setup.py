# -*- coding: utf-8 -*-
# @Time    : 18-9-28 下午1:16
# @Author  : duyongan
# @FileName: setup.py
# @Software: PyCharm

from distutils.core import setup

setup(
    name='text_process',
    version='2.5.2',
    packages=['text_process'],
    author='Haydon',
    author_email='13261051171@163.com',
    description='easy utils for process text',
    package_data = {'text_process': ['*']},
    install_requires=['nltk','jieba','simple_pickle','numpy'],
    # long_description=open('README.md', encoding='utf-8').read(),
)