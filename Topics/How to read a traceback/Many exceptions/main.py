import math

def find_sqrt(number):
    try:
        print(math.sqrt(number))
    except TypeError:
        print(math.sqrt(int(number)))