# This code serves as the menu for everything concerning 3BLD.
#
# By Hudson Hadley


while True:
    print()
    print("----------------------------------------------------------")
    print("Menu:")
    print()
    print("Enter 1 to quiz yourself")
    print()
    print("Enter 2 to alter or look up a pair")
    print()
    print("Enter 3 to see the current data from cstimer")
    print()
    print("Enter . to quit")

    while True:
        choice = input()

        if choice in ["1", "2", "3", "."]:
            break

        else:
            print("Enter 1, 2, 3, or .")

    if choice == "1":
        print()
        print("----------------------------------------------------------")
        print("Quiz:")
        print()
        exec(open("/Users/Hudson/Programs/Python/3BLD/quiz.py").read())

    elif choice == "2":
        print()
        print("----------------------------------------------------------")
        print("Pairs:")
        print()
        exec(open("/Users/Hudson/Programs/Python/3BLD/pairs.py").read())

    elif choice == "3":
        print()
        print("----------------------------------------------------------")
        print("Data:")
        print()
        exec(open("/Users/Hudson/Programs/Python/3BLD/get_data.py").read())

    elif choice == ".":
        break

