# -*- coding: utf-8  -*-
# @Author: Xingqi Ye
# @Time: 2019-04-06-08


import os

# get current address
current_file = __file__



# get root path
root_path = os.path.abspath(os.path.join(current_file, os.pardir))

# create input data path
input_data_path = os.path.abspath(os.path.join(root_path, 'data', 'input_data'))

# create output data path
output_data_path = os.path.abspath(os.path.join(root_path, 'data', 'output_data'))

