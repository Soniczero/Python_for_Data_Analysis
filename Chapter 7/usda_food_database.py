#! /usr/bin/env pathon3
''' 
Chapter 7
Example: USDA Food Database
'''
#%%
import json
import os
import pandas as pd

try:
    data_file = os.path.dirname(__file__)
    print('debug:')
except:
    print('jupyter:')
    __file__ = r'e:\\workspace\\Python\\Python_for_Data_Analysis\\Chapter 7\\usda_food_database.py'
data_file = os.path.join(os.path.dirname(__file__),
                         'data\\foods-2011-10-03.json')
print(__file__)
print(os.path.dirname(__file__))
db = json.load(open(data_file))  # list of dict
js_db = pd.read_json(data_file)  # DataFrame

print(type(db), ':')
print(len(db))
print(db[0].keys())
print(db[0]['nutrients'][0], '\n')

print(type(js_db), ':')
# print(js_db.info())
print(js_db.ix[0, 'nutrients'][0], '\n')

# nutrients is a MxN matrix.
nutrients = pd.DataFrame(db[0]['nutrients'])
print(nutrients[:7], '\n')
info_keys = ['description', 'group', 'id', 'manufacturer']
columns = nutrients.columns  # equavilent to info_keys
# print(columns)
info = pd.DataFrame(db, columns=info_keys)
print(info.head(), '\n')
print(info.info(), '\n')
print(pd.value_counts(info.group)[:10], '\n')

nutrients = []

for rec in db:
    fnuts = pd.DataFrame(rec['nutrients'])
    fnuts['id'] = rec['id']
    nutrients.append(fnuts)

print('nutrients 3D matrix:')
# nutrients is a list
print(nutrients[0][:10], '\n')
# shift nutrients to DataFrame
nutrients = pd.concat(nutrients, ignore_index=True)
print('\nnutrients.info:', nutrients.info())
print('duplicate:', nutrients.duplicated().sum())
nutrients = nutrients.drop_duplicates()
print('clean:', nutrients.info(), '\n')

col_mapping = {'description': 'food',
               'group': 'fgroup'}
# info = DataFrame(db)
info = info.rename(columns=col_mapping, copy=False)
print(info.info(), '\n')

col_mapping = {'description': 'nutrient',
               'group': 'nutgroup'}
nutrients = nutrients.rename(columns=col_mapping, copy=False)
print(nutrients.info(), '\n')

ndata = pd.merge(nutrients, info, on='id', how='outer')
print(ndata.info(), '\n')
print('ndata.ix[30000]:\n', ndata.iloc[30000], sep='')

# groupby() makes indexes ['nutrient', 'fgroup'], then calulate the 
# midpoint, quantile(0.5), of 'value' column.
result = ndata.groupby(['nutrient', 'fgroup'])['value'].quantile(0.5)
result['Zinc, Zn'].sort_values().plot(kind='barh')

by_nutrient = ndata.groupby(['nutgroup', 'nutrient'])
# xs() method, cross-section, slice the by_nutrient matrix
get_maximum = lambda x: x.xs(x.value.idxmax())
get_minimum = lambda x: x.xs(x.value.idxmin())

max_foods = by_nutrient.apply(get_maximum)[['value', 'food']]
min_foods = by_nutrient.apply(get_minimum)[['value', 'food']]
# cut food name string little short for displaying
max_foods.food = max_foods.food.str[:50]
min_foods.food = min_foods.food.str[:50]
print('The foods of which the nutrient is the max:')
print(max_foods.ix['Amino Acids']['food'], '\n')
print('The foods of which the nutrient is the min:')
print(min_foods.ix['Amino Acids']['food'])