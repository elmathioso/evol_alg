import string
import random
import os

populationSize = 100
goal = 'thisismyhandle'
geneSize = len(goal)
population = []
fitness = []
matingProbability = []
matingPool = []
generation = 0
mutationRate = 0.01 #0.1%
minimumFitness = 0.05
deathRatio = 0.1

def evaluateFitness(var1, var2):
	count = 0
	distance = []
	for i in range(0, len(var1)-1):
		distance.append(abs(ord(var1[i]) - ord(var2[i])))
		if (var1[i] == var2[i]):
			count = count+1
			
			#print(ord(var1[i]))
			#print(ord(var2[i]))
	#if (count > 0):
		#look at how far characters are from target
		#print(120 - sum(distance))
		
		#return (max(40 - max(distance), 0))
	#else:
		#return 0
	return count*count*count*count

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
	
def crossover(parentA, parentB):
	slice = random.randint(1, len(parentA))
	order = random.random()
	
	#print(parentA, parentB, slice, len(parentA))
	
	if (order<0.5):
		child = parentA[0: slice] + parentB[slice: len(parentA)]
	else:	
		child = parentB[0: slice] + parentA[slice: len(parentA)]
	
	return child
	
	
def mutate(child, mutationRate):
	
	adult = ''
	for i in range(len(child)):
		#print(i)
		if (random.random() < mutationRate):
			adult = adult + (random.choice(string.ascii_lowercase))
			
			#if (random.random() < 0.5):
			#	adult = adult + chr(min(ord(child[i]) + 1, ord('z')))
			#else:
			#	adult = adult + chr(max(ord(child[i]) - 1, ord('a')))
			
			
#			print("Mutate!")
		else:
			adult = adult + child[i]
	#print(adult)
	return adult
	
			
def killWeakest(probability):

	localProb = probability
	
	for i in range(round(populationSize*deathRatio), 0):

	
		if (min(localProb) != max(localProb)):
			minimum = min(localProb)
			localProb[localProb.index(minimum)] = 0
		
	return localProb
	


random.seed()
# Initialize	population
for i in range(populationSize):
	population.append(''.join(random.choice(string.ascii_lowercase) for _ in range(geneSize)))
	fitness.append(int(0))

fitness = evaluateFitnesses(population, goal)
matingProbability = calculateMatingProbability(fitness)
matingPool = generateMatingPool(matingProbability, populationSize)

print(matingProbability)

breakLoop = False
while  (generation < 100000) and (breakLoop == False):
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
	
	fitness = evaluateFitnesses(population, goal)
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
	
	for i in range(populationSize):
		if (population[i] == goal):
			breakLoop = True

print(generation)
print(population)	