# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 09:59:54 2018

@author: pmarella
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Loading data
data = pd.read_excel("Assignment_2.xlsx")

# deleting unwanted row and duplicate rows
data = data.drop(data.index[len(data)-1])
data = data.drop_duplicates()
data=data.replace(0, np.NaN) # since tenure cannot be 0 replacing with NaN

# cleaning MonthlyCharges and TotalCharges values
data.MonthlyCharges = pd.to_numeric(data.MonthlyCharges.str.replace("$", ""))
data.MonthlyCharges = data.MonthlyCharges.fillna(data.MonthlyCharges.mean())
data.TotalCharges = pd.to_numeric(data.TotalCharges.str.replace("$", ""), errors='coerce')
data.TotalCharges = data.TotalCharges.fillna(data.TotalCharges.mean())

# filling the missing values and cleaning the data
data.tenure = data.tenure.fillna(data.tenure.mean())
data.Churn = data.Churn.fillna("No")
data.PhoneService = data.PhoneService.fillna("Yes")
data.PaperlessBilling = data.PaperlessBilling.fillna("Yes")
data.Contract = data.Contract.fillna("month to month")
data.Contract = data.Contract.str.lower().str.replace("-", " ")

# Scatter plot for Monthly and total charges
plt.scatter(data["MonthlyCharges"], data["TotalCharges"], color="red", alpha=0.5)
plt.xlabel("Customer's Monthly Charge")
plt.ylabel("Customer's Total Charge")
plt.title("Monthly charges VS Total charges")
plt.show()
print("\nCorrelation between monthly and total charges is {}".format(data["MonthlyCharges"].corr(data["TotalCharges"])))

# cleaning payment method
data.PaymentMethod = data.PaymentMethod.fillna('Electronic Check')
data.PaymentMethod = data.PaymentMethod.str.replace('^Bank trans$|^bank transfer $|Bank transfer (automatic)', 'Bank transfer (automatic)', case=False)
data.PaymentMethod = data.PaymentMethod.str.replace('^credit card$|^Credit card $|Credit card (automatic)', 'Credit card (automatic)', case=False)
data.PaymentMethod = data.PaymentMethod.str.replace('^Electronic$|^Electronic check$', 'Electronic Check', case=False)

# bar chart for payment method
plt.bar(data["PaymentMethod"].value_counts().keys(), data["PaymentMethod"].value_counts().values, align='center')
plt.xlabel("Payment method")
plt.title("Payment method bar chart")
plt.show()

# Histogram for tenure
plt.hist(data["tenure"])
plt.ylabel("Frequency")
plt.xlabel("Tenure")
plt.title("Frequency of Tenure")
plt.grid(True)
plt.show()

# Contract VS Churn
contract_churn_no = data.loc[data["Churn"] == "No"]["Contract"].value_counts()
contract_churn_yes = data.loc[data["Churn"] == "Yes"]["Contract"].value_counts()
plt.plot(contract_churn_no.keys(), contract_churn_no.values, label="No")
plt.plot(contract_churn_no.keys(), contract_churn_yes.values, label="Yes")
plt.ylabel("Churn")
plt.xlabel("\nContract")
plt.title("Churn VS Contract")
plt.legend()
plt.show()

# Contract VS Churn VS Payment Method
index=np.arange(len(contract_churn_no.keys()))
width = 0.25
plt.subplot(2,1,1)
plt.bar(index, contract_churn_no.values, width, color="red", label="No")
plt.bar(index+width, contract_churn_yes.values, width, color="green", label="Yes")
plt.ylabel("Churn")
plt.xlabel("\nContract")
plt.title("Churn VS Contract")
plt.xticks(index+width/2 , contract_churn_no.keys())
plt.yticks(np.arange(0, 2500, 250))
plt.legend()
plt.subplot(2,1,2)
payment_churn_no = data.loc[data["Churn"] == "No"]["PaymentMethod"].value_counts()
payment_churn_yes = data.loc[data["Churn"] == "Yes"]["PaymentMethod"].value_counts()
index=np.arange(len(payment_churn_no.keys()))
plt.bar(index, payment_churn_no.values, width, color="red", label="No")
plt.bar(index+width, payment_churn_yes.values, width, color="green", label="Yes")
plt.ylabel("Churn")
plt.xlabel("\nPayment Method")
plt.title("\nChurn VS Payment Method")
plt.xticks(index+width/2 , payment_churn_no.keys())
plt.yticks(np.arange(0, 2500, 250))
plt.legend()
plt.tight_layout()
plt.show()

# Pie chart of Churning
plt.pie(data["Churn"].value_counts().values, autopct='%1.2f%%', labels=data["Churn"].value_counts().keys())
plt.title("Pie chart of Churning")
plt.legend()
plt.show()

# Phone Service vs churn
service_churn_no = data.loc[data["Churn"] == "No"]["PhoneService"].value_counts()
service_churn_yes = data.loc[data["Churn"] == "Yes"]["PhoneService"].value_counts()
plt.plot(service_churn_no.keys(), service_churn_no.values, label="No")
plt.plot(service_churn_no.keys(), service_churn_yes.values, label="Yes")
plt.ylabel("Churn")
plt.xlabel("Phone Service")
plt.title("Churn VS Phone Service")
plt.legend()
plt.show()