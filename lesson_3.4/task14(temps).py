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
        'C': 'degreeCelsius',
        'F': 'degreeFahrenheit',
        'K': 'kelvin',
    }
    for k, v in temp_units.items():
        if k == input_value:
            return v
        elif v == input_value:
            return k


def convert_temp_unit(temp, from_unit, to_unit):
    """
    Конвертирование единиц измерения температуры
    :param temp: <int>
    :param from_unit: <str>
    :param to_unit: <str>
    :return: <int>
    """
    url = 'http://www.webservicex.net/ConvertTemperature.asmx?WSDL'
    client = osa.client.Client(url)
    response = client.service.ConvertTemp(Temperature=temp, FromUnit=from_unit, ToUnit=to_unit)
    return response


def average_temperature(path_to_file, target_temp_unit):
    """
    Рассчет средней температуры в определенных единицах
    :param path_to_file: <str>
    :param target_temp_unit: <str>
    :return: None
    """
    with open(path_to_file) as file:
        temps = []
        for line in file:
            temps.append(convert_temp_unit(line.split()[0], define_unit(line.split()[1]), target_temp_unit))
        print('Cредняя температура за {0} дней: {1:.1f} {2}'.format(len(temps), sum(temps) / len(temps),
                                                                    define_unit(target_temp_unit)))

average_temperature('temps.txt', 'degreeCelsius')
