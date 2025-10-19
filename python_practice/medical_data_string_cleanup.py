medical_data = \
"""Marina Allison   ,27   ,   31.1 , 
#7010.0   ;Markus Valdez   ,   30, 
22.4,   #4050.0 ;Connie Ballard ,43 
,   25.3 , #12060.0 ;Darnell Weber   
,   35   , 20.6   , #7500.0;
Sylvie Charles   ,22, 22.1 
,#3022.0   ;   Vinay Padilla,24,   
26.9 ,#4620.0 ;Meredith Santiago, 51   , 
29.3 ,#16330.0;   Andre Mccarty, 
19,22.7 , #2900.0 ; 
Lorena Hodson ,65, 33.1 , #19370.0; 
Isaac Vu ,34, 24.8,   #7045.0"""

#replace # with $
updated_medical_data = medical_data.replace('#','$')

#iterates through list to calculate the number of medical records
num_records = 0
for records in updated_medical_data:
  if records == "$":
    num_records += 1

#splits up records into a list of each medical record
medical_data_split = updated_medical_data.split(";")
#print(medical_data_split)

#iterates through medical_data_split and appends records into medical_records
medical_records = []
for record in medical_data_split:
  medical_records.append(record.split(","))
#print(medical_records)

#cleaning up whitespace
medical_records_clean = []
#loops through each record; create empty list for cleaned records
for x in medical_records:
  record_clean = []
#loops through each item in each medical record, strip whitespace, and append to record clean
  for item in x:
    record_clean.append(item.strip())
  medical_records_clean.append(record_clean)

#make all records uppercase
for record in medical_records_clean:
  record[0] = record[0].upper()
  #print(record[0])

#create 4 empty lists to store variables
names = []
ages = []
bmis = []
insurance_costs = []

#iterate through medical_records_clean to append data into the appropriate variable
for item in medical_records_clean:
  names.append(item[0])
  ages.append(item[1])
  bmis.append(item[2])
  insurance_costs.append(item[3])

#create bmi variable and set equal to zero
total_bmi = 0

#iterate through bmis and add each bmi to total bmi; convert bmi to float
for bmi in bmis:
  total_bmi += float(bmi)

#calculating avg bmi and printing results
average_bmi = total_bmi/ len(str(total_bmi))

print("Average BMI " + str(round(average_bmi)))

#calculate avg insurance costs; for loop and removal of $ sign
insurance = []
for insure in insurance_costs:
  insurance.append(insure.strip("$"))
#print(insurance)

total_ins_cost = 0
for cost in insurance:
  total_ins_cost += float(cost)

avg_cost = total_ins_cost/ len(str(round(total_ins_cost)))

print("Average Insurance Cost: " + str(avg_cost))

#for loop that outputs a tring for each person
for i in range(0, len(medical_records_clean)):
    print("{0} is {1} years old with a BMI of {2} and an insurance cost of {3}.".format(names[i], ages[i], bmis[i], insurance_costs[i]))