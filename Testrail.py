# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 11:40:52 2018

@author: pmarella
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("Testrail_data.csv")
test_without_defect = data.loc[data["TC-Defect"].isnull()]
test_with_defect = data.loc[data["TC-Defect"].notna()]
test_failed = data.loc[data["Status"] == "Failed"]
test_passed = data.loc[data["Status"] == "Passed"]
test_blocked = data.loc[data["Status"] == "Blocked"]

#print(test_blocked)
#print(data["Test-Case"].value_counts())
#print(data["Test-Run"].value_counts())

# pie chart for job
plt.pie(data["Test-Run"].value_counts().values, autopct='%1.2f%%', labels=data["Test-Run"].value_counts().keys())
plt.title("Pie chart of Test-Run")
plt.show()

test_run_status = data.groupby(["Test-Run", "Status"]).size().unstack(fill_value=0)
print(test_run_status)
width=0.4
p1 = plt.bar(test_run_status["Passed"].keys(), test_run_status["Passed"].values)
p2 = plt.bar(test_run_status["Failed"].keys(), test_run_status["Failed"].values, width)
plt.yticks(np.arange(0,300,25))
plt.legend((p1, p2), ("Passed", "Failed"))
plt.show()


test_run_status = test_run_status.loc[test_run_status[""]]
print(test_run_status)
width=0.4
p1 = plt.bar(test_run_status["Passed"].keys(), test_run_status["Passed"].values)
p2 = plt.bar(test_run_status["Failed"].keys(), test_run_status["Failed"].values, width)
plt.yticks(np.arange(0,300,25))
plt.legend((p1, p2), ("Passed", "Failed"))
plt.show()