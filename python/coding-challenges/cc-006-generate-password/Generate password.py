name = input("Please enter your full name(without any space): ").lower()

import random

def get_random_letter():
    result = ''.join(random.choice(name) for i in range(3))
    print(result, end='')
get_random_letter()
print(random.randrange(1000, 10000))
    
    