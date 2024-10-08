from initialization1 import*
from mytest import *
# Crossover 
# Define the crossover probability
crossProb = 0.8
# Define mutation probablity
mutateProb = 0.5


def repairLost(chromosome,p1,p2):

    courseCred = dict(zip(cp['Course_Code'], cp['NOCW']))

    for day in chromosome:
            for slot in day:
                for sub in slot:
                    if sub!='' and sub in courseCred:
                        courseCred[sub]-=1
                        if courseCred[sub] == 0:
                            del courseCred[sub]
                    elif sub!='' and sub not in courseCred:
                        slot[slot.index(sub)] = ''
    
    for day in chromosome:
            for j in range(4):
                classes = [day[i][j] for i in range(6)]

                if classes[0]=='' and classes[1] in courseCred:
                    day[0][j] = classes[1]
                    courseCred[classes[1]]-=1
                    if courseCred[classes[1]]==0:
                        del courseCred[classes[1]]
                    
                if classes[1]=='' and classes[2] in courseCred:
                    day[1][j] = classes[2]
                    courseCred[classes[2]]-=1
                    if courseCred[classes[2]]==0:
                        del courseCred[classes[2]]

                if classes[1]=='' and classes[0] in courseCred:
                    day[1][j] = classes[0]
                    courseCred[classes[0]]-=1
                    if courseCred[classes[0]]==0:
                        del courseCred[classes[0]]
                    
                if classes[3]=='' and classes[4] in courseCred:
                    day[3][j] = classes[4]
                    courseCred[classes[4]]-=1
                    if courseCred[classes[4]]==0:
                        del courseCred[classes[4]]

                if classes[4]=='' and classes[5] in courseCred:
                    day[4][j] = classes[5]
                    courseCred[classes[5]]-=1
                    if courseCred[classes[5]]==0:
                        del courseCred[classes[5]]

                if classes[4]=='' and classes[3] in courseCred:
                    day[4][j] = classes[3]
                    courseCred[classes[3]]-=1
                    if courseCred[classes[3]]==0:
                        del courseCred[classes[3]]


    chromosome = weektosubs(chromosome)

    for i in range(120):
        if chromosome[i] == '':
            if p1[i] in courseCred and p2[i] == '':
                chromosome[i] = p1[i]
                courseCred[chromosome[i]] -= 1
            elif p1[i] == '' and p2[i] in courseCred:
                chromosome[i] = p2[i]
                courseCred[chromosome[i]] -= 1
            if chromosome[i]!='' and courseCred[chromosome[i]] == 0:
                del courseCred[chromosome[i]]

    chromosome = weektoslots(substoweek(chromosome))

    while courseCred!={}:

        rs = random.randint(0,29)
        rsub = random.choice(list(courseCred.keys()))
        rb = (subject_batch_ind_dict[rsub]-2)//2

        while chromosome[rs][rb]!='':
            rs = random.randint(0,29)
        chromosome[rs][rb] = rsub
        courseCred[rsub] -= 1
        if courseCred[rsub] == 0:
            del courseCred[rsub]
            
    chromosome = slotstoweek(chromosome)
    return chromosome


# We use random or non-random multipoint crossover here 
# Random multipoint : two parents are chosen to crossover by roullete wheel selection , then a random value N (no. of points 
# of crossover) ranging from 1 to 119 is chosen. Following which the multipoint crossover is done. 

# Non-Random multipoint : We can fix the no. of points of crossover to suitable value

#-------------------------------#-----------------------------------------#

def crossoverIW(pop):

    # assume the population is a list of individuals with corresponding fitness values
    population = [(indiv, fitness) for indiv, fitness in zip(pop, Fit_values)]

    # sort the population based on fitness values
    population.sort(key=lambda x: x[1], reverse=True)

    # shuffle the population list
    random.shuffle(population)

    # select the first two individuals in the shuffled list as parents
    parent1 = population[0][0]
    parent2 = population[1][0]

    # remove parents from the population
    pop.remove(parent1)
    pop.remove(parent2)

    parent1 = weektosubs(parent1)
    parent2 = weektosubs(parent2)


    # Check if crossover should be performed
    if random.random() <= crossProb:
    # Perform crossover
    # N Multipoint crossover 
        N = 10
        cpoints = sorted(random.sample(range(1, 120), N-1))

        # Add the endpoints of the chromosome to the list of crossover points
        cpoints = [0] + cpoints + [120]
        
        # Extract segments from parents and create offspring
        offspring1 = []
        offspring2 = []
        for i in range(len(cpoints)-1):
            if i % 2 == 0:
                seg_length = cpoints[i+1] - cpoints[i]
                if len(offspring1) + seg_length <= 120:
                    offspring1 += parent1[cpoints[i]:cpoints[i+1]]
                else:
                    offspring1 += parent1[cpoints[i]:cpoints[i]+(120-len(offspring1))]
                seg_length = cpoints[i+1] - cpoints[i]
                if len(offspring2) + seg_length <= 120:
                    offspring2 += parent2[cpoints[i]:cpoints[i+1]]
                else:
                    offspring2 += parent2[cpoints[i]:cpoints[i]+(120-len(offspring2))]
            else:
                seg_length = cpoints[i+1] - cpoints[i]
                if len(offspring1) + seg_length <= 120:
                    offspring1 += parent2[cpoints[i]:cpoints[i+1]]
                else:
                    offspring1 += parent2[cpoints[i]:cpoints[i]+(120-len(offspring1))]
                seg_length = cpoints[i+1] - cpoints[i]
                if len(offspring2) + seg_length <= 120:
                    offspring2 += parent1[cpoints[i]:cpoints[i+1]]
                else:
                    offspring2 += parent1[cpoints[i]:cpoints[i]+(120-len(offspring2))]
               
        offspring1 = substoweek(offspring1)
        offspring2 = substoweek(offspring2)
        
        offspring1 = repairLost(offspring1,parent1,parent2)
        offspring2 = repairLost(offspring2,parent1,parent2)

        rn = random.random()
        if rn<=mutateProb:
            return mutationDay(offspring1,offspring2)
            # o1,o2 = mutationSlot(offspring1,offspring2) 
            # return mutationDay(o1,o2)
        else:
            return [offspring1,offspring2]
 
    
    else:
        return []

#---------------------------#--------------------------------------------#    

def crossoverSW(pop):

    # assume the population is a list of individuals with corresponding fitness values
    population = [(indiv, fitness) for indiv, fitness in zip(pop, Fit_values)]

    # select the first parent
    parent1 = random.choice(population)[0]
    # select the second parent
    parent2 = random.choice(population)[0]

    if parent1==parent2:
        pop.remove(parent1)
    else:
        pop.remove(parent1)
        pop.remove(parent2)

    parent1 = weektoslots(parent1)
    parent2 = weektoslots(parent2)

    # Check if crossover should be performed
    if random.random() <= crossProb:
        N = 5
        cpoints = sorted(random.sample(range(1, 30), N-1))

        # Add the endpoints of the chromosome to the list of crossover points
        cpoints = [0] + cpoints + [30]
        
        # Extract segments from parents and create offspring
        offspring1 = []
        offspring2 = []

        for i in range(0,len(cpoints)-1):
            if (i%2)==0:
                for j in range(cpoints[i],cpoints[i+1]):
                    offspring1.append(parent1[j])
            else:
                for j in range(cpoints[i],cpoints[i+1]):
                    offspring1.append(parent2[j])

        for i in range(0,len(cpoints)-1):
            if (i%2)==0:
                for j in range(cpoints[i],cpoints[i+1]):
                    offspring2.append(parent2[j])
            else:
                for j in range(cpoints[i],cpoints[i+1]):
                    offspring2.append(parent1[j])


        parent1 = slotstoweek(parent1)
        parent2 = slotstoweek(parent2)
        parent1 = weektosubs(parent1)
        parent2 = weektosubs(parent2)
        offspring1 = slotstoweek(offspring1)
        offspring2 = slotstoweek(offspring2)

        offspring1 = repairLost(offspring1,parent1,parent2)
        offspring2 = repairLost(offspring2,parent1,parent2)

        rn = random.random()
        if rn<=mutateProb:
            return mutationDay(offspring1,offspring2) 
            
        else:
            return [offspring1,offspring2]
    else:
        return []

#-------------------------------#-----------------------------------------#

def uniformCrossover(pop):

    # assume the population is a list of individuals with corresponding fitness values
    population = [(indiv, fitness) for indiv, fitness in zip(pop, Fit_values)]

    # select the first parent
    parent1 = random.choice(population)[0]
    # select the second parent
    while True:
        parent2 = random.choice(population)[0]
        if parent2 != parent1:
            break
        
    pop.remove(parent1)
    pop.remove(parent2)

    parent1 = weektosubs(parent1)
    parent2 = weektosubs(parent2)


    # Check if crossover should be performed
    if random.random() <= crossProb:
        offspring1 = []
        offspring2 = []

        for i in range(120):
            rn = random.random()
            if rn<=0.5:
                offspring1.append(parent1[i])
                offspring2.append(parent2[i])
            else:
                offspring1.append(parent2[i])
                offspring2.append(parent1[i])

        offspring1 = substoweek(offspring1)
        offspring2 = substoweek(offspring2)
        
        offspring1 = repairLost(offspring1,parent1,parent2)
        offspring2 = repairLost(offspring2,parent1,parent2)
        
        
        
        rn = random.random()
        if rn<=mutateProb:
            o1,o2 = mutationDay(offspring1,offspring2) 
            return mutationSlot(o1,o2)
        else:
            return [offspring1,offspring2]
    
    else:
        return []
    
#-------------------------------#-----------------------------------------#

# def uniformCrossover(pop):
#     # calculate the total fitness of the population
#     total_fitness = sum(fitness for fitness in pop.values())

#     # select the first parent
#     rand_num1 = random.uniform(0, total_fitness)
#     fit_sum = 0
#     parent1 = None
#     for chromosome, fitness in pop.items():
#         fit_sum += fitness
#         if fit_sum >= rand_num1:
#             parent1 = chromosome
#             break

#     # select the second parent
#     while True:
#         rand_num2 = random.uniform(0, total_fitness)
#         fit_sum = 0
#         parent2 = None
#         for chromosome, fitness in pop.items():
#             fit_sum += fitness
#             if fit_sum >= rand_num2 and chromosome != parent1:
#                 parent2 = chromosome
#                 break
#         if parent2:
#             break

        
#     del pop[parent1]
#     del pop[parent2]


#     # Check if crossover should be performed
#     if random.random() <= crossProb:
#         offspring1 = []
#         offspring2 = []

#         for i in range(120):
#             rn = random.random()
#             if rn<=0.5:
#                 offspring1.append(parent1[i])
#                 offspring2.append(parent2[i])
#             else:
#                 offspring1.append(parent2[i])
#                 offspring2.append(parent1[i])

#         offspring1 = substoweek(offspring1)
#         offspring2 = substoweek(offspring2)
        
#         offspring1 = repairLost(offspring1,parent1,parent2)
#         offspring2 = repairLost(offspring2,parent1,parent2)
        
#         offspring1 = weektosubs(offspring1)
#         offspring2 = weektosubs(offspring2)
        
#         rn = random.random()
#         if rn<=mutateProb:
#             return mutationDay(offspring1,offspring2) 
#         else:
#             return [offspring1,offspring2]
    
#     else:
#         return []




#----------------------------------------------------------------#

# Mutation 

def mutationSlot(chromosome1,chromosome2):

    chromosome1 = weektoslots(chromosome1)
    chromosome2 = weektoslots(chromosome2)
    n = len(chromosome1)

    rn1 = random.randint(0,n-1)
    rn2 = random.randint(0,n-1)
    while rn1==rn2:
        rn2 = random.randint(0,n-1)
    chromosome1[rn1],chromosome1[rn2] = chromosome1[rn2],chromosome1[rn1]

    rn1 = random.randint(0,n-1)
    rn2 = random.randint(0,n-1)
    while rn1==rn2:
        rn2 = random.randint(0,n-1)
    chromosome2[rn1],chromosome2[rn2] = chromosome2[rn2],chromosome2[rn1]
    repairLost
    return [slotstoweek(chromosome1),slotstoweek(chromosome2)]

#---------------------------------------------------#
def mutationDay(chromosome1,chromosome2):
    n = len(chromosome1)

    rn1 = random.randint(0,n//2)
    rn2 = random.randint(n//2,n-1)
    chromosome1[rn1],chromosome1[rn2] = chromosome1[rn2],chromosome1[rn1]

    rn1 = random.randint(0,n//2)
    rn2 = random.randint(n//2,n-1)
    chromosome2[rn1],chromosome2[rn2] = chromosome2[rn2],chromosome2[rn1]

    return [chromosome1,chromosome2]

def mutationSlotShuffle(chromosome1,chromosome2):
    return 
def mutationDayShuffle(chromosome1,chromosome2):
    return