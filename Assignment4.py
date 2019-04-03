# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 11:07:23 2018

@author: pmarella
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("Assignment_1.csv")
data.salary.fillna(data.salary.mean(), inplace=True)
data.job = data.job.str.replace(".", "")


# Bar plot for Education with marital status and salary
pvt_table = data.pivot_table(values=["salary"], index=["education"], columns=["marital"])
pvt_table.plot.bar(grid=True)
plt.xlabel("Education with marital status")
plt.ylabel("Salary")
plt.title("Salary VS Education with marital status (Fig 1)")
plt.legend()
plt.show()

# stacked bar plot for Education and Job
job_data = data.groupby(["job", "education"]).size().unstack(fill_value=0)
print(job_data)
width = 0.4
p1 = plt.bar(job_data["primary"].keys(), job_data["primary"].values, width, color="red")
p2 = plt.bar(job_data["secondary"].keys(), job_data["secondary"].values, width, bottom=job_data["primary"].values, color="yellowgreen")
p3 = plt.bar(job_data["tertiary"].keys(), job_data["tertiary"].values, width, bottom=job_data["primary"].values+job_data["secondary"].values, color="green")
plt.xlabel("Job")
plt.ylabel("No. of employee")
plt.title("Job VS Education (Fig 2)")
plt.xticks(rotation=45)
plt.yticks(np.arange(0,22,2))
plt.legend((p1, p2, p3), ("Primary", "Secondary", "Tertiary"))
plt.show()

# Adding age range
def age_range(x):
    if x["age"] >= 60:
        return "60's"
    elif 60 > x["age"] >= 50:
        return "50's"
    elif 50 > x["age"] >= 40:
        return "40's"
    elif 40 > x["age"] >= 30:
        return "30's"
    else:
        return "20's"

data["age_range"] = data.apply(lambda x: age_range(x), axis=1)

# Line plot between age range and job
job_admin = data.loc[data["job"] == "admin"]["age_range"].value_counts().sort_index()
job_technician = data.loc[data["job"] == "technician"]["age_range"].value_counts().sort_index()
job_blue = data.loc[data["job"] == "blue-collar"]["age_range"].value_counts().sort_index()
job_entrepreneur = data.loc[data["job"] == "entrepreneur"]["age_range"].value_counts().sort_index()
job_management = data.loc[data["job"] == "management"]["age_range"].value_counts().sort_index()
job_retired = data.loc[data["job"] == "retired"]["age_range"].value_counts().sort_index()
job_self = data.loc[data["job"] == "self-employed"]["age_range"].value_counts().sort_index()
job_services = data.loc[data["job"] == "services"]["age_range"].value_counts().sort_index()
plt.plot(job_admin.keys(), job_admin.values, label="admin")
plt.plot(job_technician.keys(), job_technician.values, label="technician")
plt.plot(job_blue.keys(), job_blue.values, label="blue-collar")
plt.plot(job_entrepreneur.keys(), job_entrepreneur.values, label="entrepreneur")
plt.plot(job_management.keys(), job_management.values, label="management")
plt.plot(job_retired.keys(), job_retired.values, label="retired")
plt.ylabel("No of employees")
plt.xlabel("Age range")
plt.title("Jobs VS age (Fig3)")
plt.legend()
plt.show()

# Bar plot for Job and salary using seaborn
sns.barplot(x="job", y="salary", hue="marital", data=data)
plt.xticks(rotation=45)
plt.title("Jobs and salaries (Fig4)")
plt.show()


# pie chart for job
plt.pie(data["job"].value_counts().values, autopct='%1.2f%%', labels=data["job"].value_counts().keys())
plt.title("Pie chart of Job (Fig 5)")
plt.show()

# Scatter plot between salary and age
plt.scatter(data["salary"], data["age"], color="red", alpha=0.5)
plt.xlabel("salary")
plt.ylabel("age")
plt.title("Salary VS Age (Fig 6)")
plt.legend()
plt.show()

# Bar plot for salary and target
target = data.groupby(["salary", "targeted"]).size()
target.unstack(fill_value=0).plot.bar()
plt.xlabel("salary")
plt.ylabel("targeted")
plt.title("Salary VS Targeted (Fig 7)")
plt.show()

# box plot between salary and job
data.boxplot(column="salary", by="job", rot=30, figsize=(10,13))
plt.show()

# box plot between balance and marital status
data.boxplot(column="balance", by="marital")
plt.title("Balance VS marital (Fig 8)")
plt.show()

# correlation between numerical columns
print("Correlation between numberical columns")
print(data.corr())

# inference
print("\n*********************SUMMARY********************")
print("\nInferences drawn from visualizition\n")
print("1. Form fig1, Employees with tertiary - divorced and single are getting high salary")
print("2. From fig2, Technicians are having secondary education only")
print("3. From fig3, No people's age is greater than 50 in technician, entrepreneur, and management")
print("4. From fig4, Entrepreneurs are grabing more avg salary whereas blue-collars are getting less salary ")
print("5. From fig5, Organization is having almost same count for technician, management and blue-collar")
print("6. From fig6, 100000 salary is in all the age groups")
print("7. From fig7, 60000 salary group is having more targeted")
print("8. From fig8, Married employees are having more outliers in balance")