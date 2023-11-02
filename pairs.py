# A program which assists in the solving of the 3x3x3 Rubik's cube blindly
# A letter pair is inputted, and the corresponding word to remember the pair
# Is outputted. Additionally it can be used to change words.
#
# By Hudson Hadley

# This reloads objects so it updates if menu did not close
import importlib
import objects
importlib.reload(objects)

from objects import spread_sheet, get_word

# Copies the file with the spreadsheet to be changed at the end
copy = open("objects.py", "r").read()



pair = ""
last_pair = ""

print("Enter . to return to menu")
print()
print("Enter ; to replace the previous pair")

# Go through the loop for as long as the user wants
while True:

    # Get the input as two letters
    while True:
        last_pair = pair
        pair = input("\nInput letter pair:").upper()


        if len(pair) == 2 and "A" <= pair[0] <= "X" and "A" <= pair[1] <= "X":
            break

        elif pair == ";" and last_pair != "=" and len(last_pair) == 2 and "A" <= last_pair[0] <= "X" and "A" <= last_pair[1] <= "X":

            # Make sure the user is not replacing a double pair besides CC II WW and SS
            if last_pair[0] == last_pair[1] and last_pair[0] not in ["C", "I", "W", "S"]:
                print("{}{} is a double pair. It will never come up in memorizing".format(last_pair[0], last_pair[1]))

            else:

                # Instructions for how to input a word
                print()
                print("The current word for {} is : {}".format(last_pair, get_word(last_pair[0], last_pair[1])))
                print("Press enter if you do not want to change anything")
                print()
                print("Use / between words to designate two options")
                print("eg. if JO was Joe/Joseph, either could be entered and both would be correct")
                print()
                print("Use () around a word to designate it as optional")
                print("eg. if AL was Allen (Iverson), Iverson would be an optional thing to input")
                print()

                # Get the new word for the last pair
                while True:
                    new_word = input("Input the new word for {} : ".format(last_pair))

                    double_words = False

                    for i in range(len(spread_sheet)):
                        for j in range(len(spread_sheet)):
                            if spread_sheet[i][j].upper() == new_word and new_word:
                                print("\n{} is already being used for {}{}".format(new_word, chr(i + 65), chr(j + 65)))
                                double_words = True

                    if not double_words:
                        break

                # If the new word isn't just hitting enter
                if new_word != "":
                    # Translate the letter pair into numbers -----> [A, B] into [0, 1]
                    num = [int(ord(last_pair[0])) - 65, int(ord(last_pair[1]) - 65)]
                    # Change the spread_sheet using the new word
                    spread_sheet[num[0]][num[1]] = new_word

        elif pair == ".":
            break


    if pair == ".":
        break

    word = get_word(pair[0], pair[1])

    print("Letter pair: {}".format(pair))
    print("Word: {}".format(word))


# Now objects.py must be altered to reflect the new spread_sheet assuming that it has been changed
# First copy everything up to the spreadsheet section

# Find where the spread_sheet variable starts
index = 0
while True:

    s = ""
    for i in range(index, index + len("spread_sheet =")):
        s += copy[i]

    if s == "spread_sheet =":
        break

    index += 1

# This will be the new file
# To begin with, everything up to the point where the spread_sheet starts is the same
new_file = copy[: index]


# This will be the code in objects.py that is replaced. It starts with spread_sheet = ["N/A,...]
new_file += "spread_sheet = ["

# For every row in the spread_sheet
for i in range(len(spread_sheet)):
    # If it's not the first line then add some spacing so it lines up nicely --------->    spread_sheet = [".....
    if i != 0:                                                               #                             ".....
        new_file += "\t\t\t   "

    # Start with an opening quotation mark and then
    new_file += "\""


    # This creates "blah, blah, blah...blah", \n

    # For all of the words except the last one
    for j in range(len(spread_sheet[i]) - 1):
        # Place the word then a comma then a space
        new_file += spread_sheet[i][j] + "," + " "

    # For the last word (except the last word of the last line) place the word then a closing quotation mark then a comma then an enter
    if i != len(spread_sheet) - 1:
        new_file += spread_sheet[i][len(spread_sheet[i]) - 1] + "\"" + "," + "\n"

    # If it is the last word then end it with a closing quotation mark and a closing bracket
    else:
        new_file += spread_sheet[i][len(spread_sheet[i]) - 1] + "\"" + "]" + "\n"


# Once the spread_sheet variable is changed, the code after it needs to be copied
# Find where the spread_sheet ends at N/A"]
while copy[index] != "N" or copy[index + 1] != "/" or copy[index + 2] != "A" or copy[index + 3] != "\"" or copy[index + 4] != "]":
    index += 1

# Since index only will represent N in the N/A"], we need to add 5 to get to the end
index += 6

# Copy everything after the end of the spread_sheet
new_file += copy[index :]

with open("objects.py", "w") as f:
    f.write(new_file)
    f.flush()
