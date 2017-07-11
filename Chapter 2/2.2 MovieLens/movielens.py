#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import pandas as pd
import os

BASE_DIR = os.path.dirname(__file__)
print(BASE_DIR)
path = os.path.join(BASE_DIR, 'data\\ml-1m')
if not os.path.exists(path):
    print('Error: no such path exists \"' + path + '\".')
    exit()

if not os.path.exists(os.path.join(path, 'ratings.dat')):
    print('Error: no such path exists \"' + path + '\".')
    exit()

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table(os.path.join(path,'users.dat'), sep='::', header=None, names=unames)

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table(os.path.join(path,'ratings.dat'), sep='::', header=None, names=rnames)

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table(os.path.join(path,'movies.dat'), sep='::', header=None, names=mnames)

print('First 5 in Users:')
print(users[:5])
print('\nFirst 5 in Ratings:')
print(ratings[:5])
print('\nFirst 5 in Movies:')
print(movies[:5])

data = pd.merge(pd.merge(ratings, users), movies)
print('\nData merged:')
print(data.info())

# pivot table
mean_ratings = data.pivot_table('rating', index='title', columns='gender', aggfunc='mean')
print('\nFirst 5 mean ratings:')
print(mean_ratings[:5])

ratings_by_title = data.groupby('title').size()
print('\nFirst 10 ratings in title:')
print(ratings_by_title[:10])

active_titles = ratings_by_title.index[ratings_by_title >= 250]
print('\nRatings >= 250:')
print(active_titles)

mean_ratings = mean_ratings.ix[active_titles]
print('\nTitiles with ratings >= 250:')
print(mean_ratings.info())

top_female_ratings = mean_ratings.sort_index(by='F', ascending=False)
print('\nTop 10 female ratings:')
print(top_female_ratings[:10])

#%%
# Measuring rating disagreement---------------------------------------------------
mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
sorted_by_diff = mean_ratings.sort_values(by='diff')
print('\nTop 15 ratings sorted in diff:')
print(sorted_by_diff[:15])

# Reverse order of rows, thake first 15 rows
print('\nLast 15 reversed:')
print(sorted_by_diff[::-1][:15])

# Standard deviation of rating grouped by title
rating_std_by_title = data.groupby('title')['rating'].std()
# Filter down to active_title
rating_std_by_title = rating_std_by_title.ix[active_titles]
print('\nTop 15 titiles(ratings=>250) filtered by std deviation:')
print(rating_std_by_title.sort_values(ascending=False)[:10])
