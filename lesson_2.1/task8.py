#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv


money_amount = 10000
schengen_countries = set()
sea_countries = set()
warm_countries = set()
cheap_countries = set()


with open('countries.csv') as csv_file:
    country_reader = csv.DictReader(csv_file, delimiter=';')
    for row in country_reader:
        if row['Schengen'] == 'True':
            schengen_countries.add(row['CountryName'])
        if row['Sea'] == 'True':
            sea_countries.add(row['CountryName'])
        if int(row['AverageTemperature']) > 20:
            warm_countries.add(row['CountryName'])
        if ((money_amount / float(row['CurrencyRate'])) - (int(row['RentPerDay']) * 30)) > 0:
            cheap_countries.add(row['CountryName'])

# print(schengen_countries)
# print(sea_countries)
# print(warm_countries)
# print(cheap_countries)

warm_sea_cheap_countries = warm_countries & sea_countries & cheap_countries
schengen_cheap_countries = schengen_countries & cheap_countries

print('Теплые страны с морем, в которых мы можем прожить месяц:', warm_sea_cheap_countries)
print('Страны Шенгеского договора, в которых мы можем прожить месяц:', schengen_cheap_countries)
