#python3 python_practice/ins_data_loop_and_comprehension.py to run from root folder

#data
names = ["Judith", "Abel", "Tyson", "Martha", "Beverley", "David", "Anabel"]
estimated_insurance_costs = [1000.0, 2000.0, 3000.0, 4000.0, 5000.0, 6000.0, 7000.0]
actual_insurance_costs = [1100.0, 2200.0, 3300.0, 4400.0, 5500.0, 6600.0, 7700.0]

# Add your code here
#initialize total cost variable
total_cost = 0

#for loop to sum actual ins costs
for actual in actual_insurance_costs:
  total_cost += actual
print(f"Total Insurance Costs: {total_cost}.")

#calculate average cost
average_cost = total_cost / len(actual_insurance_costs)
print(f"Average Insurance Cost: {average_cost}")

#for loop to show actual ins cost w/person's name
for i in range(len(names)):
  name = names[i]
  insurance_cost = actual_insurance_costs[i]
  print(f"The insurance cost for {name} is {insurance_cost} dollars.")
  if insurance_cost > average_cost:
    print(f"The insurance cost for {name} is above average.")
  elif insurance_cost < average_cost:
    print(f"The insurance cost for {name} is below average.")
  else:
    print(f"The insurance cost for {name} is equal to the average.") 

#creating list comprehension to adjust estimated ins costs
updated_insurance_costs = [11/10 * i for i in estimated_insurance_costs]
print(updated_insurance_costs)
