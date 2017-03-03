#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os.path


RESIDENCE_LIMIT = 90
SCHENGEN_CONSTRAINT = 180
visits = []


def file_reading(visits_list):
    """
    Чтение визитов из файла
    :param visits_list:
    :return:
    """
    with open('visits.txt') as visits_file:
        for line in visits_file:
            visit = []
            for item in line.strip().split(','):
                item = int(item)
                visit.append(item)
            visits_list.append(visit)


def file_record(visits_list):
    """
    Запись визитов в файл
    :param visits_list:
    :return:
    """
    with open('visits.txt', 'w') as visits_file:
        for visit in visits_list:
            line = []
            for date in visit:
                date = str(date)
                line.append(date)
            visits_file.write('{0}\n'.format(', '.join(line)))


def date_difference(leave, arrive):
    """
    Разница дат
    :param leave:
    :param arrive:
    :return:
    """
    result = leave - arrive + 1
    return result


def visit_length(visit):
    """
    Длина визита
    :param visit:
    :return:
    """
    return date_difference(visit[1], visit[0])


def get_days_for_visits(visits_list):
    """
    Рассчет дней для визитов
    :param visits_list:
    :return:
    """
    days_for_visits = []
    for visit in visits_list:
        days_for_visit = 0
        for past_visit in visits_list:
            if visit[0] - SCHENGEN_CONSTRAINT < past_visit[0] < visit[0]:
                days_for_visit += visit_length(past_visit)
        days_for_visit += visit_length(visit)
        days_for_visits.append(days_for_visit)
    return days_for_visits


def print_days_future_visit(visits_list, date_in_future):
    """
    Рассчет дней для будущего визита
    :param visits_list:
    :param date_in_future:
    :return:
    """
    visits_for_future = visits_list + [[date_in_future, date_in_future]]
    days_for_future_visits = get_days_for_visits(visits_for_future)
    days_in_es = RESIDENCE_LIMIT - days_for_future_visits[len(days_for_future_visits) - 1] + 1
    print('Если въедем {0} числа, сможем провести в EC {1} дней'.format(date_in_future, days_in_es))


def dates_order_check(visits_list):
    """
    Проверка порядок вводимых дат
    :param visits_list:
    :return:
    """
    for visit in visits_list:
        if visit[0] > visit[1]:
            print('Дата выезда раньше даты въезда:', visit)
            return True


def overlapping_visits_check(visits_list):
    """
    Проверка на накладывающиеся визиты
    :param visits_list:
    :return:
    """
    for visit in visits_list:
        for past_visit in visits_list:
            if past_visit != visit and past_visit[0] <= visit[0] <= past_visit[1]:
                print('Накладывающиеся визиты:', past_visit, visit)
                return True


def overstay_time_check(visits_list):
    """
    Проверка на превышение лимита
    :param visits_list:
    :return:
    """
    days_for_visits = get_days_for_visits(visits_list)
    for visit, total_days in zip(visits_list, days_for_visits):
        if total_days > RESIDENCE_LIMIT:
            overstay_time = total_days - RESIDENCE_LIMIT
            print('Во время визита {0} время пребывания в ЕС превышено на {1} дней'.format(visit, overstay_time))
            return True


def visits_check(visits_list):
    """
    Проверка визитов
    :param visits_list:
    :return:
    """
    if dates_order_check(visits_list) or overlapping_visits_check(visits_list) or overstay_time_check(visits_list):
        visits_list.remove(visits[-1])


def int_check():
    """
    Являются ли вводимые данные числом
    :return:
    """
    while True:
        user_input = input()
        if user_input and user_input.isdigit():
            user_input = int(user_input)
            break
        else:
            print('Нужно ввести число. Попробуйте снова.')
            continue
    return user_input


def visit_make(dates_list):
    """
    Создание поездки из даты въезда и даты выезда
    :param dates_list:
    :return:
    """
    print('Дата въезда:')
    dates_list.append(int_check())
    print('Дата выезда:')
    dates_list.append(int_check())


def add_visit(visits_list):
    """
    Добавление визита
    :param visits_list:
    :return:
    """
    visit = []
    visit_make(visit)
    if len(visits_list) >= 1 and visits_list[-1] >= visit:
        print('Даты следующего визита раньше или совпадают с датами предыдущего визита:', visits_list[-1], visit)
    elif len(visits_list) >= 1 and visit[0] - visits_list[0][0] >= SCHENGEN_CONSTRAINT:
        print('К поездке {0} срок действия визы истечет. Выберите другие даты.'.format(visit))
    elif len(visits_list) >= 1 and visit[1] - visits_list[0][0] >= SCHENGEN_CONSTRAINT:
        print('Во время поездки {0} срок действия визы истечет. Выберите другие даты.'.format(visit))
    else:
        visits_list.append(visit)


def remove_visit(visits_list):
    """
    Удаление визита
    :param visits_list:
    :return:
    """
    while True:
        visit = []
        visit_make(visit)
        if visit not in visits_list:
            print('Такой поездки не существует. Попробуйте снова.')
            continue
        else:
            visits_list.remove(visit)
            break


def predict_visit(visits_list):
    """
    Проверка будущего визита
    :param visits_list:
    :return:
    """
    future_visit_entry = int(input('Дата въезда будущего визита:\n'))
    if future_visit_entry > visits_list[-1][1]:
        print_days_future_visit(visits_list, future_visit_entry)
    else:
        print('Дата въезда будущего визита не может быть раньше даты выезда предыдущего')


def exit_program(visits_list):
    """
    Выход из программы
    :param visits_list:
    :return:
    """
    file_record(visits_list)
    print('Список визитов:', visits)
    sys.exit()

# Список комманд
commands = {
    'v': add_visit,
    'r': remove_visit,
    'p': predict_visit,
    'e': exit_program
}

# Проверка на существование файла с визитами
if os.path.exists('visits.txt'):
    file_reading(visits)
else:
    pass

print('Список команд:\n'
      'v - добавить визит\n'
      'r - удалить визит\n'
      'p - указать дату будущего визита\n'
      'e - выход')

while True:
    command_choice = input('Что вы хотите сделать?\n')
    func = commands.get(command_choice)
    if func is None:
        print('Пожалуйста, используйте команды из списка!')
        continue
    else:
        func(visits)
        visits_check(visits)
        file_record(visits)
        print('Текущий список визитов:', visits)
