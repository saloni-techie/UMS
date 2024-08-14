import itertools
from initialization1 import *
# No Faculty should have been assigned two different classes at same time ( in same slot of day )
# No Lab should be assigned to two different batches at same time

# We count the number of conflicts / Violations made in the chromosome and add 1/1+c score to the chromosome's final eval score
# if c is 0 the max value of 1 is added 



    

def returnFit(x):
    return sum([1/(1+i) for i in x])

def separateChromosome(chromosome):
    sem2 = {}
    sem4 = {}
    sem6 = {}
    sem8 = {}
    dayMap = {1:"Mon", 2:"Tue" , 3:"Wed" , 4:"Thurs" , 5:"Fri"}
    for i in range(len(chromosome)):
        
        sem2[dayMap[i+1]] = []
        sem4[dayMap[i+1]] = []
        sem6[dayMap[i+1]] = []
        sem8[dayMap[i+1]] = []
        for  slot in chromosome[i]:
            sem2[dayMap[i+1]].append(slot[0])
            sem4[dayMap[i+1]].append(slot[1])
            sem6[dayMap[i+1]].append(slot[2])
            sem8[dayMap[i+1]].append(slot[3])
    return sem2,sem4,sem6,sem8


def fitnessFunction(chromosome):
    
    conflicts = []
    fitness_value = 0
    option_list = [1,2,3,4,5,6,7,8,9]
    
    
    i = 0
    
    while i < len(option_list):
        
        if option_list[i] == 1:
            fac_Clash(chromosome,conflicts)
        elif option_list[i] == 2:
            lab_Clash(chromosome,conflicts)
        elif option_list[i] == 3:
            Blank_class(chromosome,conflicts)
        elif option_list[i] == 4:
            Repeated_class(chromosome,conflicts)
        elif option_list[i] == 5:
            lab_second_half(chromosome,conflicts)
        elif option_list[i] == 6:
            nsame_cla_be_af_lunch(chromosome,conflicts)
        elif option_list[i] == 7:
            slot1 = 0
            set_slot_null(chromosome,slot1) 
            nfirst_slot(chromosome,conflicts,slot1)
        elif option_list[i] == 8:
            Break_class(chromosome,conflicts)
        elif option_list[i] == 9:
            hrtwo_conti_crethree(chromosome,conflicts)
        i += 1
        
    fitness_value += returnFit(conflicts)
    return fitness_value

        
        
# def constraint1(week,conflicts):
#      # 1 No faculty should have two classes alloted in same slot of time
#         # 1 No two batches should have same lab alloted to them in same slot of time
#         conflicts.append(0)
#         for day in week:
#             for slot in day:
#                 for sub, osub in itertools.combinations(slot, 2):
#                     if sub and osub:
#                         # Faculty clash check
#                         if sub != osub and subject_teacher_dict[sub] == subject_teacher_dict[osub]:
#                             conflicts[-1] += 1
#                         # Lab clash check
#                         if sub != osub and course_type_dict[sub] == 'L' and course_type_dict[osub] == 'L':
#                             if lab_alloted[subject_batch_ind_dict[sub]] == lab_alloted[subject_batch_ind_dict[osub]]:
#                                 conflicts[-1] += 1  

def set_slot_null(week,slot1):
    
    for day in week:
        day[slot1] = ['','','','']

def fac_Clash(week,conflicts):
    conflicts.append(0)
    for day in week:
            for slot in day:
                for sub, osub in itertools.combinations(slot, 2):
                    if sub and osub:
                        # Faculty clash check
                        if sub != osub and subject_teacher_dict[sub] == subject_teacher_dict[osub]:
                            conflicts[-1] += 1
             
def lab_Clash(week,conflicts):
    conflicts.append(0)
    for day in week:
            for slot in day:
                for sub, osub in itertools.combinations(slot, 2):
                    if sub and osub:
                    #Lab clash check
                       if sub != osub and course_type_dict[sub] == 'L' and course_type_dict[osub] == 'L':
                            if lab_alloted[subject_batch_ind_dict[sub]] == lab_alloted[subject_batch_ind_dict[osub]]:
                                conflicts[-1] += 1  

        
            
    
    
# def constrtraint2(week,conflicts):
#     conflicts.append(0) # 2 Blank class
#     conflicts.append(0) # 3 Repeated class
#     conflicts.append(0) # 4 lab second half
#     for day in week:
#             for j in range(4):
#                 day_classes = [day[i][j] for i in range(6)]

#                 # Blank class conflict 
#                 blank_class = day_classes.count('')
#                 if blank_class == 0:
#                     conflicts[-3] += 0.1

#                 for sub in set(day_classes):
#                     if sub != '':
#                         tc = day_classes.count(sub)
#                         c = 0
#                         lc = 0
#                         for i in range(len(day_classes)):
#                             if day_classes[i] == sub:
#                                 c += 1
#                             else:
#                                 lc = max(lc, c)
#                                 c = 0
#                         lc = max(lc, c)
 
#                         if lc == 1:
#                             conflicts[-2] += (tc - lc)
#                         else:
#                             conflicts[-2] += (tc - lc) + (lc - 2)

#                 # Lab classes should be conducted in second half
#                 for i in range(3):
#                     if day_classes[i]!='' and course_type_dict[day_classes[i]]=='L':
#                         conflicts[-1] += 0.2

        


   
  
# #Blank class   
def Blank_class(week,conflicts):
    
    conflicts.append(0)
    for day in week:
            for j in range(4):
                day_classes = [day[i][j] for i in range(6)]

                # Blank class conflict 
                blank_class = day_classes.count('')
                if blank_class == 0:
                    conflicts[-3] += 0.1
                

    

# 3 Repeated class
def Repeated_class(week,conflicts):
    
    conflicts.append(0) 
    for day in week:
            for j in range(4):
                day_classes = [day[i][j] for i in range(6)]
                for sub in set(day_classes):
                    if sub != '':
                        tc = day_classes.count(sub)
                        c = 0
                        lc = 0
                        for i in range(len(day_classes)):
                            if day_classes[i] == sub:
                                c += 1
                            else:
                                lc = max(lc, c)
                                c = 0
                        lc = max(lc, c)
 
                        if lc == 1:
                            conflicts[-2] += (tc - lc)
                        else:
                            conflicts[-2] += (tc - lc) + (lc - 2)
 

                     
# Lab classes should be conducted in second half
def lab_second_half(week,conflicts):
    
    conflicts.append(0) # 4 lab second half
    for day in week:
        for j in range(4):
            day_classes = [day[i][j] for i in range(6)]
            
            for i in range(3):
                if day_classes[i]!='' and course_type_dict[day_classes[i]]=='L':
                    conflicts[-1] += 0.2
 

# 5 Class after lunch and before lunch should not be same  
def nsame_cla_be_af_lunch(week,conflicts):
                             
        conflicts.append(0)
        for day in week:
            if set(day[2]).intersection(set(day[3]))!=set(): 
                conflicts[-1] += 1
        
    
    
# 6 Try not to fill the first slot of each day ( it is very early in morning )       
def nfirst_slot(week,conflicts,slot1):
    
    for day in week:
        
        day[slot1] == ['','','','']
            
            # conflicts[-3] += 0.1
        
        
        
            
 # 7 Class hour discontinuity : breakage between two classes
 
def Break_class(week,conflicts):
    
        conflicts.append(0)
        for day in week:
            conflicts_day = []
            for j in range(4):
                cc = sum([1 for i in range(6) if day[i][j] != ''])
                conflicts_day.append(cc)
            if max(conflicts_day) > 1:
                conflicts[-1] += 0.5
        
   
# 8 Try to have atleast one 2 hours continous class of a subject with credit >= 3

def hrtwo_conti_crethree(week,conflicts):
        conflicts.append(0)
        for day in week:
            for j in range(4):
                classes = []
                for i in range(6):
                    classes.append(day[i][j])
                cool_subjects = {}
                if classes[0]!='' and classes[0] == classes[1]:
                    if classes[0] in subject_credithour_dict:
                        cool_subjects[classes[0]] = 1
                if classes[1]!='' and classes[2] == classes[1]:
                    if classes[0] in subject_credithour_dict:
                        cool_subjects[classes[0]] = 1
                if classes[3]!='' and classes[4] == classes[1]:
                    if classes[0] in subject_credithour_dict:
                        cool_subjects[classes[0]] = 1
                if classes[4]!='' and classes[5] == classes[1]:
                    if classes[0] in subject_credithour_dict:
                        cool_subjects[classes[0]] = 1

                conflicts[-1]+= (len(subject_credithour_dict)-len(cool_subjects))/10
                
                
       
# Fitness Calculations
Fit_values = []
for chromosome in pop:
    Fit_values.append(fitnessFunction(chromosome))           
