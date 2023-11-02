# A program which assists in memorizing words for the letter pairs in 3BLD.
# It compiles a list of the letter pairs desired to be quizzed and selects them randomly.
# After each one is answered correectly it reviews the ones you got wrong by going over
# each pair the number of times they were answered incorrectly
#
# By Hudson Hadley

# The spreadsheet is a 2D array of words for AA - XX
# The get word function takes in a letter pair and outputs a word
from objects import spread_sheet, get_word

# For picking which letter pair to test
from random import choice

# For timing how quickly one answers
from time import time

# network holds a class for a neural network which is used for determining if words should be counted as right or wrong
# lowest_cost holds good weights and biases for our network
from typo_network import network, lowest_cost

# We need numpy for the input layer of the neural network
import numpy as np


# This will help with spell check
from functions import key_distance

def levenshtein_distance(word1, word2):
    # Create a matrix to store the distances between substrings
    matrix = [[0] * (len(word2) + 1) for _ in range(len(word1) + 1)]

    # Initialize the first row and column of the matrix
    for i in range(len(word1) + 1):
        matrix[i][0] = i
    for j in range(len(word2) + 1):
        matrix[0][j] = j

    # Calculate the Levenshtein distance
    for i in range(1, len(word1) + 1):
        for j in range(1, len(word2) + 1):
            cost = 0 if word1[i - 1] == word2[j - 1] else 1
            matrix[i][j] = min(
                matrix[i - 1][j] + 1,  # Deletion
                matrix[i][j - 1] + 1,  # Insertion
                matrix[i - 1][j - 1] + cost,  # Substitution
            )

    return matrix[len(word1)][len(word2)]


def keyboard_distance(key1, key2):
    key_positions = {
    "q": (0, 0), "w": (1, 0), "e": (2, 0), "r": (3, 0), "t": (4, 0), "y": (5, 0), "u": (6, 0), "i": (7, 0), "o": (8, 0), "p": (9, 0),
    "a": (0.5, 1), "s": (1.5, 1), "d": (2.5, 1), "f": (3.5, 1), "g": (4.5, 1), "h": (5.5, 1), "j": (6.5, 1), "k": (7.5, 1), "l": (8.5, 1),
    "z": (1, 2), "x": (2, 2), "c": (3, 2), "v": (4, 2), "b": (5, 2), "n": (6, 2), "m": (7, 2)
    }
    
    if key1 not in key_positions or key2 not in key_positions:
        return -1  # Return -1 if either of the keys is not found in the dictionary

    pos1 = key_positions[key1]
    pos2 = key_positions[key2]

    # Calculate Euclidean distance between the two key positions
    distance = math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    return distance
    

# Tests if the guess is correct
def correct(guess, answer):

    # Get rid of any leading or following spaces
    guess = guess.strip().upper()

    acceptable_answers = []

    if "/" in answer:
        answer = list(answer.split("/"))

    else:
        answer = [answer]

    # This will keep track of if there are parentheses
    is_parentheses = False

    for i in answer:
        # The answers as they are, are both acceptable
        acceptable_answers.append(i)

        # Get rid of parentheses stuff  --- AJ (Mathwin) ----> AJ
        remove = False
        answer_without_parentheses = ""

        # Go through the string
        for j in i:
            # If we hit the parentheses
            if j == "(":
                is_parentheses = True
                # Then we begin to remove
                remove = True

            # If we're not in the parentheses then we want it
            if not remove:
                answer_without_parentheses += j

            # Once we hit the end of the parentheses we care again
            if j == ")":
                remove = False

        if is_parentheses:
            # The answers with no parentheses things are acceptable
            acceptable_answers.append(answer_without_parentheses.strip())

            # The answers with the parentheses stuff not in parentheses is acceptable
            acceptable_answers.append(i.replace("(", "").replace(")", ""))


    # PRECURSOR TO NEURAL NETWORK_____________________________________________________________________________

    # # See if the guess is (or close to) one of the acceptable answers
    # for i in acceptable_answers:
    #
    #     # # len(guess) // 2.5 is just an arbitrary number
    #     # # It means you get one mess up for every 2.5 letters
    #     # if levenshtein_distance(i.upper(), guess.upper()) <= len(guess) // 2.5:
    #     #     return True
    #
    # else:
    #     return False

    # NEURAL NETWORK____________________________________________________________________________________________

    net = network.Network([5, 3, 1], lowest_cost.weights, lowest_cost.biases)

    for i in acceptable_answers:
        i = i.upper()
        # Levenshtein distance between words
        l_dist = levenshtein_distance(i, guess)

        # Difference between lengths
        diff_word_length = abs(len(i) - len(guess))

        # Distance between each relative key
        dist_bt_letters = 0
        altered_word = i.replace(" ", "")
        altered_guess = guess.replace(" ", "")

        for j in range(min(len(altered_guess), len(altered_word))):
            dist_bt_letters += key_distance(altered_word[j], altered_guess[j])

        # difference in distance traveled
        guess_distance = 0
        word_distance = 0

        for j in range(len(altered_guess) - 1):
            guess_distance += key_distance(altered_guess[j], altered_guess[j + 1])

        for j in range(len(altered_word) - 1):
                word_distance += key_distance(altered_word[j], altered_word[j + 1])

        dif_in_distance = abs(guess_distance - word_distance)

        average_length = (len(i) + len(guess)) / 2

        # Put the inputs into the network and get the outputs
        output = net.feedforward(np.array([[l_dist], [diff_word_length], [dist_bt_letters], [dif_in_distance], [average_length]], dtype=np.float32))[0][0]

        # print([l_dist], [diff_word_length], [dist_bt_letters], [dif_in_distance], [average_length])
        # print(output)

        # If the output neuron is closer to 1 then it is right
        if round(output) == 1:
            return True

    # If none of the acceptable answers lead to a correct answer, then it is false
    else:
        return False


# This will get the letters one wants to be tested, make sure they make sense, format them correctly, make a list
# Of all the letters expressed in the input, and then return them
def get_letters():
    # Instructions of how to input letters to be tested
    print("What letters would you like to be tested on?")
    print("Enter either individual letters (A, B, C) or as a range (A-C)")
    print("Seperating each individual letter or range with commas.")
    print("For a random letter, input Z or if you want multiple random letters ")
    print("input a number before Z (5Z).")
    print("If you want to be tested on all the letters, enter all.")
    print("For example: A-D, G, K-P, 2Z could be A, B, C, D, E, G, K, L, M, N, O, P, R")

    while True:
        # Get the input and format it
        # Make all the things capitalized so it is easier to work with      "a-b, c" ----> "A-B, C"
        # Get rid of all the spaces                                         "A-B, C" ----> "A-B,C"
        # Turn it into a list with eah element seperated by commas          "A-B, C" ----> ["A-B", "C"]
        raw_letters = input().upper().replace(" ", "").split(",")

        # Check to see if the inputted letters are cool beans
        # Go through all the elments in the input (each thing sperated by commas)
        for i in raw_letters:

            # Can we break out of the while loop?
            cool_beans = False

            # If it is one long and is between A and X or is Z then continue
            if (len(i) == 1 and "A" <= i <= "X") or i == "Z":
                cool_beans = True

            # If it is three long and the first and last are letters between A and X and the middle is a "-" then continue
            # Additionally make sure that the first letter is smaller than the last (nothing like X-A)
            elif len(i) == 3 and "A" <= i[0] <= "X" and i[1] == "-" and "A" <= i[2] <= "X" and ord(i[0]) < ord(i[2]):
                cool_beans = True

            # If it is ##Z or #Z where the numbers represent how many random letters
            # If it is #Z make sure the # is between 1 and 9
            # If it is ##Z make sure the ## is between 1 and 24
            elif "Z" in i:
                if len(i) == 2 and "Z" == i[1] and "0" < i[0] <= "9":
                    cool_beans = True

                elif len(i) == 3 and "Z" == i[2] and "0" < i[0] < "3" and "0" <= i[1] <= "9":
                    cool_beans = True

            # If it is all
            elif i == "ALL":
                i = ["A-X"]
                cool_beans = True

            # If something is not cool beans, then get out of the for loop and ask for another input
            else:
                print(i)
                cool_beans = False
                break

        # If it is cool beans break out of the while loop
        if cool_beans:
            break

    # Letters is the actual list of letters going to be tested with no dashes or numbers with the z
    letters = []

    # These are the potential letters that a random choice could be
    picks_for_random = [chr(i + 65) for i in range(24)]

    # Sort the raw_letters according to the last letter in each index
    raw_letters.sort(key=lambda x: x[len(x) - 1])

    # Go through the raw letters
    for i in raw_letters:
        # If there is a range
        if "-" in i:

            # Go through all the letters from the first letter to the last one
            for j in range(ord(i[0]), ord(i[2]) + 1):

                # If the letter in the range is not in the list already add it and remove it from the random list
                if chr(j) not in letters:
                    letters.append(chr(j))
                    picks_for_random.remove(chr(j))

        # If there is just a letter and it is not Z add it and remove it from the random list
        elif len(i) == 1 and "Z" not in i:
            # If it is not in the list add it
            if i not in letters:
                letters.append(i)
                picks_for_random.remove(i)

        # If it is a Z case
        else:
            # If it is just the letter Z without any numbers
            if len(i) == 1:
                # If there is still random letters to pick
                if len(picks_for_random) > 0:
                    # Pick a random letter
                    pick = choice(picks_for_random)
                    # Add it
                    letters.append(pick)
                    # Remove it from the random list
                    picks_for_random.remove(pick)

            # If it is a Z case with a number
            else:
                # If the number is one digit (#Z)
                if "Z" == i[1]:
                    # Change the number into an int
                    # ord("0") == 48
                    num = ord(i[0]) - 48

                # If the number is two digit (##Z)
                else:
                    # Change the number into an int
                    # ord("0") == 48
                    # Take the first number and multiply it by ten and add the second
                    # "23" --> 20 + 3
                    num = (ord(i[0]) - 48) * 10 + ord(i[1]) - 48

                # Pick a random letter num many times
                for j in range(num):
                    # If there is still random letters to pick
                    if len(picks_for_random) > 0:
                        # Pick a random letter
                        pick = choice(picks_for_random)
                        # Add it
                        letters.append(pick)
                        # Remove it from the random list
                        picks_for_random.remove(pick)

    return letters





# -------------------------------------------------------------------------------- INPUT -----------------------------
# This will hold [AB, AC, AD, AE....XW] (all the letter pairs we want to be tested)
options = []

# Which letters are being tested
# These start off as false, then after inputting what letters you want, are altered
letters_tested = {'A': False,
                  'B': False,
                  'C': False,
                  'D': False,
                  'E': False,
                  'F': False,
                  'G': False,
                  'H': False,
                  'I': False,
                  'J': False,
                  'K': False,
                  'L': False,
                  'M': False,
                  'N': False,
                  'O': False,
                  'P': False,
                  'Q': False,
                  'R': False,
                  'S': False,
                  'T': False,
                  'U': False,
                  'V': False,
                  'W': False,
                  'X': False}

# Get a list of the letters desired to be tested
letter_input = get_letters()


# Once we have the input go through all of them
for i in letter_input:
    # Make each letter true (meaning we want it to be tested)
    letters_tested[i] = True


# ----------------------------------------------------------------- PAIRS ------------------------------------------


# Keep track of how many you got wrong
strikes = 0

# Find the last letter being tested (for commas)
for i in range(ord("X"), ord("A") - 1, -1):

    # If it is true since we are going backwards, this must be the last one
    if letters_tested[chr(i)]:
        # Assign it and get out
        last_one = chr(i)
        break

print("Letters being tested:")

# All the letters
letters = [chr(i) for i in range(ord("A"), ord("X") + 1)]

# Go through all the letters
for i in letters:

    # If we want it to be tested
    if letters_tested[i]:

        # If it is the last one we don't want a comma
        if i != last_one:
            # Say it is being tested
            print(i, end=", ")

        else:
            print(i)

        # Add all the pairs which start with that letter
        for j in range(ord("A"), ord("X") + 1):

            # If it is not the same letter (since same letter pairs are impossible besides I,S,C,W for M2/4x4)
            if i != chr(j) or i == "I" or i == "S" or i == "C" or i == "W":
                options.append(i + chr(j))

# Line break
print()
print()

# Literally just a copy of options for the end
letters_being_tested = [i for i in options]


# ----------------------------------------QUIZ BEGINS---------------------------------------------------

# Pairs tested
letter_pair_count = 0

# How many pairs are being tested
total_pairs = len(options)

times_pair_was_wrong = {}

# For every option set the strikes for each pair to 0 to begin with
for i in options:
    times_pair_was_wrong[i] = 0

total_time = 0

# ----------------------------------------INSTRUCTIONS--------------------------------------------------

print("Enter = to pause")
print()
print()

paused = False

input("Press enter to start...\n")
# ----------------------------------------GO------------------------------------------------------------

# This will keep track if the program has been quitted or not
# This is so that if you quit the main quiz, you do not have to do the review
quitted = False


guess = ""


# Go through the options until each has been answered correctly
while len(options) > 0:

    # Pick a random pair out of the options
    pick = choice(options)


    # We assume it is not paused unless it is paused. If it is paused, we then set it to true
    paused = False

    # Ask for the word
    print("Pairs left: {} / {}".format(len(options), total_pairs))
    start = time()
    guess = input("{}: ".format(pick))

    # If a pause in the quiz is requested ----------------------------------------PAUSE
    if guess.strip() == "=":
        paused = True

        print()
        print("----------------------------------------------------------")
        print("Pause:")
        print()

        while True:
            print("Press enter to resume")
            print("Enter . to quit")
            print()
            pause_input = input()

            if pause_input in ["", "."]:
                break

        # If they want to quit
        if pause_input == ".":
            # Get an input that is yes or no to make sure the user actually wants to quit
            while True:
                print("Are you sure you want to quit? No progress will be saved")
                are_you_sure = input("Yes or No: ").upper()

                # If the input is yes or no get out
                if are_you_sure in ["YES", "NO"]:
                    break

            # If its yes then break out of the quiz
            if are_you_sure == "YES":
                quitted = True
                break

            # If its not yes then just continue
            else:
                continue


        # If the input is not . then just continue on with the quiz
        print()
        print("----------------------------------------------------------")
        print("Quiz:")
        print()


    # If it is cool beans ------------------------------------------------------CORRECT
    elif correct(guess.upper(), get_word(pick[0], pick[1])):
        print("CORRECT")
        print("{}: {}".format(pick, get_word(pick[0], pick[1])))
        print()

        total_time += time() - start

        # Get rid of it
        options.remove(pick)

        # Add that a letter has been tested
        letter_pair_count += 1



    # If it is not cool beans -------------------------------------------------INCORRECT
    else:
        # Sometimes it's hard to see if you got a pair incorrect, so add some ---- to alert the user
        print("INCORRECT-----------------------")
        print("{}: {}".format(pick, get_word(pick[0], pick[1])))
        print()

        # Also make an annoying noise
        print("\a")

        total_time += time() - start

        # Add that a letter has been tested
        letter_pair_count += 1

        # Add a strike to that pair
        times_pair_was_wrong[pick] += 1
        strikes += 1


# ----------------------------------------------------------------------------------------------REVIEW

review_pairs = []

# If we got stuff wrong, give us the run down
if strikes > 0:
    print("Pairs you got wrong:")
    for i in letters_being_tested:

        # If you got it wrong once
        if times_pair_was_wrong[i] == 1:

            # Add it once
            review_pairs.append(i)

            # Output the info
            print("{}: {} time".format(i, times_pair_was_wrong[i]))

        # If you got it wrong more than once
        elif times_pair_was_wrong[i] > 0:

            # Add it to review pairs as many times as you got wrong
            for j in range(times_pair_was_wrong[i]):
                review_pairs.append(i)

            # Output the info
            print("{}: {} times".format(i, times_pair_was_wrong[i]))

if letter_pair_count != 0:
    print("Accuracy: {}%".format(round(100 * (letter_pair_count - strikes) / letter_pair_count, 2)))
    print("Average time: {} seconds".format(round(total_time / letter_pair_count, 2)))
    print()


# If we did not quit out of the quiz, then go over pairs you got wrong
if not quitted:
    # If we have review pairs
    if len(review_pairs) > 0:
        print("Review Pairs:")

    print()

    total_pairs_got_wrong = [i for i in review_pairs]

    while len(review_pairs) > 0:

        # Choose a random one if there was not a pause (otherwise just ask the one before the pause)
        if not paused:
            pick = choice(review_pairs)


        # We assume it is not paused unless it is paused. In that case we then set it to true
        paused = False

        # Ask for the word
        print("Pairs left: {} / {}".format(len(review_pairs), len(total_pairs_got_wrong)))
        guess = input("{}: ".format(pick))


        # If it is cool beans ------------------------------------------------------CORRECT
        if correct(guess, get_word(pick[0], pick[1])):
            print("Correct!")
            print("{}: {}".format(pick, get_word(pick[0], pick[1])))
            print()

            # Get rid of it
            review_pairs.remove(pick)


        # If it is not cool beans -------------------------------------------------INCORRECT
        else:
            print("Incorrect-----------------------")
            print("{}: {}".format(pick, get_word(pick[0], pick[1])))
            print()

            print("\a")

# B#cause the beans are cool
print("Cool beans")
