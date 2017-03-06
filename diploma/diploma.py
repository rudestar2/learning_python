#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time

import vk
import user_info as ui


session = vk.AuthSession(app_id=ui.APP_ID, user_login=ui.USER_LOGIN, user_password=ui.USER_PASSWORD)
api = vk.API(session)


def get_user():
    """
    Получение id пользователя
    :return: <int>
    """
    user = input('Введите имя страницы или id пользователя: ')
    if user.isdigit():
        uid = int(user)
    else:
        uid = api.users.get(user_ids=[user])[0]['uid']
    return uid


def get_followers(user_id):
    """
    Получение списка подписчиков
    :return: <list>
    """
    followers = []
    offset = 0
    while True:
        response = api.users.getFollowers(user_id=user_id, count=1000, offset=offset)
        followers.extend(response['items'])
        offset += 1000
        print('Получено подписчиков:', len(followers))
        # Создание задержки из-за ограничения на количество запросов в секунду
        time.sleep(0.34)
        if offset >= response['count']:
            break
    return followers


def sorting_groups(groups):
    """
    Сортировка групп по количеству подписчиков
    :param groups:
    :return: <list>
    """
    return sorted(groups.items(), key=lambda x: x[1], reverse=True)


def get_groups(users_list):
    """
    Получение списка групп, отсортированного по количеству друзей пользователя, состоящих в них
    :param users_list: <list>
    :return: <dict>
    """
    groups = {}
    user_count = 1
    for user in users_list:
        try:
            for item in api.groups.get(user_id=user, extended=1)[1:]:
                if item['name'] in groups.keys():
                    groups[item['name']] += 1
                else:
                    groups[item['name']] = 1
        # Обработка исключения, если пользователь удален или забанен
        except vk.exceptions.VkAPIError:
            print('Обработанно пользователей:', user_count)
            user_count += 1
            continue
        print('Обработанно пользователей:', user_count)
        user_count += 1
    return sorting_groups(groups)


def file_write(groups_list):
    """
    Запись топ 100 групп в файл
    :param groups_list: <list>
    :return:
    """
    top_groups = [{'title': i[0], 'count': i[1]} for i in groups_list[0:100]]
    print(top_groups)
    with open('top100.json', 'w') as file:
        json.dump(top_groups, file, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    user_id = get_user()

    # Вариант для друзей
    friends = api.friends.get(user_id=user_id)
    file_write(get_groups(friends))

    # Вариант для подписчиков (при большом количестве подписчиков работает очень долго)
    # file_write(get_groups(get_followers(user_id)))
