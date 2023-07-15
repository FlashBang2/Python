import random

def foo(x,y,z):
    return 6 * x ** 3 + 9 * y ** 2 + 90 * z - 25

def fitness(x,y,z):
    ans = foo(x,y,z)

    if ans == 0:
        return 99999
    else:
        return abs(1/ans)

#generate solutions
solutions = []
for s in range(1000):
    solutions.append((random.uniform(0,10000),
                      random.uniform(0,10000),
                      random.uniform(0,10000)))

for iteration in range(10000):
    rankedSolutions = []
    for solution in solutions:
        rankedSolutions.append( (fitness(solution[0],solution[1],solution[2]),solution) )
    rankedSolutions.sort()
    rankedSolutions.reverse()
    print ("=== Generation " + str(iteration) + " best solutions === ")
    print (rankedSolutions[0])

    if rankedSolutions[0][0] > 999:
        break

    bestSolutions = rankedSolutions[:100]

    elements = []
    for solution in bestSolutions:
        elements.append(solution[1][0])
        elements.append(solution[1][1])
        elements.append(solution[1][2])

    newGen = []
    for _ in range(1000):
        element1 = random.choice(elements) * random.uniform(0.99,1.01)
        element2 = random.choice(elements) * random.uniform(0.99,1.01)
        element3 = random.choice(elements) * random.uniform(0.99,1.01)
        
        newGen.append((element1,element2,element3))

    solutions = newGen


