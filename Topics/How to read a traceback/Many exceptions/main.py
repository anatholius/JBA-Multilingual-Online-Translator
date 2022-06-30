import math


def find_sqrt(number):
    try:
        print(math.sqrt(int(number)))
    except (TypeError, ValueError):
        print('Please pass a number like "5" or 5')
