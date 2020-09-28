def menu():
    print("Welcome to the phonebook application")
    print('1. Find phone number')
    print('2. Insert a phone number')
    print('3. Delete a person from the phonebook')
    print('4. Terminate')
    print()

numbers = {}
menu_choice = 0
menu()
while menu_choice != 4:
    menu_choice = int(input("Select operation on Phonebook App (1/2/3): "))
    if menu_choice == 1:
        x=input("Find the phone number of :")
        if x in name:
            print(numbers[x])
        else:
            print(f"Couldn't find phone number of {x}")
        print()
    elif menu_choice == 2:
        name = input("Insert the name of the person: ")
        phone =input("Insert the number of the person: ")
        if phone.isdigit():
            numbers[name] = phone
            print(f"Phone number of {name} is inserted into the phonebook")
        else:
            print ("Invalid input format, cancelling operation ...")
            menu()
    elif menu_choice == 3:
        name=input("Whom to delete from phonebook : ")
        if name in numbers:
            del numbers[name]
            print(f"{name} is deleted from the phonebook")
        else:
            print(name, "was not found")
    elif menu_choice != 4:
        print("Exiting phonebook")
        menu()
