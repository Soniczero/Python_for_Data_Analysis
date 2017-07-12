#! /usr/bin/env python
# -*- coding: UTF-8 -*-

#%%
import os
import zipfile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __debug__:
    BASE_PATH = 'e:\\workspace\\Python\\Python_for_Data_Analysis\\Chapter 2\\2.3 US Baby Names'
else:
    BASE_PATH = os.path.dirname(__file__)
path = os.path.join(BASE_PATH, 'data\\names.zip')
if not os.path.exists(path):
    print('Error: no such file in the path \"' + path + '\".' )
    exit()
with zipfile.ZipFile(path) as myzip:
    with myzip.open('yob1880.txt') as myfile:
        names1880 = pd.read_csv(myfile, names=['name', 'sex', 'births'])
print('First 10 lines in name\'s data of 1880:')
print(names1880[:10])

print('\nInfo of data:')
print(names1880.info())

print('\nBrouped by sex:')
print(names1880.groupby('sex').births.sum())

years = range(1880, 2011)
pieces = []
columns = ['name', 'sex', 'births']
with zipfile.ZipFile(path) as myzip:
    for year in years:
        file_name = 'yob%d.txt' % year
        frame = pd.read_csv(myzip.open(file_name), names=columns)
        frame['year'] = year
        pieces.append(frame)
# Concatenate everything into a single DataFrame
names = pd.concat(pieces, ignore_index=True)

print('\npieces and names:')
print(pieces[0].info())
print(names.info())

total_births = names.pivot_table('births', index='year', columns='sex', aggfunc=sum)
print('\nTotal births in year:')
print(total_births.tail())
total_births.plot(title='Total births by sex and year')

def add_prop(group):
    births = group.births.astype(float)
    group['prop'] = births / births.sum()
    return group

names = names.groupby(['year', 'sex']).apply(add_prop)
print('\nInfo of grouped names:')
print(names.info())
# Sanity check
if np.allclose(names.groupby(['year', 'sex']).prop.sum(), 1):
    print('Sanity check: pass')
else:
    print('Sanity check: fail')

def get_top1000(group):
    return group.sort_values(by='births', ascending=False)[:1000]
grouped = names.groupby(['year', 'sex'])
top1000 = grouped.apply(get_top1000)
print('\nInfo of Top1000:')
print(top1000.info())

# Another implement
pieces = []
for year, group in names.groupby(['year', 'sex']):
    pieces.append(group.sort_values(by='births', ascending=False)[:1000])
top1000 = pd.concat(pieces, ignore_index=True)
print('\nanother implement:')
print(top1000.info())

# Analyzing Name Trends----------------------------------------------------------
boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']
total_births = top1000.pivot_table('births', index='year', columns='name', aggfunc=sum)
print('\nPivot table of names:')
print(total_births.info())
subset = total_births[['John', 'Harry', 'Mary', "Marilyn"]]
subset.plot(subplots=True, figsize=(12, 10), grid=False, title='Number of births per year')

table = top1000.pivot_table('prop', index='year', columns='sex', aggfunc=sum)
table.plot(title='Sum of table1000.prop by year and sex',
            yticks=np.linspace(0, 1.2, 13), xticks=range(1991, 2020, 10))

df = boys[boys.year == 2010]
print('\nBoys\' names in 2010:')
print(boys.info())

prop_cumsum = df.sort_values(by='prop', ascending=False).prop.cumsum()
print('\nTop 10 proportions:')
print(prop_cumsum[:10])
print(prop_cumsum.searchsorted(0.5))

df = boys[boys.year == 1990]
in1990 = df.sort_values(by='prop', ascending=False).prop.cumsum()
in1990.searchsorted(0.5) + 1

def get_quantile_count(group, q=0.5):
    group = group.sort_values(by='prop', ascending=False)
    return group.prop.cumsum().searchsorted(q) + 1

diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')
print('\nDiversity:')
print(diversity.head())
# TODO: diversity.plot can't be ploted.
# diversity.plot(title='Number of popular names in top 50%')

# The "Last Letter" Revolution--------------------------------------------------------------------------
# extract last letter from name column
get_last_letter = lambda x: x[-1]
last_letters = names.name.map(get_last_letter)
last_letters.name = 'last_letter'
table = names.pivot_table('births', index=last_letters, columns=['sex', 'year'], aggfunc=sum)
subtable = table.reindex(columns=[1910, 1960, 2010], level='year')
print(subtable.head())
print(subtable.sum())

letter_prop = subtable / subtable.sum().astype(float)
fig, axes = plt.subplots(2, 1, figsize=(10, 8))
letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female', legend=False)

letter_prop = table / table.sum().astype(float)
dny_ts = letter_prop.ix[['d', 'n', 'y'], 'M'].T
print('\nd,n,y in boy\' names:')
print(dny_ts.head())
dny_ts.plot()

# Boy names that became girl names (and vice versa)-----------------------------------------------------
all_names = top1000.name.unique()
mask = np.array(['lesl' in x.lower() for x in all_names])  # Filter by prefix 'lesl'
lesley_like = all_names[mask]
print('\nLesley like (e.g. Lesl-) names:')
print(lesley_like)

filtered = top1000[top1000.name.isin(lesley_like)]
print(filtered.groupby('name').births.sum())

table = filtered.pivot_table('births', index='year', columns='sex', aggfunc=sum)
table = table.div(table.sum(1), axis=0)
print(table.tail())
table.plot(style={'M': 'k-', 'F': 'k--'})