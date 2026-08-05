#import libraries
import pandas as pd
import numpy as np

#bring in file
customers=pd.read_csv('customers.csv')

#print first few rows
print(customers.head())

#convert signup date to datetime
customers['signup_date'] = pd.to_datetime(customers['signup_date'], errors='coerce')

#convert string value to number string, convert to float
customers['spend'] = customers['spend'].replace('Three hundred', '300')
customers['spend'] = (
    customers['spend']
    .replace('[$,]', '', regex=True)   # remove dollar signs/commas
    .astype(float)
)

customers.dtypes

#handle missing values
customers['email'] = customers['email'].fillna('unknown')
customers['age'] = customers['age'].fillna(customers['age'].median())
customers['spend'] = customers['spend'].fillna(0)
customers['signup_date'] = customers['signup_date'].fillna(pd.to_datetime('2020-01-01'))

#standardize text data
customers['country'] = customers['country'].str.upper().replace({'USA': 'US', 'CANADA': 'CA', 'UNITED KINGDOM': 'UK'})
customers['email'] = customers['email'].str.lower()
customers['country'].unique()

customers.head()

#drop dupes
customers = customers.drop_duplicates()

#final look at data
customers.describe()

print(customers)
