#!/usr/bin/env python
# -*- coding: utf-8 -*-

import osa


def define_unit(input_value):
    """
    Определение единиц измерения
    :param input_value: <str>
    :return: <str>
    """
    temp_units = {
        'mi': 'Miles',
        'km': 'Kilometers',
    }
    for k, v in temp_units.items():
        if k == input_value:
            return v
        elif v == input_value:
            return k


def convert_distance_unit(length, from_unit, to_unit):
    """
    Конвертирование единиц измерения расстояния
    :param length: <int>
    :param from_unit: <str>
    :param to_unit: <str>
    :return: <int>
    """
    url = 'http://www.webservicex.net/length.asmx?WSDL'
    client = osa.client.Client(url)
    response = client.service.ChangeLengthUnit(LengthValue=length, fromLengthUnit=from_unit, toLengthUnit=to_unit)
    return response


def total_distance(path_to_file, target_distance_unit):
    """
    Рассчет общих расходов в определенной валюте
    :param path_to_file: <str>
    :param target_distance_unit: <str>
    :return: None
    """
    with open(path_to_file) as file:
        distance = []
        for line in file:
            if ',' in line.split()[1]:
                number = line.split()[1].replace(',', '')
            else:
                number = line.split()[1]
            distance.append(convert_distance_unit(number, define_unit(line.split()[2]), target_distance_unit))
            print('{0} {1:,.2f} {2}'.format(line.split()[0], distance[-1], define_unit(target_distance_unit)))
        print('\nСуммарное расстояние: {0:,.2f} {1}'.format(sum(distance), define_unit(target_distance_unit)))

total_distance('travel.txt', 'Kilometers')
