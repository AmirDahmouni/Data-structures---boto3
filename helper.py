def days_to_units(number_of_days, unit):
    # we want to do conversion only for positive numbers
    if number_of_days > 0:
      return f"{number_of_days} days are {unit* number_of_days}"
    elif number_of_days == 0:
       return "0 not accepted !"
    else:
      return "you entered a negative value, so no conversion for you"