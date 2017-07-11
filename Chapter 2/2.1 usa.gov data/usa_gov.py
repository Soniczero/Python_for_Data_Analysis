#! /usr/bin/env python
# -*- coding: UTF-8 -*-

#%%
import json
import os
from collections import defaultdict
from collections import Counter

# path of the data file.
BASE_PATH = os.path.dirname(__file__)
path = os.path.join(BASE_PATH, 'data\\usagov_bitly_data2012-03-16-1331923249.txt')
if not os.path.exists(path):
    print('Error: no such file found in \"' + path + '\".')
    exit()
# assert os.path.exists(path), 'Error: no such file found in \"' + path + '\".'

print('The first data in the opened file:')
print(open(path).readline())  # print one line
records = [json.loads(line) for line in open(path)]  # records is a list of dicts

# Section 1------------------------------------------------------------------------
# Counting Time Zones in Pure Python
time_zones = [rec['tz'] for rec in records if 'tz' in rec]
print('\n\nFirst 10 time zones:')
print(time_zones[:10])  # print top 10 time zones

def get_counts(sequence):
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts

def get_counts2(sequence):
    counts = defaultdict(int)  # values will initialize to 0
    for x in sequence:
        counts[x] +=1
    return counts

counts = get_counts(time_zones)
print('\nCount in America/New_York:', counts['America/New_York'])
print('Total times zones:', len(time_zones))

def top_counts(count_dict, n=10):
    value_key_pairs = [(count, tz) for tz, count in count_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-n:]

print('\n\nTop 10 time zones:')
print(top_counts(counts))  # print top 10 time zones in decending order of counts

counts = Counter(time_zones)  # another implement by collections.Counter
print('\nAnother implement Top 10 time zones:')
print(counts.most_common(10))

# Section 2------------------------------------------------------------------------
# Counting Time Zones with pandas
from pandas import DataFrame, Series
import pandas as pd

frame = DataFrame(records)
print('\n\nFirst 10 records in DataFrame:')
print(frame[:10])
print('\n\nFirst 10 time zones in DataFrame:')
print(frame['tz'][:10])  # frame[column][row]

print('\nFirst 10 counts:')
tz_counts = frame['tz'].value_counts()
print(tz_counts[:10])

#%%
clean_tz = frame['tz'].fillna('Missing')  # Fill missing(NA) values
clean_tz[clean_tz == ''] = 'Unknown'  # Replace unknown valules
tz_counts = clean_tz.value_counts()
print('\nTop 10 counts(filled):')
print(tz_counts[:10])
tz_counts[:10].plot(kind='barh', rot=0)  # plot horizontal bar

results = Series([x.split()[0] for x in frame.a.dropna()])  # a is 'a' in short of application
print('\n\nFirst 5 softwares in records:')
print(results[:5])

print('\n\nTop 8 used softwares:')
print(results.value_counts()[:8])

cframe = frame[frame.a.notnull()]  # filter in 'a' column
print('\nClean null value', len(frame), '->', len(cframe))
operating_system = pd.np.where(cframe['a'].str.contains('Windows'),
                            'Windows', 'Not Windows')
print('\n\nFirst 5 OS in records:')
print(operating_system[:5])

by_tz_os = cframe.groupby(['tz', operating_system])
agg_counts = by_tz_os.size().unstack().fillna(0)
print('\n\nFirst 10 agg_counts:')
print(agg_counts[:10])
print('\nFirst 10 agg_counts stacked:')
print(by_tz_os.size()[:10])

indexer = agg_counts.sum(1).argsort()
print('\n\nFirst 10 address:')
print(indexer[:10])

# Use take to select rows in indexer's order, slice last 10 rows
count_subset = agg_counts.take(indexer)[-10:]
print('\n\nLast 10 address:')
print(count_subset[:10])
count_subset.plot(kind='barh', stacked=True)
normed_subset = count_subset.div(count_subset.sum(1), axis=0)
normed_subset.plot(kind='barh', stacked=True)