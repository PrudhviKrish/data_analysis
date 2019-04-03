# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 14:58:09 2018

@author: pmarella
"""

import pandas as pd
import matplotlib.pyplot as plt

def parser(x):
	return pd.datetime.strptime('190'+x, '%Y-%m')

data = pd.read_excel("sales.xls", header=12, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
print(data.head())