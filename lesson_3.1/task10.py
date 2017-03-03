#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os.path
import chardet
from pprint import pprint


migrations = 'Advanced Migrations'
files = set(glob.glob(os.path.join(migrations, "*.sql")))
search_results = set()


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


def file_search(parameter, container):
    """
    Поиск файла по заданным параметрам
    :param parameter:
    :param container:
    :return:
    """
    for i in container:
        with open(i, encoding=code_detector(i)) as f:
            if parameter in f.read():
                search_results.add(i)


while True:
    file_search(input('Введите строку: '), files)
    if not search_results:
        continue
    else:
        pprint(search_results)
        print('Всего: {0}'.format(len(search_results)))
        files.intersection_update(search_results)
        search_results.clear()
