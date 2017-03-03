#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import glob
import json
import chardet
import collections

files = glob.glob('*.json')


def code_detector(path_to_file):
    """
    Определение кодировки файла
    :param path_to_file:
    :return:
    """
    with open(path_to_file, 'rb') as f:
        lines = f.read()
        result = chardet.detect(lines)
        if result['encoding'] is None:
            raise Exception('Неизвестная кодировка файла!', path_to_file)
        else:
            return result['encoding']


def file_opening(file_name, news_list):
    """
    Открытие файла
    :param file_name:
    :param news_list:
    :return:
    """
    with open(file_name, encoding=code_detector(file_name)) as country_news_file:
        country_news = json.load(country_news_file)
        for item in country_news['rss']['channel']['item']:
            news_list.append(str(item['title']))
            news_list.append(str(item['description']))
        print('------------\n{0}'.format(file_name))
        print(code_detector(file_name))
        print('\n{0}\n'.format(country_news['rss']['channel']['title']))


def word_search(news_list, words_list):
    """
    Создание списка слов
    :param news_list:
    :param words_list:
    :return:
    """
    all_words = []
    for item in news_list:
        for i in filter(None, re.split('\W|\d', item)):
            if len(i) > 6:
                all_words.append(i)
    r = re.compile('[а-яА-Я]')
    for w in filter(r.match, all_words):
        words_list.append(w)


def most_common_words(words_list):
    """
    Поиск самых часто используемых слов
    :param words_list:
    :return:
    """
    c = collections.Counter()
    for word in words_list:
        c[word] += 1
    for count, letter in c.most_common(10):
        print('{0}: {1}'.format(count, letter))


for f in files:
    news = []
    words = []
    file_opening(f, news)
    word_search(news, words)
    most_common_words(words)
