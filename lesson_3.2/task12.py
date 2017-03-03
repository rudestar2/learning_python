#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import requests


KEY = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
files = glob.glob('*.txt')


def file_reading(path_to_file):
    """
    Чтение из файла
    :param path_to_file: <str> path to file.
    :return:
    """
    with open(path_to_file) as text_file:
        text = text_file.read().strip()
        return text


def file_record(path_to_file, text_string):
    """
    Запись в файл
    :param path_to_file: <str> path to file.
    :param text_string: <str> text string.
    :return:
    """
    with open(path_to_file, 'w') as text_file:
        text_file.write(text_string)


def translate_it(text, lang):
    """
    YANDEX translation plugin

    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/

    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]

    :param text: <str> text for translation.
    :param lang: <str> target language.
    :return: <str> translated text.
    """
    params = {
        'key': KEY,
        'lang': lang,
        'text': text
    }
    response = requests.get(URL, params=params).json()
    return ' '.join(response.get('text', []))


for f in files:
    print('Файл:', f)
    lang_to_translate = input('Язык перевода?\n').lower()
    if not lang_to_translate or not lang_to_translate.isalpha():
        lang_to_translate = 'ru'
    file_record('New_{0}'.format(f), translate_it(file_reading(f), lang_to_translate))
