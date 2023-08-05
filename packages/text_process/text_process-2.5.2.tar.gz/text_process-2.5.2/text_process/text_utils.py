# -*- coding: utf-8 -*-
# @Time    : 18-9-28 下午1:47
# @Author  : duyongan
# @FileName: text_utils.py
# @Software: PyCharm
import re
from simple_pickle import utils
from text_process.text import Text
import nltk
import os
import numpy as np
from jieba import posseg

# from cppjieba_py import posseg
# from numba import jit


posseg.initialize()
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
here = os.path.dirname(__file__)
stopwords = utils.read_pickle(here + '/stopwords')
idf_map = utils.read_pickle(here + '/idf_map')


def text2sencents_zh(text):
    text = re.sub('\u3000|\r|\t|\xa0', '', text)
    text = re.sub('？”|！”|。”', '”', text)
    sentences = re.split("([。！？……])", text)
    sentences.append('')
    sentences = ["".join(i) for i in zip(sentences[0::2], sentences[1::2])]
    last_sentences = []
    for sentence in sentences:
        last_sentences += [senten.replace('\n', '').strip() for senten in sentence.split('\n\n')
                           if senten.replace('\n', '').strip()]
    return last_sentences


def text2sencents_en(text):
    text = re.sub('\u3000|\r|\t|\xa0|\n', '', text)
    sentences = tokenizer.tokenize(text)
    return sentences


def sort_keys_weights(keys, weights, return_tuple=False):
    keys_weights = dict(zip(keys, weights))
    keys_weights = sorted(keys_weights.items(), key=lambda k: k[1], reverse=True)
    if return_tuple:
        return keys_weights
    keys = [term[0] for term in keys_weights]
    return keys


def text_process_zh_single(text):
    text = re.sub('\u3000|\r|\t|\xa0|\n', '', text)
    text = posseg.lcut(text)
    text_n_list = [word_.word for word_ in text if
                   len(word_.word) > 1 and word_.word not in stopwords and
                   word_.flag in ['n', 'v', 'ns', 'nt', 'nr', 'ni', 'nl', 'nz',
                                  'nrf', 'nsf', 'nrj', 'nr1', 'nr2']]
    return text_n_list


def text_process_zh_not_single(text):
    words = [tuple_ for tuple_ in list(posseg.cut(text))
             if list(tuple_)[0].strip() and len(list(tuple_)[0].strip()) > 1]
    words2 = []
    temp = ''
    enstart = False
    for i in range(len(words)):
        if words[i].flag in ['n', 'ns', 'nt', 'nr', 'ni', 'nl',
                             'nz', 'nrf', 'nsf', 'nrj', 'nr1',
                             'nr2'] and len(temp) < 3 and not enstart:
            if words[i].word not in stopwords:
                temp = temp + words[i].word
            if i == len(words) - 1:
                if temp.strip() != '':
                    words2.append(temp)
        else:
            if temp.strip() != '' and not enstart:
                words2.append(temp)
                temp = ''
    return words2


def text_process_en(text):
    text = re.sub('\u3000|\r|\t|\xa0|\n', '', text)
    text = text.replace(',', ' ')
    text_list = text.split()
    texter = Text(text_list)
    text_n_list = texter.collocations()
    return text_n_list


def range_easy(a_object):
    return range(len(a_object))


def duplicate(a_list):
    return list(set(a_list))


def getKeywords_zh_single(text, num=5):
    moshengci_weight = max(idf_map.values())
    text_n_list = text_process_zh_single(text)
    keywords_set = duplicate(text_n_list)
    keywords_count = [text_n_list.count(keyword) for keyword in keywords_set]
    keywords_weight = []
    for i, keyword in enumerate(keywords_set):
        keyword_count = keywords_count[i]
        len_keyword = len(keyword)
        try:
            idf_map[keyword]
        except:
            idf_map[keyword] = moshengci_weight
        keywords_weight.append(len_keyword * np.sqrt(keyword_count) * idf_map[keyword])
    return sort_keys_weights(keywords_set, keywords_weight)[:min(num, len(keywords_set))]


def getKeywords_zh_not_single(text, num=5):
    moshengci_weight = max(idf_map.values())
    text_n_list = text_process_zh_not_single(text)
    keywords_set = duplicate(text_n_list)
    keywords_count = [text_n_list.count(keyword) for keyword in keywords_set]
    keywords_weight = []
    for i, keyword in enumerate(keywords_set):
        keyword_count = keywords_count[i]
        len_keyword = len(keyword)
        try:
            idf_map[keyword]
        except:
            idf_map[keyword] = moshengci_weight
        keywords_weight.append(len_keyword * np.sqrt(keyword_count) * idf_map[keyword])
    return sort_keys_weights(keywords_set, keywords_weight)[:min(num, len(keywords_set))]


def getKeywords_en(text, num=5):
    moshengci_weight = max(idf_map.values())
    text_n_list = text_process_en(text)
    keywords_set = duplicate(text_n_list)
    keywords_count = [text_n_list.count(keyword) for keyword in keywords_set]
    keywords_weight = []
    for i, keyword in enumerate(keywords_set):
        keyword_count = keywords_count[i]
        len_keyword = len(keyword)
        try:
            idf_map[keyword]
        except:
            idf_map[keyword] = moshengci_weight
        keywords_weight.append(len_keyword * np.sqrt(keyword_count) * idf_map[keyword])
    return sort_keys_weights(keywords_set, keywords_weight)[:min(num, len(keywords_set))]


def compare_two_txt(text1, text2):
    words1 = text_process_zh_single(text1)
    words2 = text_process_zh_single(text2)
    same_len = len([val for val in words1 if val in words2])
    return (same_len / max(0.1, len(words1)) + same_len / max(0.1, len(words2))) / 2


def cos(i, j):
    return np.nan_to_num(np.dot(i, j) / (np.linalg.norm(i) * np.linalg.norm(j)))


def sum_0(vec):
    return np.sum(vec, axis=0) / max(len(vec), 0.9999)


class compare_bot:
    def __init__(self):
        self.__here = os.path.dirname(__file__)
        self.__single_word2vec = utils.read_pickle(self.__here + '/single_word2vec')

    def compare_two_txt_accuracy(self, text1, text2, fast=False):
        words1 = getKeywords_zh_single(text1, 20)
        words2 = getKeywords_zh_single(text2, 20)
        vec1 = []
        for word in words1:
            for w in list(word):
                try:
                    vec1.append(self.__single_word2vec[w])
                except:
                    pass
        vec1 = sum_0(vec1)  # np.sum(vec1, axis=0) / max(len(vec1),0.9999)
        vec2 = []
        for word in words2:
            for w in list(word):
                try:
                    vec2.append(self.__single_word2vec[w])
                except:
                    pass
        vec2 = sum_0(vec2)  # np.sum(vec2, axis=0) / max(len(vec2),0.9999)
        result = cos(vec1, vec2)
        if type(result) != np.float64:
            result = 0.0
        return result

    def compare_two_word(self, word1, word2):
        vec1 = []
        for w in list(word1):
            try:
                # print(single_word2vec[w])
                vec1.append(self.__single_word2vec[w])
            except:
                pass
        vec1 = sum_0(vec1)  # np.sum(vec1, axis=0) / max(len(vec1), 0.9999)
        vec2 = []
        for w in list(word2):
            try:
                vec2.append(self.__single_word2vec[w])
            except:
                pass
        vec2 = sum_0(vec2)  # np.sum(vec2, axis=0) / max(len(vec2), 0.9999)
        result = cos(vec1, vec2)
        if type(result) != np.float64:
            result = 0.0
        return result


def getAbstract_zh(title, text, num=3):
    sentences = text2sencents_zh(text)
    vecs_sim = []
    for sentence in sentences:
        vecs_sim.append(compare_two_txt(title, sentence))
    abstract = sort_keys_weights(sentences, vecs_sim)[:min(num, len(sentences))]
    index_num = [sentences.index(sentence) for sentence in abstract]
    abstract = sort_keys_weights(abstract, index_num)
    return ''.join(abstract)


def getAbstract_en(title, text, num=3):
    sentences = text_process_en(text)
    vecs_sim = []
    for sentence in sentences:
        vecs_sim.append(compare_two_txt(title, sentence))
    abstract = sort_keys_weights(sentences, vecs_sim)[:min(num, len(sentences))]
    index_num = [sentences.index(sentence) for sentence in abstract]
    abstract = sort_keys_weights(abstract, index_num)
    return ''.join(abstract)

# text="""
# 原标题：（时政）习近平对全国党委秘书长会议作出重要指示 强调坚决维护党中央权威和集中统一领导 全力推动党中央决策部署贯彻落实
#
# 　　新华社北京10月20日电全国党委秘书长会议19日至20日在京召开。会前，中共中央总书记、国家主席、中央军委主席习近平作出重要指示。他指出，党委办公厅（室）作为党委的综合部门，是党委履行领导职责的参谋助手。党的十八大以来，各级党委办公厅（室）服务大局、勇于担当、辛勤工作，为推动党和国家事业发展作出了重要贡献。面向新时代，要进一步增强“四个意识”，加强理论武装，提高队伍素质，弘扬优良传统，坚持改革创新，坚决维护党中央权威和集中统一领导，全力推动党中央决策部署贯彻落实，全面提高“三服务”工作水平，建设让党放心、让人民满意的模范机关。　
#
# 　　中共中央政治局委员、中央书记处书记、中央办公厅主任丁薛祥在会上讲话强调，各级党委办公厅（室）要旗帜鲜明讲政治，以正确的认识和行动坚决维护习近平总书记核心地位、坚决维护党中央权威和集中统一领导。要适应新形势新任务新挑战，进一步抓好理论武装、机构职能优化、工作机制创新、干部队伍建设，不断推动“三服务”事业创新发展。　　
#
# 　　会议总结交流了党的十八大以来党委办公厅（室）工作的成效和经验，研究了提高“三服务”工作水平的任务和措施，就党委办公厅（室）近期重点工作进行了具体部署。（完）
# """
# num=4000
# compare_botor =compare_bot()
# import time
# start_time = time.time()
# for i in range(num):
#     compare_botor.compare_two_txt_accuracy(text,text)
# end_time = time.time()
# print(end_time - start_time)
