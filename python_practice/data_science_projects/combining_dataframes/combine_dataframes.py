#importing pandas and bringing in visits and checkouts csvs
import pandas as pd

visits = pd.read_csv('visits.csv', parse_dates=[1])
checkouts = pd.read_csv('checkouts.csv', parse_dates=[1])

#print 5 rows of visits table
print(visits.head())

#print 5 rows of checkouts table
print(checkouts.head())

#merge two tables (able to merge because they are similar in shape)
v_to_c = visits.merge(checkouts)

#print 5 rows of new table
print(v_to_c.head())

#calculate time between checkout_out and vist_time
v_to_c['time'] = v_to_c.checkout_time - v_to_c.visit_time

#print 5 rows of with new column
print(v_to_c.head())

#mean time between checkout_out and vist_time
print(v_to_c.time.mean())
