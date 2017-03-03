#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from urllib.parse import urlencode, urlparse


AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.60'
APP_ID = 5900188

auth_data = {
    'client_id': APP_ID,
    'display': 'mobile',
    'response_type': 'token',
    'scope': 'friends,status',
    'v': VERSION,
}

print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))

token_url = 'https://oauth.vk.com/blank.html#access_token=\
85ae82f265d00198d0994316ae78d37f7b36d7e487186377e1339ad8d7fbbd44a88b097c1beb6adbd1705&expires_in=86400&user_id=14931358'

o = urlparse(token_url)
fragments = dict((i.split('=')) for i in o.fragment.split('&'))
access_token = fragments['access_token']


def get_friends(user_id):
    """
    Получение списка друзей
    :param user_id:
    :return:
    """
    friends_list = []
    params = {
        'access_token': access_token,
        'v': VERSION,
        'user_id': user_id,
        'fields': 'first_name,last_name'
    }
    response = requests.get('https://api.vk.com/method/friends.get', params=params)
    for item in response.json()['response']['items']:
        if 'deactivated' in item:
            continue
        else:
            friends_list.append(item)
    return friends_list


def common_friends(user_id):
    """
    Общие друзья
    :param user_id:
    :return:
    """
    friends_list = []
    params = {
        'access_token': access_token,
        'v': VERSION,
        'target_uid': user_id,
    }
    response = requests.get('https://api.vk.com/method/friends.getMutual', params=params)
    for item in response.json()['response']:
        response = requests.get('https://api.vk.com/method/users.get', params={'user_id': item})
        if 'deactivated' in response.json()['response'][0]:
            continue
        else:
            friends_list.append(response.json()['response'][0])
    return friends_list


def print_friend(friend):
    """
    Вывод имени и фамилии
    :param friend:
    :return:
    """
    line = '{0} {1}'.format(friend['first_name'], friend['last_name'])
    return line


for my_friend in get_friends(None):
    print('-' * len(print_friend(my_friend)))
    print(print_friend(my_friend))
    print('-' * len(print_friend(my_friend)))
    for other_friend in get_friends(my_friend['id']):
        print('\t', print_friend(other_friend))
    if not common_friends(my_friend['id']):
        print('\n\t\tОбщих друзей нет\n')
    else:
        print('\n\t\tОбщие друзья: {0}\n'.format(list(print_friend(f) for f in common_friends(my_friend['id']))))
