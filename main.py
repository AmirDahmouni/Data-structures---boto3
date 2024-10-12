from helper import days_to_units
from user import User
from post import Post
from parseSheet import parseExcel
import os
import requests

print(os.name)
print("Hello world !")
print('Hello world !')
print(-20)
print(50)
print(23.35)
print(20*24*13.6/25)
print("20 days are" + str(50) + "minutes")
print(f"20 days are { 25 *2 } minutes")
print(type("Amir"))

to_seconds = 24 * 60 * 60
name_unit = "seconds"
print(f"35 days are {to_seconds} {name_unit}")

to_seconds = 24
name_unit= "hours"
def days_to_units_message(number_of_days, unit, message):
    local_variable = "internal message"
    print(f"{number_of_days} days are {unit * number_of_days} {name_unit}")
    print(f"{local_variable} then global message, {message}, all good !")

days_to_units_message(35, 24, "Awesome")


user_input = ""
def input_validate_and_execute():
  try:
      while user_input != "exit":
        user_input = input("Hey user, enter a number of days and i will convert it to hours! OR exit \n")
        if(user_input.isdigit()):
          days = days_to_units(int(user_input), 24)
          print(f" Days = {days}")
        else:
          print("Your input is not a number")
  except ValueError:
     print("Your input is invalid")



user_input = input("Hey user, enter a number of days as a comma seperated list  and i will convert them to hours! \n")
for num_of_days_element in user_input.split(","):
  days = days_to_units(int(num_of_days_element), 24)
  print(days)

# Set does not duplicate value
# basic operations of set
set_elements = set(user_input.split(","))
set_elements.add(2651326)  # add it randomly depends on available memory case
for num_of_days_element in set_elements :
  days = days_to_units(int(num_of_days_element), 24)
  print(days)
set_elements.remove(2651326)
print(f"set {set_elements}")


# built-in function
# print()
# input()
# set()
# int()
# bool()
# chr()
# round(2.65)
# max()
"2, 3".split(",")
[1,2,4].append(3)


# Dictionnary data

user_input = ""
def input_validate_and_execute():
  while user_input != "exit":
    user_input = input("Hey user, enter a number of days, unit to convert OR exit \n")
    days_unit = user_input.split(":")
    days_and_unit = {"days": days_unit[0], "unit": days_unit[1]}
    days_to_units(days_and_unit["days"], days_and_unit["unit"])



parseExcel("inventory.xlsx")

# Create users
main_user = User("adh@gmail.com", "Amir Dahmouni", "pwd1", "DevOps Engineer")
main_user.get_user_info()

developer = User("ddh@aa.com", "Daniel", "pwd2", "Developer")
developer.get_user_info()

# Create posts for users
post_one = Post("CI/CD jenkins pipeline", developer.name)
developer.add_post(post_one)

post_two = Post("Learning Python", main_user.name)
main_user.add_post(post_two)

# Get all posts for each user
print("\nPosts by Amir:")
main_user.get_all_posts()

print("\nPosts by Daniel:")
developer.get_all_posts()


response = requests.get("https://api.github.com/users/AmirDahmouni/repos")
my_projects = response.json()
print(type(my_projects))

# print just the names and urls
for project in my_projects:
    print(f"Project Name: {project['name']}\n Clone Url: {project['clone_url']}\n")



