# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 10:16:10 2018

@author: pmarella
"""

import pandas as pd
import numpy as np

data = pd.read_excel("Assignment_2.xlsx")

# deleting unwanted row and duplicate rows
data = data.drop(data.index[len(data)-1])
data = data.drop_duplicates()
data=data.replace(0, np.NaN) # since tenure cannot be 0 replacing with NaN

# Printing missing values
print("Missing values by column wise \n")
print(data.isnull().sum())

# cleaning MonthlyCharges and TotalCharges values
data.MonthlyCharges = pd.to_numeric(data.MonthlyCharges.str.replace("$", ""))
data.TotalCharges = pd.to_numeric(data.TotalCharges.str.replace("$", ""), errors='coerce')
if data.MonthlyCharges.max() - data.MonthlyCharges.quantile(0.75) > data.MonthlyCharges.quantile(0.75) - data.MonthlyCharges.mean():
    print("MonthlyCharges contains Outliers")
else:
    print("MonthlyCharges don't contain Outliers")

if data.TotalCharges.max() - data.TotalCharges.quantile(0.75) > data.TotalCharges.quantile(0.75) - data.TotalCharges.mean():
    print("TotalCharges contains Outliers")
else:
    print("TotalCharges don't contain Outliers")

def total_charges_range(x):
    if x["TotalCharges"] > data.TotalCharges.quantile(0.75):
        return "Very High"
    elif data.TotalCharges.quantile(0.75) < x["TotalCharges"] < data.TotalCharges.mean():
        return "High"
    elif data.TotalCharges.mean() < x["TotalCharges"] < data.TotalCharges.quantile(0.25):
        return "Medium"
    else:
        return "Low"

# Adding Column according to TotalCharges =
data["TotalChargesRange"] = data.apply(lambda x: total_charges_range(x), axis=1)

# spliting customer information into number and code
data["CustomerNumber"], data["CustomerCode"] = data["customerID"].str.split("-").str