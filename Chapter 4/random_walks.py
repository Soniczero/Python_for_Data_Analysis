#! /usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Implement a single random walk with 1,000 steps.
'''

#%%
import random
import numpy as np
import pandas as pd
import matplotlib as plt

position = 0
walk = [position]
steps = 1000
for i in range(steps):
    step = 1 if random.randint(0, 1) else -1
    position += step
    walk.append(position)
plot_walk = pd.DataFrame(walk)
plot_walk._set_axis_name('Move per step',axis=0)
plot_walk._set_axis_name('Step',axis=1)
plot_walk.plot(title='Random walk with +1/-1 steps')

nsteps = 1000
draws = np.random.randint(0, 2, size=nsteps)
steps = np.where(draws > 0, 1, -1)
walk = steps.cumsum()
print('Walk min:', walk.min())
print('Walk max:', walk.max())
print('Walk reach 10:', (np.abs(walk) >= 10).argmax())
plot_walk = pd.DataFrame(walk)
plot_walk._set_axis_name('Position',axis=0)
plot_walk._set_axis_name('Step',axis=1)
plot_walk.plot(title='Another Random walk with +1/-1 steps')
# plt.pyplot(range(steps), walk)

# Simulating Many Random Walks at Once-------------------------------------
nwalks = 5000
nsteps = 1000
draws = np.random.randint(0, 2, size=(nwalks, nsteps))
steps = np.where(draws > 0, 1, -1)
walks = steps.cumsum(1)  # cumsum steps's axis=1 to make walk(position)
print('\nMultiple Walks:')
print('Walks min:', walks.min())
print('Walks max:', walks.max())
hits30 = (np.abs(walks) >= 30).any(1)
print('Walks reach 30:', hits30)
print('Hits times:', hits30.sum())
crossing_times = (np.abs(walks[hits30]) >= 30).argmax(1)
print('Crossing times:', crossing_times.mean())