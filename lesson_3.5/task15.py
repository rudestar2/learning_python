#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from urllib.parse import urlencode, urljoin

AUTHORIZE_URL = 'https://oauth.yandex.ru/authorize'
APP_ID = '83187537f557469f85269d32981ff40b'

auth_data = {
    'response_type': 'token',
    'client_id': APP_ID
}

print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))

TOKEN = 'AQAAAAAbJ6hxAAP6j9WnW21H60i5vukUcN1VOFc'


class YandexMetrika(object):
    _METRIKA_STAT_URL = 'https://api-metrika.yandex.ru/stat/v1/'
    _METRIKA_MANAGEMENT_URL = 'https://api-metrika.yandex.ru/management/v1/'
    token = None

    def __init__(self, token):
        self.token = token

    def get_header(self):
        return {
            'Content-Type': 'application.json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    @property
    def counter_list(self):
        url = urljoin(self._METRIKA_MANAGEMENT_URL, 'counters')
        headers = self.get_header()
        response = requests.get(url, headers=headers)
        counter_list = [c['id'] for c in response.json()['counters']]
        return counter_list

    def get_metrics_count(self, counter_id, metric):
        url = urljoin(self._METRIKA_STAT_URL, 'data')
        headers = self.get_header()
        params = {
            'id': counter_id,
            'metrics': 'ym:s:{}'.format(metric)
        }
        response = requests.get(url, params=params, headers=headers)
        metrics_count = response.json()['data'][0]['metrics'][0]
        return metrics_count


metrika = YandexMetrika(TOKEN)
counter_list = metrika.counter_list
for counter in counter_list:
    print('Суммарное количество визитов: {:.0f}'.format(metrika.get_metrics_count(counter, 'visits')))
    print('Количество уникальных посетителей: {:.0f}'.format(metrika.get_metrics_count(counter, 'users')))
    print('Число просмотров страниц на сайте: {:.0f}'.format(metrika.get_metrics_count(counter, 'pageviews')))
