#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd


def row_count(row):
    row.Count = row.Count + row[-1]
    return row


def count_top3(years_list):
    df = pd.DataFrame()
    for year in years_list:
        file = '/names/yob{}.txt'.format(year)
        names = pd.read_csv(file, names=['Name', 'Gender', 'Count'])
        if df.empty:
            df = df.append(names)
        else:
            df = pd.merge(df, names, on=['Name', 'Gender'], suffixes=['', '_{}'.format(year)]).apply(row_count, axis=1)
            # df = df.ix[:, 0:3]
    return df.sort_values(by='Count', ascending=False).head(3)


count_top3([1940, 1950, 1960, 1970])


def count_dynamics(years_list):
    dynamics = {
        'M': [],
        'F': []
    }
    for year in years_list:
        file = '/names/yob{}.txt'.format(year)
        names = pd.read_csv(file, names=['Name', 'Gender', 'Count'])
        dynamics['M'].append(names[names.Gender == 'M'].Count.sum())
        dynamics['F'].append(names[names.Gender == 'F'].Count.sum())
    return dynamics


count_dynamics([1880, 1920, 1950])
