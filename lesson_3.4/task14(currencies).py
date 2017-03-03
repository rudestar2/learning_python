#!/usr/bin/env python
# -*- coding: utf-8 -*-

import osa


def convert_currency(amount, from_currency, to_currency):
    """
    Конвертирование валюты
    :param amount: <int>
    :param from_currency: <str>
    :param to_currency: <str>
    :return: <int>
    """
    url = 'http://fx.currencysystem.com/webservices/CurrencyServer4.asmx?WSDL'
    client = osa.client.Client(url)
    response = client.service.ConvertToNum(amount=amount, fromCurrency=from_currency,
                                           toCurrency=to_currency, rounding=True)
    return response


def total_costs(path_to_file, target_currency):
    """
    Рассчет общих расходов в определенной валюте
    :param path_to_file: <str>
    :param target_currency: <str>
    :return: None
    """
    with open(path_to_file) as file:
        prices = []
        for line in file:
            prices.append(round(convert_currency(line.split()[1], line.split()[2], target_currency)))
            print(line.split()[0], prices[-1], target_currency)
        print('\nОбщие расходы на путешествие: {0} {1}'.format(sum(prices), target_currency))

total_costs('currencies.txt', 'RUB')
