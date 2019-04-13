# -*- coding: utf-8  -*-
# @Author: Xingqi Ye
# @Time: 2019-04-06-09


import pandas as pd
import config
from scipy import stats

pd.set_option('expand_frame_repr', False)

# import data
def import_data():
    # import data from path
    df = pd.read_csv(config.input_data_path + '/ClosePriceHSI.csv', parse_dates=['Date'])
    df.sort_values(by=['Date'], inplace=True)

    return df

# transfer to period data
def transfer_to_period_data(df, rule_type=' '):

    '''

    :param df:
    :param rule_type:

    5B  Weekly frequency
    M   Month End frequency

    :return:
    '''

    # set Date as index

    df['period_date'] = df['Date']
    df.set_index('Date', inplace=True)

    # transfer to period data
    period_df = df.resample(rule=rule_type, base=0, label='right', closed='left').last()

    # reset index, put Date as the period end date
    period_df.reset_index(inplace=True)
    period_df['Date'] = period_df['period_date']

    del period_df['period_date']
    df.reset_index(inplace=True, drop=False)

    return period_df

def calculation_p_value(df, x):

    TestList = df[x].tolist()

    k, p = stats.normaltest(TestList)

    return p

