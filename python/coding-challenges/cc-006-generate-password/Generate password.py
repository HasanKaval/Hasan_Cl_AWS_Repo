import random

def get_random_letter():
    name = input("Please enter your full name(without any space): ").lower()
    result = ''.join(random.choice(name) for i in range(3))
    print(result + str(random.randrange(1000, 10000)))

get_random_letter()

    
    