#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Chapter 7 Data Wrangling: Clean, Transform, Merge, Reshape
'''
#%%
import pandas as pd
import numpy as np
import os
import re

# Combining and Merging Data Sets
print('''
Combining and Merging Data Sets
-------------------------------
''')
df1 = pd.DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'a', 'b'],
                    'data': range(7)})
df2 = pd.DataFrame({'key': ['a', 'b', 'd'],
                    'data2': range(3)})
print(df1, '\n')
print(df2, '\n')
print(pd.merge(df1, df2), '\n')
print(pd.merge(df1, df2, on='key'), '\n')

df3 = pd.DataFrame({'lkey': ['b', 'b', 'a', 'c', 'a', 'a', 'b'],
                    'data1': range(7)})
df4 = pd.DataFrame({'rkey': ['a', 'b', 'd'],
                    'data2': range(3)})
print(pd.merge(df3, df4, left_on='lkey', right_on='rkey'), '\n')
print(pd.merge(df1, df2, how='outer'), '\n')

df5 = pd.DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'b'],
                    'data1': range(6)})
df6 = pd.DataFrame({'key': ['a', 'b', 'a', 'b', 'd'],
                    'data2': range(5)})
print(df5, '\n')
print(df6, '\n')
print(pd.merge(df5, df6, on='key', how='left'), '\n')
print(pd.merge(df5, df6, on='key', how='right'), '\n')
print(pd.merge(df5, df6, on='key', how='inner'), '\n')
print(pd.merge(df5, df6, on='key', how='outer'), '\n')

# Merge with multiple keys
df7 = pd.DataFrame({'key1': ['foo', 'foo', 'bar'],
                    'key2': ['one', 'two', 'one'],
                    'lval': [1, 2, 3]})
df8 = pd.DataFrame({'key1': ['foo', 'foo', 'bar', 'bar'],
                    'key2': ['one', 'one', 'one', 'two'],
                    'rval': [4, 5, 6, 7]})
print(pd.merge(df7, df8, on=['key1', 'key2'],how='outer').set_index(['key1', 'key2']), '\n')
print(pd.merge(df7, df8, on='key1', suffixes=('_left', '_right'), how='outer'), '\n')

# Merging on Index
df9 = pd.DataFrame({'key': ['a', 'b', 'a', 'a', 'b', 'c'],
                    'value': range(6)})
df10 = pd.DataFrame({'group_val': [3.5, 7]}, index=['a', 'b'])
print(pd.merge(df9, df10, left_on='key', right_index=True, how='outer'), '\n')

df11 = pd.DataFrame({'key1': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
                     'key2': [2000, 2001, 2002, 2001, 2002],
                     'data': np.arange(5.)})
df12 = pd.DataFrame(np.arange(12).reshape((6, 2)),
                    index=[['Nevada', 'Nevada', 'Ohio', 'Ohio', 'Ohio', 'Ohio'],
                           [2001, 2000, 2000, 2000, 2001, 2002]],
                    columns=['event1', 'event2'])
print(df11, '\n')
print(df12, '\n')
print(pd.merge(df11, df12, left_on=['key1', 'key2'], right_index=True, how='outer'), '\n')

df13 = pd.DataFrame([[1., 2.], [3., 4.], [5., 6.]], index=['a', 'c', 'e'],
                    columns=['Ohio', 'Nevada'])
df14 = pd.DataFrame([[7., 8.], [9., 10.], [11., 12.], [13, 14]],
                    index=['b', 'c', 'd', 'e'], columns=['Missouri', 'Alabama'])
print(pd.merge(df13, df14, left_index=True, right_index=True, how='outer'), '\n')
print(df13.join(df14, how='outer'), '\n')

print(df9.join(df10, on='key'), '\n')

df15 = pd.DataFrame([[7., 8.], [9., 10.], [11., 12.], [16., 17.]],
                    index=['a', 'c', 'e', 'f'], columns=['New York', 'Oregon'])
print(df13.join([df14, df15]), '\n')

# Concatenating Along an Axis
arr = np.arange(12).reshape((3, 4))
print(np.concatenate([arr, arr], axis=1), '\n')

s1 = pd.Series([0, 1], index=['a', 'b'])
s2 = pd.Series([2, 3, 4], index=['c', 'd', 'e'])
s3 = pd.Series([5, 6], index=['f', 'g'])
print('s1:', s1)
print('s2:', s2)
print('s3:', s3)
print(pd.concat([s1, s2, s3]), '\n')
print(pd.concat([s1, s2, s3], axis=1).fillna(0), '\n')

s4 = pd.concat([s1*5, s3])
print(pd.concat([s1, s4], axis=1), '\n')
print(pd.concat([s1, s4], axis=1, join='inner'), '\n')
print(pd.concat([s1, s4], axis=1, join_axes=[['a', 'c', 'b', 'e']]), '\n')

result = pd.concat([s1, s1, s3], keys=['one', 'two', 'three'])
print(result, '\n')
print(result.unstack(), '\n')

# When axis=1, keys become columns head
print(pd.concat([s1, s1, s3], axis=1, keys=['one', 'two', 'three']), '\n')

df16 = pd.DataFrame(np.arange(6).reshape(3, 2), index=['a', 'b', 'c'], 
                    columns=['one', 'two'])
df17 = pd.DataFrame(5 + np.arange(4).reshape(2, 2), index=['a', 'c'], 
                    columns=['three', 'four'])
print(pd.concat([df16, df17], axis=1, keys=['level1', 'level2'],
                names=['upper', 'lower']))

df18 = pd.DataFrame(np.random.randn(3, 4), columns=['a', 'b', 'c', 'd'])
df19 = pd.DataFrame(np.random.randn(2, 3), columns=['b', 'd', 'a'])
print(pd.concat([df18, df19], ignore_index=True), '\n')

# Combining Data with Overlap
a = pd.Series([np.nan, 2.5, np.nan, 3.5, 4.5, np.nan],
            index=['f', 'e', 'd', 'c', 'b', 'a'])
b = pd.Series(np.arange(len(a), dtype=np.float64),
            index=['f', 'e', 'd', 'c', 'b', 'a'])
b[-1] = np.nan
print('a:', a)
print('b:', b)
print(pd.Series(np.where(pd.isnull(a), b, a), 
                index=['f', 'e', 'd', 'c', 'b', 'a']), '\n')
print(b[:-2])
print(a[2:])
print(b[:-2].combine_first(a[2:]), '\n')

df20 = pd.DataFrame({'a': [1., np.nan, 5., np.nan],
                     'b': [np.nan, 2., np.nan, 6.],
                     'c': range(2, 18, 4)})
df21 = pd.DataFrame({'a': [5., 4., np.nan, 3., 7.],
                     'b': [np.nan, 3., 4., 6., 8.]})
print(df20.combine_first(df21), '\n')

# Reshaping and Pivoting
# ----------------------
print('''
Reshaping and Pivoting
----------------------
''')
data = pd.DataFrame(np.arange(6).reshape((2, 3)),
                 index=pd.Index(['Ohio', 'Colorado'], name='state'),
                 columns=pd.Index(['one', 'two', 'three'], name='number'))
print(data, '\n')
result = data.stack()
print(result)
print(result.unstack(), '\n')
print(result.unstack(0))
print(result.unstack('state'), '\n')

s1 = pd.Series([0, 1, 2, 3], index=['a', 'b', 'c', 'd'])
s2 = pd.Series([4, 5, 6], index=['c', 'd', 'e'])
data2 = pd.concat([s1, s2], keys=['one', 'two'])
print(data2)
print(data2.unstack())
print(data2.unstack().stack(dropna=False), '\n')

df22 = pd.DataFrame({'left': result, 'right': result + 5},
                    columns=pd.Index(['left', 'right'], name='side'))
print(df22)
print(df22.unstack('state'))
print(df22.unstack('state').stack('side'), '\n')

# Pivoting “long” to “wide” Format
datafile = open(os.path.join(os.path.dirname(__file__), 
                'data\\macrodata.csv'))
rawdata = pd.read_csv(datafile)
# print(ldata.info())
print(rawdata[:10], '\n')
item = ['realgdp', 'infl', 'unemp']
ldata = rawdata.ix[:9, ['year', 'quarter', 'realgdp', 'infl', 'unemp']]
ldata = ldata.set_index(['year', 'quarter'])
ldata.columns.name = 'item'
print(ldata.info())
tdata = ldata.stack()
print(tdata, '\n')
# print(ldata.pivot('year', 'quarter'))
# pivoted = ldata.pivot('year', 'item', 'value')
# print(pivoted.head())

raw = [['1959-03-31 00:00:00',  'realgdp',  2710.349],
        ['1959-03-31 00:00:00',     'infl',     0.000],
        ['1959-03-31 00:00:00',    'unemp',     5.800],
        ['1959-06-30 00:00:00',  'realgdp',  2778.801],
        ['1959-06-30 00:00:00',     'infl',     2.340],
        ['1959-06-30 00:00:00',    'unemp',     5.100],
        ['1959-09-30 00:00:00',  'realgdp',  2775.488],
        ['1959-09-30 00:00:00',     'infl',     2.740],
        ['1959-09-30 00:00:00',    'unemp',     5.300],
        ['1959-12-31 00:00:00',  'realgdp',  2785.204]]
rldata = pd.DataFrame(raw, columns=['date', 'item', 'value'])
print(rldata, '\n')
pivoted = rldata.pivot('date', 'item', 'value')
print(rldata.pivot('date', 'item'), '\n'+'-'*10)
print(pivoted, '\n')
rldata['value2'] = np.random.randn(len(rldata))
print(rldata, '\n')
pivoted = rldata.pivot('date', 'item')
print(pivoted, '\n')
print(pivoted['value'], '\n')
print(rldata.set_index(['date', 'item']).unstack('item'))

# Data Transformation
# -------------------
print('''
Data Transformation
-------------------
''')
# Removing Duplicates
data = pd.DataFrame({'k1': ['one'] *3 + ['two'] * 4,
                     'k2': [1, 1, 2, 3, 3, 4, 4]})
print(data, '\n')
print(data.duplicated(), '\n')  # return bool values
print(data.drop_duplicates(), '\n')

data['v1'] = range(7)
print(data, '\n')
print(data.drop_duplicates(['k1']), '\n')
print(data.drop_duplicates(['k1', 'k2'], keep='last'), '\n')

# Transforming Data Using a Function or Mapping
data = pd.DataFrame({'food': ['bacon', 'pulled pork', 'bacon', 'Pastrami',
                              'corned beef', 'Bacon', 'pastrami', 'honey ham',
                              'nova lox'],
                     'ounces': [4, 3, 12, 6, 7.5, 8, 3, 5, 6]})
print(data, '\n')

meat_to_animal = {
  'bacon': 'pig',
  'pulled pork': 'pig',
  'pastrami': 'cow',
  'corned beef': 'cow',
  'honey ham': 'pig',
  'nova lox': 'salmon'
}
# for key:value, map key to value.
data['animal'] = data['food'].map(str.lower).map(meat_to_animal)
print(data, '\n')
print(data['food'].map(lambda x: meat_to_animal[x.lower()]), '\n')

# Replacing Values
data = pd.Series([1., -999., 2., -999., -1000., 3.])
print(data.replace(-999, np.nan), '\n')
print(data.replace([-999, -1000], np.nan), '\n')
print(data.replace([-999, -1000], [np.nan, 0]), '\n')
print(data.replace({-999: np.nan, -1000: 0}), '\n')

# Renaming Axis Indexes
data = pd.DataFrame(np.arange(12).reshape((3, 4)),
                    index=['Ohio', 'Colorado', 'New York'],
                    columns=['one', 'two', 'three', 'four'])
data.index = data.index.map(str.upper)
print(data, '\n')
print(data.rename(index=str.title, columns=str.upper), '\n')
print(data.rename(index={'OHIO': 'INDIANA'},
                  columns={'three': 'peekaboo'}), '\n')
_ = data.rename(index={'OHIO': 'INDIANA'}, inplace=True)
# print(_, '\n')
print(data, '\n')

# Discretization and Binning
ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
bins = [18, 25, 35, 60, 100]
cats = pd.cut(ages, bins)
print(cats, '\n')
print('labels in cats:', cats.codes)
print('levels in cats:', cats.categories)
print(pd.value_counts(cats), '\n')
print(pd.cut(ages, [18, 26, 36, 61, 100], right=False), '\n')

# pass bin names
group_names = ['Youth', 'YoungAdult', 'MiddleAged', 'Senior']
print(pd.cut(ages, bins, labels=group_names), '\n')

# cut in equal length
data = np.random.rand(20)
print(pd.cut(data, 4, precision=2), '\n')

# get equal size bins based on sample quantiles
data = np.random.randn(1000) # Normally distributed
cats = pd.qcut(data, 4) # Cut into quartiles
print(cats)
print(pd.value_counts(cats), '\n')

# custom quantiles, number in [0, 1]
cats = pd.qcut(data, [0, 0.1, 0.5, 0.9, 1.])
print(cats)
print(pd.value_counts(cats), '\n')

# Detecting and Filtering Outliers
np.random.seed(12345)
data = pd.DataFrame(np.random.randn(1000, 4))
print(data.describe(), '\n')

col = data[3]
print(col[np.abs(col) > 3], '\n')
print(data[(np.abs(data) > 3).any(1)], '\n' + '-' * 20)
print(data[(np.abs(data) > 3).all(1)], '\n')

# The ufunc np.sign returns an array of 1, 0 and -1 depending
# on the sign of the values.
data[np.abs(data) > 3] = np.sign(data) * 3
print(data.describe(), '\n')

# Permutation and Random Sampling
df = pd.DataFrame(np.arange(5 * 4).reshape(5, 4))
sampler = np.random.permutation(5)
print(sampler, '\n')
print(df, '\n' + '-' * 20)
print(df.take(sampler), '\n')
print(df.reindex(sampler), '\n')

print(df.take(np.random.permutation(len(df))[:3]), '\n')

bag = np.array([5, 7, -1, 6, 4])
sampler = np.random.randint(0, len(bag), size=10)
draws = bag.take(sampler)
print(sampler, '\n')
print(draws, '\n')

# Computing Indicator/Dummy Variables
df = pd.DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'b'],
                   'data1': range(6)})
print(df, '\n')
print(pd.get_dummies(df['key']), '\n')

dummies = pd.get_dummies(df['key'], prefix='key')
df_with_dummy = df[['data1']].join(dummies)
print(df_with_dummy, '\n')
print(df[['data1']].info())

# manually get dummy matrix
mnames = ['movie_id', 'title', 'genres']
m_dat = os.path.join(os.path.dirname(__file__), 'data\\movies.dat')
movies = pd.read_table(m_dat, sep='::', header=None, names=mnames)
print(movies[:10], '\n')
genre_iter = (set(x.split('|')) for x in movies.genres)  # a tuple of which every row is a set
genres = sorted(set.union(*genre_iter))  # expan genre_iter, make a set containing all genres
dummies = pd.DataFrame(np.zeros((len(movies), len(genres))), columns=genres)
for i, gen in enumerate(movies.genres):  # enumerate for loop
    dummies.ix[i, gen.split('|')] = 1
movies_windic = movies.join(dummies.add_prefix('Genre_'))
print(movies_windic.ix[0], '\n')

# combine get_dummies with a discretiza-tion function like cut
values = np.random.rand(10)
bins = [0, 0.2, 0.4, 0.6, 0.8, 1]
print(pd.get_dummies(pd.cut(values, bins)), '\n')

# String Manipulation
# -------------------
print(''' 
String Manipulation
-------------------
''')
# split
val = 'a,b,  guido'
print('split:', val.split(','))

# strip whitespace
pieces = [x.strip() for x in val.split(',')]
print('strip:', pieces)

# concatenate, join
first, second, third = pieces
print('addition:', first + '::' + second + '::' + third)
print('join:', '::'.join(pieces))
 
ex = "'guido' in val"
print(ex + ':', exec(ex))
print('index[\',\']:', val.index(','))
print('find(\':\')', val.find(':'))
ex = "val.count(',')"
print(ex + ':', exec(ex))
ex = "val.replace(',', '::')"
print(ex + ':', exec(ex))
ex = "val.replace(',', '')"
print(ex + ':', exec(ex), '\n')

# Reglular expressions
text = "foo    bar\t baz  \tqux"
print('test:\t', text,
      # the regular expression is first compiled
      '\nregex:\t', re.split('\s+', text))
# re.split('\s+', text) ==> regex.compile('\s').split(text)
regex = re.compile('\s+')
print('equivalent:\t', regex.split(text))
print('regex findall:\t', regex.findall(text))

# match, search, findall
text = """Dave dave@google.com
Steve steve@gmail.com
Rob rob@gmail.com
Ryan ryan@yahoo.com
"""
pattern = r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}'  # pattern in raw string
# re.IGNORECASE makes the regex case-insensitive
regex = re.compile(pattern, flags=re.IGNORECASE)
print(regex.findall(text))
# search returns a pair of positions
m = regex.search(text)
print(m)
print('search:\t', text[m.start():m.end()])
# match only search the pattern that occurs at the start of the string.
print('match:\t', regex.match(text))
# substitute, return new strings that take the replacements.
print('sub:\t', regex.sub('REDACTED', text))

pattern = r'([A-Z0-9._%+-]+)@([A-Z0-9.-]+)\.([A-Z]{2,4})'
regex = re.compile(pattern, flags=re.IGNORECASE)
m = regex.match('wesm@bright.net')
print(m)
# groups() returns the tuple
print(m.groups())
print(regex.findall(text))
# '\1', back-reference pattern, could be used in raplacement argument.
print(regex.sub(r'Username: \1, Domain: \2, Suffix: \3', text))

# use ?p<name> with ?p=name
regex = re.compile(r"""
    (?P<username>[A-Z0-9._%+-]+)
    @
    (?P<domain>[A-Z0-9.-]+)
    \.
    (?P<suffix>[A-Z]{2,4})""", flags=re.IGNORECASE|re.VERBOSE)
m = regex.match('wesm@bright.net')
print(m)
print(m.groups())
print(m.groupdict(), '\n')

# Vectorized string functions in pandas
data = {'Dave': 'dave@google.com', 'Steve': 'steve@gmail.com',
        'Rob': 'rob@gmail.com', 'Wes': np.nan}
data = pd.Series(data)
print(data, '\n')
print(data.isnull(), '\n')
# Series.str attribute used to skip NA valus
print(data.str.contains('gmail'), '\n')
print('pattern:', pattern)
print(data.str.findall(pattern, flags=re.IGNORECASE), '\n')

# matches = data.str.match(pattern, flags=re.IGNORECASE)
matches = data.str.extract(pattern, flags=re.IGNORECASE)
# TODO: The match method return array of booleans, not tuple as expected.
print(matches, '\n' + '-' * 20)
print(matches.get(1), '\n' + '-' * 20)
print(matches[0], '\n')
print(data.str[:5], '\n')