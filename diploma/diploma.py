#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time

import vk
from tqdm import tqdm
import user_info as ui


SESSION = vk.AuthSession(app_id=ui.APP_ID, user_login=ui.USER_LOGIN, user_password=ui.USER_PASSWORD)
API = vk.API(SESSION)


def get_user():
    """
    Получение id пользователя
    :return: <int>
    """
    user = input('Введите имя страницы или id пользователя: ')
    if user.isdigit():
        uid = int(user)
    else:
        uid = API.users.get(user_ids=[user])[0]['uid']
    return uid


def get_followers(user):
    """
    Получение множества, состоящего из id подписчиков
    :return: <set>
    """
    followers = set()
    offset = 0
    followers_count = API.users.getFollowers(user_id=user)['count']
    with tqdm(total=followers_count, desc='Получение подписчиков',
              bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
        for i in range(followers_count):
            response = API.users.getFollowers(user_id=user, count=1000, offset=offset)
            followers.update(set(response['items']))
            offset += 1000
            # Создание задержки из-за ограничения на количество запросов в секунду
            time.sleep(0.34)
            if offset >= followers_count:
                pbar.update(1000 - (offset - followers_count))
                break
            else:
                pbar.update(1000)
    return followers


def sorting_groups(groups):
    """
    Сортировка групп по количеству подписчиков
    :param groups:
    :return: <list>
    """
    return sorted(groups.items(), key=lambda x: x[1], reverse=True)


def get_groups(users):
    """
    Получение списка групп, отсортированного по количеству подписчиков пользователя, состоящих в них
    :param users: <set>
    :return: <list>
    """
    groups = {}
    for user in tqdm(users, desc='Обработка подписчиков',
                     bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'):
        try:
            for item in API.groups.get(user_id=user, extended=1)[1:]:
                groups.setdefault(item['name'], 0)
                groups[item['name']] += 1
        # Обработка исключения, если пользователь удален или забанен
        except vk.exceptions.VkAPIError:
            continue
    return sorting_groups(groups)


def file_write(groups_list):
    """
    Запись топ 100 групп в файл
    :param groups_list: <list>
    :return:
    """
    top_groups = [{'title': i[0], 'count': i[1]} for i in groups_list[:100]]
    print(top_groups)
    with open('top100.json', 'w') as file:
        json.dump(top_groups, file, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    user_id = get_user()

    # Вариант для друзей
    # friends = API.friends.get(user_id=user_id)
    # file_write(get_groups(friends))

    # Вариант для подписчиков (при большом количестве подписчиков работает очень долго)
    file_write(get_groups(get_followers(user_id)))
