# Heavily influenced by http://neuralnetworksanddeeplearning.com/chap1.html
# For this neural network structure to train effectively with grid searching,
# it is necessary to create a file "best_time.py" which holds training_data and test_data,
# a file "lowest_cost.py" which holds information regarding the hyperparameters which yielded
# the lowest cost, a file "default_parameters.py" which holds the parameters at which the
# network should start at the beginning of each SGD training session, and a file "tested.py" which
# holds information regarding which hyperparameters have already been tested and which costs they yielded.
#
# By Michael Nielson with additions by Hudson Hadley

import numpy as np
import random
import time
from datetime import datetime
import math
import matplotlib.pyplot as plt
import os
import sys

# Since we run the program from 3BLD and not typo_network we need to change path to access these files
sys.path.insert(0, "/Users/Hudson/Programs/Python/3BLD/typo_network")
# lowest_cost needs to have lowest_cost, epochs, mini_batch_size, eta, weights, and biases
import lowest_cost
# tested needs to have tested and costs
import tested
# default_parameters needs to have weights and biases
import default_parameters


# Change the path to just Python so we can access functions
sys.path.insert(0, "/Users/Hudson/Programs/Python")
from functions import send_message


# np.exp will be raising e to the power of some big numbers in the cost function which will trigger a warning about the
# size of the number. numpy will still carry out the equation but it will do some rounding which is okay. This doesn't
# really matter that much because 1/big_number is very close still to 1/(big_number + little_number)
import warnings

warnings.filterwarnings("ignore")


class Network(object):

	def __init__(self, sizes, weights=None, biases=None):
		self.num_layers = len(sizes)
		self.sizes = sizes
		self.temp = []
		self.cost = []

		if weights == None and biases == None:
			self.biases = default_parameters.biases
			self.weights = default_parameters.weights

		else:
			self.weights = weights
			self.biases = biases


	# For a given input of a, go through the neural_network and return the output layer
	def feedforward(self, a):

		for b, w in zip(self.biases, self.weights):
			# print("Weights: ", w)
			# print("Activations: ", a)
			# print("Biases: ", b)
			# print("Dot product: ", np.dot(w, a))
			# print("Added biases: ", np.dot(w, a) + b)
			# print("Sigmoid: ", sigmoid(np.dot(w, a) + b))
			a = sigmoid(np.dot(w, a) + b)

		return a



	# Train the neural neural_network using stochastic gradient descent. Training data is a list of tuples like (x, y)
	# where x is the training input for the network, and y is the desired output. If test_data is provided then the
	# neural_network will be evaluated against the test_data after each epoch, and the partial progress will be
	# printed out. This slows things down substantially, but is useful for tracking progress.
	# Update_frequnecy is the number of epochs between updates. Show_graph states whether or not a graph will be shone
	# Bypass if set to true will ignore the fact that the model has already been trained with certain hyperparameters.
	# Reset_parameters if set to true will reset the parameters back to default_parameters instead of continuing with
	# the weights and biases already established.
	def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None, update_frequency=None, show_graph=True, bypass=False, reset_parameters=True):
		# Reset the cost if this model has already been trained
		self.cost = []
		self.temp = []

		if reset_parameters:
			self.weights = default_parameters.weights
			self.biases = default_parameters.biases


		# If we've already done this just output the cost
		if (mini_batch_size, eta, epochs) in tested.tested and not bypass:
			print()

			# Append the cost to the end of the cost so we don't run into problems in grid_search
			self.cost.append(tested.costs[tested.tested.index((mini_batch_size, eta, epochs))])

			print("Cost: {}".format(np.format_float_positional(tested.costs[tested.tested.index((mini_batch_size, eta, epochs))])))
			print("Lowest cost: {}".format(np.format_float_positional(lowest_cost.lowest_cost)))
			print("Difference: {}".format(
				np.format_float_positional(tested.costs[tested.tested.index((mini_batch_size, eta, epochs))] - lowest_cost.lowest_cost)))

			return

		if show_graph:
			fig = plt.gcf()
			fig.show()

			plt.xlabel("Epochs")
			plt.ylabel("Cost")

			plt.xlim([0, epochs])
			# We'll set ylim later once we compute the first one

			fig.canvas.draw()

			# Pick a random color for the graph
			color = random.choice(["b", "g", "r", "c", "m", "y", "k"])

		if not update_frequency:
			update_frequency = 10

		if test_data:
			n_test = len(test_data)

		n = len(training_data)

		start = time.time()

		# Day of Week, Month, Day, Year, Hour, Minute, Second, AM/PM
		print("Start time: ", datetime.fromtimestamp(start).strftime("%A, %B %d, %Y %I:%M:%S %p"))

		for j in range(epochs + 1):
			random.shuffle(training_data)

			mini_batches = [training_data[k: k + mini_batch_size] for k in range(0, n, mini_batch_size)]

			for mini_batch in mini_batches:
				self.update_mini_batch(mini_batch, eta)


			c = sum(self.temp) / len(self.temp)
			self.cost.append(c)
			self.temp = []

			if j == 0 and show_graph:
				plt.ylim([0, c * 1.1])


			if j % update_frequency == 0:
				if test_data:
					test = self.evaluate(test_data)
					print()
					print("Epoch {}: {} / {}".format(j, test, n_test))
					# np.format_float_positional makes sure no floats are printed as exponents
					print("Cost: {}".format(np.format_float_positional(self.cost[j])))
					print("Change of Cost: {}".format(np.format_float_positional(self.cost[j] - self.cost[j - 1])))

					if test == 1000:
						print(self.weights)
						print()
						print(self.biases)
						exit()

				else:
					print("Epoch {} complete".format(j))

				# If we want to show the graph
				if show_graph:

					plt.plot([i for i in range(j + 1)], self.cost, color)
					plt.pause(0.1)
					fig.canvas.draw()

				# The total time elapsed
				elapsed = time.time() - start
				# How many epochs are remaining
				epochs_remaining = epochs - j
				# The rate of change of time with respect to epochs
				rate = elapsed / (j + 1)
				# The estimated time remaining
				etr = rate * epochs_remaining

				completion = time.time() + etr

				# Day of Week, Month, Day, Year, Hour, Minute, Second, AM/PM
				print("Estimated Time of SGD Completion: ",
					  datetime.fromtimestamp(completion).strftime("%A, %B %d, %Y %I:%M:%S %p"))


		# Update tested
		if (mini_batch_size, eta, epochs) not in tested.tested:
			tested.tested.append((mini_batch_size, eta, epochs))
			tested.costs.append(self.cost[len(self.cost) - 1])
			f = open("tested.py", "w")
			f.write("tested = [")

			for i in range(len(tested.tested) - 1):
				f.write(str(tested.tested[i]) + ", ")

			f.write(str(tested.tested[len(tested.tested) - 1]) + "]\n\n\n")

			f.write("costs = [")

			for i in range(len(tested.costs) - 1):
				f.write(str(tested.costs[i]) + ", ")

			f.write(str(tested.costs[len(tested.costs) - 1]) + "]")



		if show_graph:
			plt.plot([i for i in range(j + 1)], self.cost, color)
			plt.pause(0.1)
			fig.canvas.draw()




		if self.cost[len(self.cost) - 1] < lowest_cost.lowest_cost:
			print()
			print("New lowest cost!")
			print("Previous Lowest Cost: {}".format(lowest_cost.lowest_cost))
			print("Cost: {}".format(self.cost[len(self.cost) - 1]))
			print("Epochs: {}".format(epochs))
			print("Mini Batch Size: {}".format(mini_batch_size))
			print("Learning Rate: {}".format(eta))
			print()

			f = open("lowest_cost.py", "w")

			# Import numpy for weights and biases
			f.write("import numpy as np\n\n")

			# Update lowest cost and hyperparameters
			f.write("lowest_cost = {}\nepochs = {}\nmini_batch_size = {}\neta = {}\n\n".format(self.cost[len(self.cost) - 1], epochs, mini_batch_size, eta))

			# Update weights and biases
			f.write("weights = [np.array({}, dtype=np.float32), np.array({}, dtype=np.float32)]\n\n".format(
				np.array2string(self.weights[0], separator = ','), np.array2string(self.weights[1], separator = ',')))

			f.write("biases = [np.array({}, dtype=np.float32), np.array({}, dtype=np.float32)]\n\n".format(
					np.array2string(self.biases[0], separator=','), np.array2string(self.biases[1], separator=',')))




		else:
			print()
			print("Cost: {}".format(np.format_float_positional(self.cost[len(self.cost) - 1])))
			print("Lowest cost: {}".format(np.format_float_positional(lowest_cost.lowest_cost)))
			print("Difference: {}".format(np.format_float_positional(self.cost[len(self.cost) - 1] - lowest_cost.lowest_cost)))


		if show_graph:
			input("Press enter to close graph")
			plt.close()



		# input("Press enter to close graph")
		# plt.close()



	# Updates the neural_network's weights and biases by applying gradient descent using backpropagation to a single
	# mini batch. The mini_batch is a list of tuples and eta is the learning rate.
	def update_mini_batch(self, mini_batch, eta):
		nabla_b = [np.zeros(b.shape) for b in self.biases]
		nabla_w = [np.zeros(w.shape) for w in self.weights]

		self.temp.append(sum((y[0][0] - self.feedforward(x)[0][0]) ** 2 for x, y in mini_batch) / len(mini_batch))

		for x, y in mini_batch:
			delta_nabla_b, delta_nabla_w = self.backprop(x, y)

			nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
			nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]


		self.weights = [w - (eta / len(mini_batch)) * nw for w, nw in zip(self.weights, nabla_w)]
		self.biases = [b - (eta / len(mini_batch)) * nb for b, nb in zip(self.biases, nabla_b)]

	# Returns a tuple of the gradient for the cost function
	def backprop(self, x, y):

		nabla_b = [np.zeros(b.shape) for b in self.biases]
		nabla_w = [np.zeros(w.shape) for w in self.weights]

		# feedforward
		activation = x
		activations = [x]  # list to store all the activations, layer by layer
		zs = []  # list to store all the z vectors, layer by layer

		for b, w in zip(self.biases, self.weights):
			z = np.dot(w, activation) + b
			zs.append(z)
			activation = sigmoid(z)
			activations.append(activation)

		# backward pass
		delta = self.cost_derivative(activations[-1], y) * \
				sigmoid_prime(zs[-1])


		nabla_b[-1] = delta
		nabla_w[-1] = np.dot(delta, activations[-2].transpose())

		# Note that the variable l in the loop below is used a little
		# differently to the notation in Chapter 2 of the book.  Here,
		# l = 1 means the last layer of neurons, l = 2 is the
		# second-last layer, and so on.  It's a renumbering of the
		# scheme in the book, used here to take advantage of the fact
		# that Python can use negative indices in lists.
		for l in range(2, self.num_layers):
			z = zs[-l]
			sp = sigmoid_prime(z)

			delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp
			nabla_b[-l] = delta
			nabla_w[-l] = np.dot(delta, activations[-l - 1].transpose())

		return nabla_b, nabla_w

	# Return the number of test inputs the neural neural_network gets right
	def evaluate(self, test_data):

		# A list of two tuples (x, y) where x is what is outputed from inputting test_data, and y
		# is the desired output for the test_data

		test_results = [(round(self.feedforward(x)[0][0]), y) for (x, y) in test_data]

		return sum(int(x == y) for (x, y) in test_results)

	# Returns weird math stuff that I don't understand
	# noinspection PyMethodMayBeStatic
	def cost_derivative(self, output_activations, y):
		return output_activations - y


	# Does a grid search for mini batch size and learning rate and finds the costs at each point
	def grid_search(self, training_data, m_min, m_max, m_int, e_min, e_max, e_int, epochs):

		# Decimals for rounding off
		decs = len(str(float(e_int)).split(".")[1])

		# Start the mini batch size at the max and the learning rate at the min
		m = m_max
		e = e_min

		# Lists for storing all the things
		es = []
		ms = []
		costs = []

		# Keep track of what cycle we're on
		cycle = 0

		# Have another keep track of how many have been trained and not skipped
		trained = 0

		# How many total cycles we will have to do
		total = ((m_max - m_min) / m_int + 1) * ((e_max - e_min) / e_int + 1)

		print("Start: ", datetime.fromtimestamp(time.time()).strftime("%A, %B %d, %Y %I:%M:%S %p"))
		print()


		show_completion = False

		# Keep track of the total time elapsed when training but not when skipping
		time_elapsed = 0

		while m >= m_min:
			while e <= e_max:
				print()
				print("----------------------------------------------------------------------------{}% ".format(round(cycle / total * 100, 3)))

				# If we want to show the etc
				if show_completion:


					# How many cycles are remaining
					cycles_remaining = total - cycle
					# The rate of change of time with respect to epochs
					rate = time_elapsed / trained
					# The estimated time remaining
					etr = rate * cycles_remaining

					completion = time.time() + etr

					print("Estimated Time of Grid Search Completion: ", datetime.fromtimestamp(completion).strftime("%A, %B %d, %Y %I:%M:%S %p"))

				# Otherwise just output N/A
				else:
					print("Estimated Time of Grid Search Completion: N/A")


				print()

				print("Mini Batch Size: ", m)
				print("Learning Rate: ", e)

				print()

				# Reset the network
				self.weights = default_parameters.weights
				self.biases = default_parameters.biases
				self.cost = []
				self.temp = []

				# Train it
				# Keep track of when we started training the thing
				start = time.time()
				self.SGD(training_data, epochs, m, e, update_frequency=epochs, show_graph=False)

				# If it was actually trained and not skipped
				if len(self.cost) > 1:
					# Add how long it took to train to how long training has taken
					time_elapsed += time.time() - start


					# If the last one was trained we can show an etc for the grid search
					show_completion = True
					trained += 1

				# If it was skipped then we don't want to find the etc
				else:
					show_completion = False

				# Store everything so we can look back at it later
				costs.append(self.cost[len(self.cost) - 1])
				es.append(e)
				ms.append(m)

				lowest_cost.lowest_cost = min(self.cost[len(self.cost) - 1], lowest_cost.lowest_cost)

				e = round(e + e_int, decs)
				cycle += 1


			e = e_min
			m -= m_int

		low = min(costs)
		low_i = costs.index(low)

		print()
		print("----------------------------------------------------------------------------100%")
		print("Time of Completion: ", datetime.fromtimestamp(time.time()).strftime("%A, %B %d, %Y %I:%M:%S %p"))
		print()
		print("Lowest Cost Found: ", low)
		print("Epochs: ", epochs)
		print("Mini Batch Size: ", ms[low_i])
		print("Learning Rate :", es[low_i])
		print()

		# Tell me that it is done
		send_message("Grid Search Completed", "hudsonhadley@yahoo.com")

		if low <= lowest_cost.lowest_cost:
			print("New Lowest Cost!")


		else:
			print("Lowest Cost: ", lowest_cost.lowest_cost)
			print("Epochs: ", lowest_cost.epochs)
			print("Mini Batch Size: ", lowest_cost.mini_batch_size)
			print("Learning Rate :", lowest_cost.eta)
			print("Difference: ", low - lowest_cost.lowest_cost)
			print()


def sigmoid(z):
	return 1 / (1 + np.exp(-z))


# Derivative of sigmoid
def sigmoid_prime(z):
	return sigmoid(z) * (1 - sigmoid(z))
