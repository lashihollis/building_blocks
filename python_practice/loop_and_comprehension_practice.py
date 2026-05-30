#python3 python_practice/loop_and_comprehension_practice.py to run from root folder

#generate a list of numbers within a rangr
single_digits = range(10)
print(list(single_digits))

#create new list squares w/for loop
squares = []
for digit in single_digits:
  print(digit)
  squares.append(digit ** 2)
print(squares)

#create new list cubes w/list comprehension
cubes = [digit ** 3 for digit in single_digits]
print(cubes)