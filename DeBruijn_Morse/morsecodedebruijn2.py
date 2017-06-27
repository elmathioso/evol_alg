#------------------------------------
#       Morse Code Optimizer        -
#       Mathieu Lemay, 2015         -
#------------------------------------
# This program generates a Morse code string
# which contains at one place or another all of the 
# characters present in the CODE list.
#
# It is inspired by the De Bruijn sequence approach:
# https://en.wikipedia.org/wiki/De_Bruijn_sequence
# Samy Kamkar's explanation: https://youtu.be/iSSRaIU9_Vc?t=259
# Instead of optimizing the sequence, it arrived at 32 bits, which is 
# storable as a single uint32 variable, or 4 uint8 bytes.

# It generates a lookup table, where each byte contains 
# information about the position of the character in the master
# string, and the length.  

# Therefore, the total space required for the lookup table and the master
# string is 26 bytes (alpha) + 10 bytes (numbers) + 4 bytes (master string)
# which equals 40 bytes.

import math 
import random
import os
import string

#from http://code.activestate.com/recipes/578407-simple-morse-code-translator-in-python/
CODE = {'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
     	'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',
        
        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.' 
        }


populationSize = 100
#geneSize = len(goal)
population = []
fitness = []
matingProbability = []
matingPool = []
generation = 0			# starting generation number°
maxGenerations = 500
mutationRate = 0.01 	#0.1%
minimumFitness = 0.05
deathRatio = 0.1	# cull the bottom 10%
fitnessPower = 3	# how many times to multiply the fitness distance with itself; the greater the number, the more the fitter elements stand out
		

		
#starting alphabet - not optimized, but functional
sequence = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"		


# Slide over previous string to see if there is a match;
#  if not, append partially or completely
def induced_fitting(growing_string, character):
	
	#check if string already exists
	if character not in growing_string:
		
		# for every character
		for i in range(len(character), 0, -1):
			
			# check if string can be fitted partially on the tail
			if growing_string.endswith(character[:i]):

				#partial tail found.  Add remainder and exit.
				remainder = character[i-len(character):]
				growing_string = growing_string + remainder
				break
				
		else: # "else" related to the FOR loop - no match found.
			#add end to master string
			growing_string = growing_string + character
			
	return growing_string
	
	
	
# Match every character to the master string.  Either find a match in the previous 
# string, partially append, or completely append.
def evaluate_alphabet(alphabet):
	# print("Alphabet: ", alphabet)
	# start off the sequence
	pseudo_debruijn_string = induced_fitting(CODE[alphabet[0]], CODE[alphabet[1]])
	
	# go over every character
	for i in range(1, len(alphabet)):

		pseudo_debruijn_string = induced_fitting(pseudo_debruijn_string, CODE[alphabet[i]])
	
	# print(pseudo_debruijn_string) # print final string
	return pseudo_debruijn_string
	
	
	
# convert the position and length to a single byte
def translate_to_binary(master_string, character):
	# find position of character in string
	position = master_string.find(character)

	#convert length to binary
	length = len(character)
	
	#convert 5 first bits to position(xxxxx---), 3 last bits to length (-----xxx)
	return (format((position * 2**3 + length), '#04x')).upper()

	
	
# return morse character from combination byte
def translate_to_morse(master_string, character):

	char_position = math.floor(int(character, 16) / 2**3)
	char_length = int(character, 16) % 2**3
	for i in range(char_length):
		print(master_string[char_position + i], end="")
	print()

	
# Measure the length of the string.  The shorter the string, the better.
def evaluateFitness(var1, var2_length):
	distance = var2_length - len(evaluate_alphabet(var1))
	
	# if distance is greater than starting length, make it 0
	if (distance != abs(distance)):
		distance = 0
	
	return distance**fitnessPower

def evaluateFitnesses(population, goal):
	fitness = []
	for i in range(populationSize):
		fitness.append(evaluateFitness(population[i], goal))
		
		#give everyone a chance
		if (fitness[i] == 0):
			fitness[i] = 0.0001
	return fitness

def calculateMatingProbability(fitness):
	for i in range(populationSize):
		#print(i, "#")
		matingProbability.append(fitness[i] / sum(fitness))
	return matingProbability

def generateMatingPool(matingProbability, populationSize):
	counter = 0
	total = 0
	matingPool = []
	while total < populationSize * 10:

		if (random.random() <= matingProbability[counter]):
			matingPool.append(counter)
			total = total + 1

		counter = counter + 1
		counter = counter % populationSize

	return matingPool
	
# how do parents merge genes?  interleave + remove duplicates	
def crossover(parentA, parentB):
	# slice = random.randint(1, len(parentA))
	# order = random.random()
	
	# #print(parentA, parentB, slice, len(parentA))
	
	# if (order<0.5):
		# child = parentA[0: slice] + parentB[slice: len(parentA)]
	# else:	
		# child = parentB[0: slice] + parentA[slice: len(parentA)]
	
	# return child
	childDoubleGenes = ''
	for i in range(len(parentA)):
		childDoubleGenes += parentA[i]
		childDoubleGenes += parentB[i]
	
	# foo = 'mppmt'
	childGenes = ''.join(sorted(set(childDoubleGenes), key=childDoubleGenes.index))

	return childGenes
	
	
# switch two letters
def mutate(child, mutationRate):
	
	adult = ''
	for i in range(len(child)):
		#print(i)
		if (random.random() < mutationRate):
			
			i = random.randint(0, len(child) - 1)
			j = random.randint(0, len(child) - 1)
			lst = list(child)
			lst[i], lst[j] = lst[j], lst[i]
			adult = ''.join(lst)
			
			
			#if (random.random() < 0.5):
			#	adult = adult + chr(min(ord(child[i]) + 1, ord('z')))
			#else:
			#	adult = adult + chr(max(ord(child[i]) - 1, ord('a')))
			
			
#			print("Mutate!")
		else:
			adult = child
	#print(adult)
	return adult
	
			
def killWeakest(probability):

	localProb = probability
	
	for i in range(round(populationSize*deathRatio), 0):

	
		if (min(localProb) != max(localProb)):
			minimum = min(localProb)
			localProb[localProb.index(minimum)] = 0
		
	return localProb
	
def scrambleAlphabet(alphabet):
	word = list(alphabet)
	random.shuffle(word)
	return ''.join(word)
	
# ------------------------------------	
# program start
# ------------------------------------	

print("#####################################")
print("#       Morse Code Optimizer        #")
print("#       Mathieu Lemay, 2015         #")
print("#####################################")
print()	

# calculate original length, 1 bytes per dot/dash
total_starting_length = 0
for key, value in list(CODE.items()):
	total_starting_length = total_starting_length + len(value)
print("Total starting length:", total_starting_length, "bytes")


# generate master Morse list based on deBruijn alogrithm
initial_master_morse = evaluate_alphabet(sequence)

# get number of bytes required to represent master sequence
master_morse_length = math.ceil(len(initial_master_morse) / 8)
print("Master Morse sequence:", initial_master_morse, "(", len(initial_master_morse), "bits long)\n")
master_morse_binary = initial_master_morse.replace(".", "0")
master_morse_binary = master_morse_binary.replace("-", "1")
master_morse_binary = int(master_morse_binary, 2)
master_morse_binary = (format(master_morse_binary, '#04x')).upper()
print("Master Morse in hex: ", master_morse_binary)
print("\n######################\n")

#generate lookup table
BINCODE = {}
print("Generating lookup table:")
for char in sequence:
	BINCODE[char] = translate_to_binary(initial_master_morse, CODE[char])
	print(char, ":  ", translate_to_binary(initial_master_morse, CODE[char]))
print("\n######################\n")


# test sequence
hello = "HELLOWORLD"
print("Printing \"HELLOWORLD\":")
for i in range(len(hello)):

	#go over every character and print Morse sequence
	translate_to_morse(initial_master_morse, BINCODE[hello[i]])

print("\n######################\n")

	
# evaluate success:
new_length = len(BINCODE) + master_morse_length
print("Original memory cost: ", total_starting_length, " bytes")
print("New memory cost: ", new_length, " bytes")
print("Memory use reduction: ", round(((1 - (new_length / total_starting_length)) * 100), 1), "%")

os.system("pause")


# ##########################################################
# start of algorithm to resort alphabet
# ##########################################################


random.seed()
# Initialize population: scramble all of the sequences
for i in range(populationSize):
	population.append(scrambleAlphabet( sequence ))
	fitness.append(int(0))

print(population)

initial_length = len(initial_master_morse)
print(initial_length)
fitness = evaluateFitnesses(population, initial_length)
print(fitness)

matingProbability = calculateMatingProbability(fitness)
matingPool = generateMatingPool(matingProbability, populationSize)

print(matingProbability)

breakLoop = False
while  (generation < maxGenerations) and (breakLoop == False):
	random.seed()

	#evaluate fitness

	child = []

	#print(len(matingPool))

	for i in range(populationSize):
		parentA = random.randint(0, populationSize*10 - 1 )
		parentB = random.randint(0, populationSize*10 - 1 )
		#print(matingPool[parentA], matingPool[parentB])
		child.append(crossover(population[matingPool[parentA]], population[matingPool[parentB]]))

	adult = []
	for i in range(populationSize):
		adult.append(mutate(child[i], mutationRate))
		
		
	population = adult
	generation = generation + 1

	#print(child, population[0], population[1])
		
	#print(matingProbability[0], matingPool.count(0))
	#print(sum(fitness))

	#print(population[0], evaluateFitness(population[0], goal))
	
	#population = []
	fitness = []
	matingProbability = []
	matingPool = []
	
	fitness = evaluateFitnesses(population, initial_length)
	matingProbability = calculateMatingProbability(fitness)
	matingProbability = killWeakest(matingProbability)
	
	matingPool = generateMatingPool(matingProbability, populationSize)

	#print(matingProbability)
	#os.system("pause")
	
	#print(child)
	#print(adult)
	#os.system("pause")
	
	if (generation % 10 == 0):
		print("Generation:", generation, " Fitness:", max(fitness), population[0], population[1])
		print("Max Fitness:", max(fitness), ", Min Fitness:", min(fitness))
		print("Initial Length: ", initial_length, ", Present length:", len(evaluate_alphabet(population[0])), ", String:", evaluate_alphabet(population[0]))
	
	# for i in range(populationSize):
		# if (population[i] == goal):
			# breakLoop = True


print(generation)
print(population)	
