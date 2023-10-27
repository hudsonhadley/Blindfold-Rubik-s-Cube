# A program which collects training data for a neural network by asking
# the user to input a random word from 
# https://www.mit.edu/~ecprice/wordlist.10000, then asking if it should
# be counted as correct or incorrect.
#
# By Hudson Hadley




import random
import sys

# Change the path to just Python so we can access functions
sys.path.insert(0, "/Users/Hudson/Programs/Python")

from functions import levenshtein_distance, key_distance

def tally():
	f = open("/users/hudson/programs/python/3bld/typo_network/best_time.py", "r")
	s = f.read()
	f.close()

	# If collecting test_data it should be however much training data there is plus 5
	# If collecting training_data it should be 3
	return s.count("\n") - 10005 #3

w = open("words.txt", "r").read().split("\n")


first = True
while tally() % 1000 != 0 or first:
	p = random.choice(w)
	print(tally())
	print()
	inp = input("Type {}: ".format(p)).upper()

	p = p.upper()

	yay_nay = input("Did you get it right? (y or n): ").upper()

	if yay_nay == "Y":
		y = 1

	else:
		y = 0

	# Levenshtein distance between words
	l_dist = levenshtein_distance(p, inp)

	# Difference between lengths
	diff_word_length = abs(len(p) - len(inp))

	# Distance between each relative key
	dist_bt_letters = 0
	altered_word = p.replace(" ", "")
	altered_guess = inp.replace(" ", "")

	for i in range(min(len(altered_guess), len(altered_word))):
		dist_bt_letters += key_distance(altered_word[i], altered_guess[i])

	# difference in distance traveled
	guess_distance = 0
	word_distance = 0

	for i in range(len(altered_guess) - 1):
		guess_distance += key_distance(altered_guess[i], altered_guess[i + 1])

	for i in range(len(altered_word) - 1):
		word_distance += key_distance(altered_word[i], altered_word[i + 1])

	dif_in_distance = abs(guess_distance - word_distance)

	average_length = (len(p) + len(inp)) / 2

	# print(l_dist)
	# print(diff_word_length)
	# print(dist_bt_letters)
	# print(dif_in_distance)
	# print(average_length)

	f = open("/users/hudson/programs/python/3bld/typo_network/best_time.py", "a")
	f.write("(np.array([[{}], [{}], [{}], [{}], [{}]], dtype=np.float32), np.array([[{}]], dtype=np.float32)),\n".format(l_dist, diff_word_length, dist_bt_letters, dif_in_distance, average_length, y))
	f.close()

	first = False
