# -*- coding: utf-8  -*-
# @Author: Xingqi Ye
# @Time: 2019-04-07-18


import Functions
import pandas as pd
import config
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox

pd.set_option('expand_frame_repr', False)


daily_data = Functions.import_data()

code_list = daily_data.columns
code_list = code_list.drop('Date')

monthly_data = Functions.transfer_to_period_data(daily_data, 'M')
weekly_data = Functions.transfer_to_period_data(daily_data, '5B')


# calculate the daily, weekly, monthly return
daily_return_data = daily_data.copy()
weekly_return_data = weekly_data.copy()
monthly_return_data = monthly_data.copy()

for x in code_list:

   daily_return_data[x] = daily_return_data[x].pct_change(1)
   weekly_return_data[x] = weekly_return_data[x].pct_change(1)
   monthly_return_data[x] = monthly_return_data[x].pct_change(1)

# Calculate the covariance matrix
covariance_matrix = weekly_data.cov()
covariance_matrix.to_csv(config.output_data_path + '/covHSI.csv', mode='a')

# Plot histogram for 700 HK
Tencent_return = list()
Tencent_return = daily_return_data['700 HK'].tolist()
Tencent_return = Tencent_return[1:]
num_bins = 100

fig, ax = plt.subplots()
n, bins, patches = ax.hist(Tencent_return, num_bins, density=1)

ax.set_xticks(np.arange(-0.1, 0.1, 0.02))
ax.set_yticks(np.arange(0, 88, 8))
plt.title('700 HK')
plt.savefig(config.output_data_path + '/700_HK', formate="PNG")
plt.show()


# normal test
p_value = list(map(lambda x : stats.normaltest(weekly_return_data[x][1:]).pvalue, code_list))
# print(p_value)

fig, ax1 = plt.subplots()
ax1.scatter(code_list, p_value, c='r', alpha=0.5)
ax1.tick_params(labelsize=5, labelrotation=45)

ax2 = ax1.twinx()
ax2.axhline(y=0.05)

plt.savefig(config.output_data_path + '/normal_test', format="PNG")
plt.show()


# Auto-correlation test
'''
Test

# p_value_auto_corr = acorr_ljungbox(weekly_return_data['101 HK'][1:], lags=5)
# print(p_value_auto_corr)

Using Map function, return 5 array including the p-value of all the stocks on each lag value from 1 to 5

plot in different colors

'''

p_value_auto_corr = zip(*map(lambda x: acorr_ljungbox(weekly_return_data[x][1:],lags=5)[1], code_list))
p_value_auto_corr_list = list(p_value_auto_corr)
# print(p_value_auto_corr_list)

for i in range(len(p_value_auto_corr_list)):
   fig, ax1 = plt.subplots()
   ax1.scatter(code_list, p_value_auto_corr_list[i], marker='o', label='lags='+str(i+1))
   ax1.tick_params(labelsize=5, labelrotation=45)
   ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

   ax2 = ax1.twinx()
   ax2.axhline(y=0.05)

   plt.savefig(config.output_data_path + '/auto_correlation_test_lag_ %s' %(i+1))
   plt.show()


# Daily Return Calculation
daily_return_data['DateTime'] = daily_return_data['Date'].dt.year * 100 + daily_return_data['Date'].dt.month
print(daily_return_data.groupby('DateTime').std())

