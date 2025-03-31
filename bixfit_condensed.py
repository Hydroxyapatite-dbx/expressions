import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import csv
import pandas as pd

def biexpfunc(x, a, b, c, d, e):
    return a * np.exp(-x / b) + c * np.exp(-x / d) + e

# One .csv with an arbitrary number of columns, of which even indices correspond to time steps, and odd indices correspond to intensity steps.
# It begins with a transposition of the input file, necessarily formatted like so:
#
#                                                                           .csv file:
#      time step (scan 1):     |     abs (scan 1):   | ... ... ... ... | ... ... ... ... | ... ... ... ... | ... ... ... ... |   time step (scan N)  |    abs (scan N)   |
#   (row zero of file)  t_01   |         abs_01      |        ...      |    ...          |       ...       |      ...        |          t_0N         |       abs_0N      |
#              t_11            |         abs_11      |        ...      |       ...       |     ...         |      ...        |          t_1N         |       ...         |
#              t_21            |          ...                                                                                |          ...          |                   
#              ...
#
#
# where, for instance, 't_01' denotes the zeroth timestep of the first scan, and '|' fills in for the comma.
#
# To execute the code, simply copy-paste the .csv data file pathname into the first line here, and customize the name of the new transposed file to be created. The code then
# acts on the transposed file to generate a biexponential fit involving a computation and averaging of biexponential time constants across scans.

with open('/Users/matthewsalinas/Downloads/bix_7.csv', 'r', encoding='utf-8-sig') as csvDataFile_3: #Copy-paste your data file pathname in place of /Users...csv.
    csvReader3 = csv.reader(csvDataFile_3)
    csv3 = list(csvReader3)
    tpos_csv3 = list(zip(*csv3))
with open('/Users/matthewsalinas/Downloads/bix_8.csv', 'w', encoding='utf-8-sig', newline='') as csvDataFile_3out: #Copy-paste your new file pathname in place of /Users...csv.
    csv_writer = csv.writer(csvDataFile_3out)
    csv_writer.writerows(tpos_csv3)

df = pd.read_csv('/Users/matthewsalinas/Downloads/bix_8.csv', header=None) #Copy-paste your new file pathname in place of /Users...csv.
t = df.iloc[lambda x: x.index % 2 == 0]
ri = df.iloc[lambda x: x.index % 2 != 0]
tmat = []
rimat = []

for j in range(len(t)):
    x = t.iloc[j]
    t_j = x.to_list()
    print('timearray_'+str(j) , '=' , t_j)
    tmat.append(t_j)
for k in range(len(ri)):
    y = ri.iloc[k]
    ri_k = y.to_list()
    print('absarray_'+str(k) , '=' , ri_k)
    rimat.append(ri_k)

tc1set = []
tc2set = []
c1set = []
c2set = []
c0set = []
for n in range(len(ri)):
    poptn, pcovn = curve_fit(biexpfunc, list(map(float, tmat[n])), list(map(float, rimat[n])))
    tc1set.append(poptn[1])
    tc2set.append(poptn[3])
    c1set.append(poptn[0])
    c2set.append(poptn[2])
    c0set.append(poptn[4])

tc1_array = np.array(tc1set)
tc2_array = np.array(tc2set)
c1_array = np.array(c1set)
c2_array = np.array(c2set)
c0_array = np.array(c0set)

print('set of first time constant values =', tc1_array)
print('set of second time constant values =', tc2_array)
print('set of first coefficient values =', c1_array)
print('set of second coefficient values =', c2_array)
print('set of offset values =', c0_array)

def filter(data, m=1):
    return data[abs(data - np.mean(data)) < m * np.std(data)]
tc1array_c = filter(tc1_array, m=1)
tc2array_c = filter(tc2_array, m=1)
c1array_c = filter(c1_array, m=1)
c2array_c = filter(c2_array, m=1)
c0array_c = filter(c0_array, m=1)

print('set of first time constant values (outliers removed)=', tc1array_c)
print('set of second time constant values (outliers removed)=', tc2array_c)
print('set of first coefficient values (outliers removed)=', c1array_c)
print('set of second coefficient values (outliers removed)=', c2array_c)
print('set of offset values (outliers removed)=', c0array_c)

tc1_avg = np.mean(tc1_array)
tc2_avg = np.mean(tc2_array)

tc1_c_avg = np.mean(tc1array_c)
tc2_c_avg = np.mean(tc2array_c)
c1_c_avg = np.mean(c1array_c)
c2_c_avg = np.mean(c2array_c)
c0_c_avg = np.mean(c0array_c)

print('(tc1_avg, tc2_avg) =', tc1_avg, tc2_avg)
print('Set of averages of "clean" sets [time_const_1, time_const_2, coeff_1, coeff_2, offset] =', [float(tc1_c_avg), float(tc2_c_avg), float(c1_c_avg), float(c2_c_avg), float(c0_c_avg)])