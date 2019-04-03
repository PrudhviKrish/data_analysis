# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 14:46:18 2018

@author: pmarella
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

bug_data = pd.read_excel("JIRA_Defect.xlsx", "SourceData")
bug_data.dropna(axis=1, how="all", inplace=True)
bug_data = bug_data[bug_data["Project key"].isin(["OMNI", "NGIO"])]

commit_data = pd.read_excel("CommitData.xlsx")


bug_data_omni = bug_data[bug_data["Project key"] == "OMNI"]
plt.pie(bug_data_omni["Component/s"].value_counts().values, autopct='%1.2f%%', labels=bug_data_omni["Component/s"].value_counts().keys())
plt.title("Pie chart of affected components in OMNI")
plt.savefig("ComponentOmni", loc=1)
plt.show()

bug_data_ngio = bug_data[bug_data["Project key"] == "NGIO"]
plt.pie(bug_data_ngio["Component/s"].value_counts().values, autopct='%1.2f%%', labels=bug_data_ngio["Component/s"].value_counts().keys())
plt.title("Pie chart of affected components in NGIO")
plt.savefig("ComponentNgio")
plt.show()

def group_pie(df):
    pie_counts = df.groupby(["Component/s"]).agg('count')
    pct_value = pie_counts[lambda df: df.columns[0]].quantile(.70)
    values_below_pct_value = pie_counts[lambda df: df.columns[0]].loc[lambda s: s < pct_value].index.values
    def fix_values(row):
        if row["Component/s"] in values_below_pct_value:
            row["Component/s"] = 'Other'
        return row 
    pie_grouped = df.apply(fix_values, axis=1).groupby("Component/s").agg('count')
    return pie_grouped

bug_data_omni_others = group_pie(bug_data_omni)
plt.pie(bug_data_omni_others["Summary"], autopct='%1.2f%%', labels=bug_data_omni_others["Summary"].index)
plt.title("Pie chart of affected components in OMNI")
plt.gcf().set_size_inches(10, 5)
plt.savefig("ComponentOmni1", loc=1)
plt.show()

bug_data_ngio_others = group_pie(bug_data_ngio)
plt.pie(bug_data_ngio_others["Summary"], autopct='%1.2f%%', labels=bug_data_ngio_others["Summary"].index)
plt.title("Pie chart of affected components in NGIO")
plt.gcf().set_size_inches(10, 5)
plt.savefig("ComponentNgio1")
plt.show()

likelihood = bug_data[bug_data["Custom field (Likelihood of Occurrence)"] != "Unknown"]
likelihood = likelihood.groupby(["Custom field (Likelihood of Occurrence)", "Component/s"]).size().unstack(fill_value=0)
index=np.arange(len(likelihood["Data Path - FileSystem"].keys()))
width = 0.1
p1 = plt.bar(index, likelihood["Data Path - FileSystem"].values, width, color="red")
p2 = plt.bar(index+width, likelihood["DP"].values, width, color="yellowgreen")
p3 = plt.bar(index+2*width, likelihood["DP - Volume manager"].values, width, color="blue")
plt.xlabel("components")
plt.ylabel("Likelihood")
plt.title("Likelihood VS Components")
plt.xticks(index+2*width/3 , likelihood["Data Path - FileSystem"].keys(), rotation=45)
plt.legend((p1, p2, p3), ("Data Path - FileSystem", "DP", "DP - Volume manager"))
plt.savefig("Likelihood")
plt.show()

for columns in bug_data.columns:
    
#    elif "Affects Version/s." in columns:
#        bug_data["Affects Version/s"] = bug_data["Affects Version/s"] + ", " + bug_data[columns].map(str)
#        bug_data.drop(columns, axis=1, inplace=True)
    
    if "Comment." in columns:
        bug_data["Comment"] = np.where(bug_data[columns].isnull(), bug_data["Comment"], bug_data["Comment"] + ", " + bug_data[columns].map(str))
        bug_data.drop(columns, axis=1, inplace=True)
    
#    elif "Component/s." in columns:
#        bug_data["Component/s"] = bug_data["Component/s"] + ", " + bug_data[columns].map(str)
#        bug_data.drop(columns, axis=1, inplace=True)
    
    elif "Log Work." in columns:
        bug_data["Log Work"] = bug_data["Log Work"] + ", " + bug_data[columns].map(str)
        bug_data.drop(columns, axis=1, inplace=True)
    
    elif "Attachment." in columns:
        bug_data["Attachment"] = bug_data["Attachment"] + ", " + bug_data[columns].map(str)
        bug_data.drop(columns, axis=1, inplace=True)
    
    elif "Outward issue link (Relates)." in columns:
        bug_data["Outward issue link (Relates)"] = bug_data["Outward issue link (Relates)"] + ", " + bug_data[columns].map(str)
        bug_data.drop(columns, axis=1, inplace=True)
    
    elif "Outward issue link (Duplicate)." in columns:
        bug_data["Outward issue link (Duplicate)"] = bug_data["Outward issue link (Duplicate)"] + ", " + bug_data[columns].map(str)
        bug_data.drop(columns, axis=1, inplace=True)
    
    elif "Outward issue link (Blocks)." in columns:
        bug_data["Outward issue link (Blocks)"] = bug_data["Outward issue link (Blocks)"] + ", " + bug_data[columns].map(str)
        bug_data.drop(columns, axis=1, inplace=True)
    
    elif "Outward issue link (Dependency)." in columns:
        bug_data["Outward issue link (Dependency)"] = bug_data["Outward issue link (Dependency)"] + ", " + bug_data[columns].map(str)
        bug_data.drop(columns, axis=1, inplace=True)
    
    elif "Outward issue link (Root Cause ID)." in columns:
        bug_data["Outward issue link (Root Cause ID)"] = bug_data["Outward issue link (Root Cause ID)"] + ", " + bug_data[columns].map(str)
        bug_data.drop(columns, axis=1, inplace=True)


plt.pie(bug_data["Priority"].value_counts().values, autopct='%1.2f%%', labels=bug_data["Priority"].value_counts().values)
plt.title("Pie chart of Priority")
plt.legend(bug_data["Priority"].value_counts().keys())
plt.savefig("Priority")
plt.show()

column_list = ["Summary", "Issue key", "Issue id", "Issue Type", "Status", "Project name",
               "Priority", "Resolution", "Created", "Resolved", "Affects Version/s", 
               "Fix Version/s", "Component/s", "Comment"]

bug_data = bug_data[column_list]
commit_data = commit_data[["commitId", "filesAffected", "key"]]
commit_data.rename(columns={"key": "Issue key"}, inplace=True)

final_data = pd.merge(bug_data, commit_data, on="Issue key", how="outer")

final_data["filesWithPath"] = final_data["filesAffected"].str.findall(r'[a-zA-Z]+\/[a-zA-Z_\-.]+\/.*?\.\w+')
file_details = final_data[["Issue key", "Priority", "Affects Version/s", "Component/s", "filesWithPath"]]
file_details.dropna(inplace=True)

rows = []
_ = file_details.apply(lambda row: [rows.append([row['Issue key'], row['Priority'], row["Affects Version/s"], row["Component/s"], nn]) for nn in row["filesWithPath"]], axis=1)
df = pd.DataFrame(rows, columns=file_details.columns)
df["file"] = df["filesWithPath"].str.extract('(\w+\.\w+)', expand=False)
df = df[df["Priority"] != "Low"]


job_data = df.groupby(["filesWithPath", "Priority"]).size().unstack(fill_value=0)
data_value_ge_1 = job_data.drop(job_data[(job_data["Critical"].isin([0,1,2,3])) & (job_data["High"].isin([0,1,2,3])) & (job_data["Medium"].isin([0,1,2,3]))].index)

totals = [i+j+k for i,j,k in zip(job_data['Critical'], job_data['High'], job_data['Medium'])]
CriticalBars = [i / j * 100 for i,j in zip(job_data['Critical'], totals)]
HighBars = [i / j * 100 for i,j in zip(job_data['High'], totals)]
MediumBars = [i / j * 100 for i,j in zip(job_data['Medium'], totals)]
width = 0.8
p1 = plt.bar(job_data["Critical"].keys(), CriticalBars, color='r', edgecolor='white', width=width)
p2 = plt.bar(job_data["High"].keys(), HighBars, bottom=CriticalBars, color='y', edgecolor='white', width=width)
p3 = plt.bar(job_data["Medium"].keys(), MediumBars, bottom=[i+j for i,j in zip(CriticalBars, HighBars)], color='g', edgecolor='white', width=width)
plt.grid(axis="y")
plt.xlabel("Files")
plt.ylabel("No. of bugs")
plt.title("File VS Priority")
plt.xticks(rotation=90)
plt.legend((p1, p2, p3), ("Critical", "High", "Medium"))
plt.gcf().set_size_inches(20, 9)
plt.gcf().savefig("File&PriorityPercent", bbox_inches='tight', dpi=300)
plt.show()


p1 = plt.bar(job_data["Critical"].keys(), job_data["Critical"].values, width, color="red")
p2 = plt.bar(job_data["High"].keys(), job_data["High"].values, width, bottom=job_data["Critical"].values, color="yellow")
p3 = plt.bar(job_data["Medium"].keys(), job_data["Medium"].values, width, bottom=job_data["Critical"].values+job_data["High"].values, color="green")
plt.grid(axis="y")
plt.xlabel("Files")
plt.ylabel("No. of bugs")
plt.title("File VS Priority")
plt.xticks(rotation=90)
# plt.yticks(np.arange(1,30,4))
plt.legend((p1, p2, p3), ("Critical", "High", "Medium"))
plt.gcf().set_size_inches(20, 9)
plt.gcf().savefig("File&Priority", bbox_inches='tight', dpi=300)
plt.show()


totals = [i+j+k for i,j,k in zip(data_value_ge_1['Critical'], data_value_ge_1['High'], data_value_ge_1['Medium'])]
CriticalBars = [i / j * 100 for i,j in zip(data_value_ge_1['Critical'], totals)]
HighBars = [i / j * 100 for i,j in zip(data_value_ge_1['High'], totals)]
MediumBars = [i / j * 100 for i,j in zip(data_value_ge_1['Medium'], totals)]
width = 0.4
p1 = plt.bar(data_value_ge_1["Critical"].keys(), CriticalBars, color='r', edgecolor='white', width=width)
p2 = plt.bar(data_value_ge_1["High"].keys(), HighBars, bottom=CriticalBars, color='y', edgecolor='white', width=width)
p3 = plt.bar(data_value_ge_1["Medium"].keys(), MediumBars, bottom=[i+j for i,j in zip(CriticalBars, HighBars)], color='g', edgecolor='white', width=width)
plt.grid(axis="y")
plt.xlabel("Files")
plt.ylabel("No. of bugs")
plt.title("File VS Priority for repetitive files")
plt.xticks(rotation=90)
plt.legend((p1, p2, p3), ("Critical", "High", "Medium"))
plt.gcf().set_size_inches(20, 9)
plt.gcf().savefig("File&PriorityPercent_ge_1", bbox_inches='tight', dpi=300)
plt.show()


p1 = plt.bar(data_value_ge_1["Critical"].keys(), data_value_ge_1["Critical"].values, width, color="red")
p2 = plt.bar(data_value_ge_1["High"].keys(), data_value_ge_1["High"].values, width, bottom=data_value_ge_1["Critical"].values, color="yellow")
p3 = plt.bar(data_value_ge_1["Medium"].keys(), data_value_ge_1["Medium"].values, width, bottom=data_value_ge_1["Critical"].values+data_value_ge_1["High"].values, color="green")
plt.grid(axis="y")
plt.xlabel("Files")
plt.ylabel("No. of bugs")
plt.title("File VS Priority for repetitive files")
plt.xticks(rotation=90)
plt.legend((p1, p2, p3), ("Critical", "High", "Medium"))
plt.gcf().set_size_inches(20, 9)
plt.gcf().savefig("File&Priority_ge_1", bbox_inches='tight', dpi=300)
plt.show()

dfc = df[df["Priority"] == "Critical"]

job_data = dfc.groupby(["filesWithPath", "Priority"]).size().unstack(fill_value=0)
width = 0.8
plt.bar(job_data["Critical"].keys(), job_data["Critical"].values, width, color="red")
plt.grid(axis="y")
plt.xlabel("Files")
plt.ylabel("No. of bugs")
plt.title("File VS Critical Priority")
plt.xticks(rotation=90)
# plt.yticks(np.arange(1,30,4))
plt.gcf().set_size_inches(20, 9)
plt.gcf().savefig("File&CriticalPriority", bbox_inches='tight', dpi=300)
plt.show()

dfh = df[df["Priority"] == "High"]

job_data = dfh.groupby(["filesWithPath", "Priority"]).size().unstack(fill_value=0)
width = 0.8
plt.bar(job_data["High"].keys(), job_data["High"].values, width, color="yellow")
plt.grid(axis="y")
plt.xlabel("Files")
plt.ylabel("No. of bugs")
plt.title("File VS High Priority")
plt.xticks(rotation=90)
# plt.yticks(np.arange(1,30,4))
plt.gcf().set_size_inches(20, 9)
plt.gcf().savefig("File&HighPriority", bbox_inches='tight', dpi=300)
plt.show()

dfm = df[df["Priority"] == "Medium"]
job_data = dfm.groupby(["filesWithPath", "Priority"]).size().unstack(fill_value=0)
width = 0.8
plt.bar(job_data["Medium"].keys(), job_data["Medium"].values, width, color="green")
plt.grid(axis="y")
plt.xlabel("Files")
plt.ylabel("No. of bugs")
plt.title("File VS Medium Priority")
plt.xticks(rotation=90)
# plt.yticks(np.arange(1,30,4))
plt.gcf().set_size_inches(20, 9)
plt.gcf().savefig("File&MediumPriority", bbox_inches='tight', dpi=300)
plt.show()

dfc = df[df["Priority"] == "Critical"]

job_data = dfc.groupby(["filesWithPath", "Priority"]).size().unstack(fill_value=0)
data_value_ge_1 = job_data.drop(job_data[(job_data["Critical"].isin([0,1,2,3]))].index)
width = 0.4
plt.bar(data_value_ge_1["Critical"].keys(), data_value_ge_1["Critical"].values, width, color="red")
plt.grid(axis="y")
plt.xlabel("Files")
plt.ylabel("No. of bugs")
plt.title("File VS Critical Priority for repetitive files")
plt.xticks(rotation=90)
# plt.yticks(np.arange(1,30,4))
plt.gcf().set_size_inches(20, 9)
plt.gcf().savefig("File&CriticalPriority_ge_1", bbox_inches='tight', dpi=300)
plt.show()

dfh = df[df["Priority"] == "High"]

job_data = dfh.groupby(["filesWithPath", "Priority"]).size().unstack(fill_value=0)
data_value_ge_1 = job_data.drop(job_data[(job_data["High"].isin([0,1,2,3]))].index)
width = 0.4
plt.bar(data_value_ge_1["High"].keys(), data_value_ge_1["High"].values, width, color="y")
plt.grid(axis="y")
plt.xlabel("Files")
plt.ylabel("No. of bugs")
plt.title("File VS High Priority for repetitive files")
plt.xticks(rotation=90)
# plt.yticks(np.arange(1,30,4))
plt.gcf().set_size_inches(20, 9)
plt.gcf().savefig("File&HighPriority_ge_1", bbox_inches='tight', dpi=300)
plt.show()

dfm = df[df["Priority"] == "Medium"]
job_data = dfm.groupby(["filesWithPath", "Priority"]).size().unstack(fill_value=0)
data_value_ge_1 = job_data.drop(job_data[(job_data["Medium"].isin([0,1,2,3]))].index)
width = 0.4
plt.bar(data_value_ge_1["Medium"].keys(), data_value_ge_1["Medium"].values, width, color="green")
plt.grid(axis="y")
plt.xlabel("Files")
plt.ylabel("No. of bugs")
plt.title("File VS Medium Priority for repetitive files")
plt.xticks(rotation=90)
# plt.yticks(np.arange(1,30,4))
plt.gcf().set_size_inches(20, 9)
plt.gcf().savefig("File&MediumPriority_ge_1", bbox_inches='tight', dpi=300)
plt.show()

df["count"] = pd.Series([1 for x in range(len(df.index))], index=df.index)
pivot_table = pd.pivot_table(df, index=["filesWithPath"], columns=["Affects Version/s"], values=["count"])
sns.heatmap(pivot_table, annot=True, fmt="g", cmap='viridis')
plt.savefig("heatmap")
plt.show()

df_fs = df[df["Component/s"] == "Data Path - FileSystem"]

job_data = df_fs.groupby(["filesWithPath", "Priority"]).size().unstack(fill_value=0)
data_value_ge_2 = job_data.drop(job_data[(job_data["Critical"].isin([0,1,2,3])) & (job_data["High"].isin([0,1,2,3])) & (job_data["Medium"].isin([0,1,2,3]))].index)


totals = [i+j+k for i,j,k in zip(job_data['Critical'], job_data['High'], job_data['Medium'])]
CriticalBars = [i / j * 100 for i,j in zip(job_data['Critical'], totals)]
HighBars = [i / j * 100 for i,j in zip(job_data['High'], totals)]
MediumBars = [i / j * 100 for i,j in zip(job_data['Medium'], totals)]
width = 0.8
p1 = plt.bar(job_data["Critical"].keys(), CriticalBars, color='r', edgecolor='white', width=width)
p2 = plt.bar(job_data["High"].keys(), HighBars, bottom=CriticalBars, color='y', edgecolor='white', width=width)
p3 = plt.bar(job_data["Medium"].keys(), MediumBars, bottom=[i+j for i,j in zip(CriticalBars, HighBars)], color='g', edgecolor='white', width=width)
plt.grid(axis="y")
plt.xlabel("Files")
plt.ylabel("No. of bugs")
plt.title("File VS Priority")
plt.xticks(rotation=90)
plt.legend((p1, p2, p3), ("Critical", "High", "Medium"))
plt.gcf().set_size_inches(20, 9)
plt.gcf().savefig("File&PriorityPercent for Data Path - FileSystem", bbox_inches='tight', dpi=300)
plt.show()

p1 = plt.bar(job_data["Critical"].keys(), job_data["Critical"].values, width, color="red")
p2 = plt.bar(job_data["High"].keys(), job_data["High"].values, width, bottom=job_data["Critical"].values, color="yellowgreen")
p3 = plt.bar(job_data["Medium"].keys(), job_data["Medium"].values, width, bottom=job_data["Critical"].values+job_data["High"].values, color="green")
plt.grid(axis="y")
plt.xlabel("Files")
plt.ylabel("No. of bugs")
plt.title("File VS Priority")
plt.xticks(rotation=90)
plt.legend((p1, p2, p3), ("Critical", "High", "Medium"))
plt.gcf().set_size_inches(20, 9)
plt.gcf().savefig("File&Priority for Data Path - FileSystem", bbox_inches='tight', dpi=300)
plt.show()

totals = [i+j+k for i,j,k in zip(data_value_ge_2['Critical'], data_value_ge_2['High'], data_value_ge_2['Medium'])]
CriticalBars = [i / j * 100 for i,j in zip(data_value_ge_2['Critical'], totals)]
HighBars = [i / j * 100 for i,j in zip(data_value_ge_2['High'], totals)]
MediumBars = [i / j * 100 for i,j in zip(data_value_ge_2['Medium'], totals)]
width = 0.4
p1 = plt.bar(data_value_ge_2["Critical"].keys(), CriticalBars, color='r', edgecolor='white', width=width)
p2 = plt.bar(data_value_ge_2["High"].keys(), HighBars, bottom=CriticalBars, color='y', edgecolor='white', width=width)
p3 = plt.bar(data_value_ge_2["Medium"].keys(), MediumBars, bottom=[i+j for i,j in zip(CriticalBars, HighBars)], color='g', edgecolor='white', width=width)
plt.grid(axis="y")
plt.xlabel("Files")
plt.ylabel("No. of bugs")
plt.title("File VS Priority for repetitive files")
plt.xticks(rotation=90)
plt.legend((p1, p2, p3), ("Critical", "High", "Medium"))
plt.gcf().set_size_inches(20, 9)
plt.gcf().savefig("File&PriorityPercent_ge_2 for Data Path - FileSystem", bbox_inches='tight', dpi=300)
plt.show()

p1 = plt.bar(data_value_ge_2["Critical"].keys(), data_value_ge_2["Critical"].values, width, color="red")
p2 = plt.bar(data_value_ge_2["High"].keys(), data_value_ge_2["High"].values, width, bottom=data_value_ge_2["Critical"].values, color="yellowgreen")
p3 = plt.bar(data_value_ge_2["Medium"].keys(), data_value_ge_2["Medium"].values, width, bottom=data_value_ge_2["Critical"].values+data_value_ge_2["High"].values, color="green")
plt.grid(axis="y")
plt.xlabel("Files")
plt.ylabel("No. of bugs")
plt.title("File VS Priority for repetitive files")
plt.xticks(rotation=90)
plt.legend((p1, p2, p3), ("Critical", "High", "Medium"))
plt.gcf().set_size_inches(20, 9)
plt.gcf().savefig("File&Priority_ge_2 for Data Path - FileSystem", bbox_inches='tight', dpi=300)
plt.show()

#print(df_fs["filesWithPath"].value_counts())
#
#status_data = bug_data.groupby(["Status", "Priority", "Resolution"]).size().unstack(fill_value=0)
#print(status_data)
#
#print(bug_data["Component/s"].value_counts())
#
#print(bug_data["Fix Version/s"].value_counts())
#
#print(commit_data["fixVersion"].value_counts())
