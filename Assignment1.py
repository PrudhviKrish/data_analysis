import pandas as pd

data = pd.read_csv("Assignment_1.csv")

# Mean salary
print("Mean salary of employees {}".format(data["salary"].mean()))

# Converting job into category
data["jobs"] = data["job"].astype("category")

print("\nJob details")
print(data.jobs.value_counts())

# Married employees whose salary greater than 60000
married_employees = data[data["marital"].isin(["married"])]
print("\nDetails of married employees with salary >60000")
print(married_employees[married_employees.salary > 60000].sort_values(by="salary"))

# Dataset of single employees
print("\nDetails of employees with marital status single")
print(data[data['marital'] == 'single'])

def missing_values():
    """
    To find columns which contain missing values
    """
    missing_data = pd.isna(data)
    return missing_data[missing_data == True].columns

def emp_count(status, salary):
    """
    Find out the number of employees with given marital status and salary
    
    :params status: marital status
    :params salary: salary range
    """
    employees = data[data["marital"].isin([status])]
    return len(employees[employees.salary == salary])

# Cloumns with empty values
print("\nColumns with empty values")
print("\n"+missing_values())

# Check employee count
print("\nNumber of employees with marital status as 'single' and salary range 60000 is {}".format(emp_count(status="single", salary=60000)))