# Omer Khan
# Project 2
# CS 461 - Brian Hare

import random, copy
from Classes import *
from math import ceil, log2
import math

# initialize a list of courses with name and size
Course.courses = [Course("CS101A", 40),
                  Course("CS101B", 25),
                  Course("CS201A", 30),
                  Course("CS201B", 30),
                  Course("CS191A", 60),
                  Course("CS191B", 20),
                  Course("CS291A", 20),
                  Course("CS291B", 40),
                  Course("CS303", 50),
                  Course("CS341", 40),
                  Course("CS449", 55),
                  Course("CS461", 40)]

# initialize a list of professors and the course they teach
Professor.professors = [Professor("Hare", "CS101A"),
                        Professor("Hare", "CS101B"),
                        Professor("Hare", "CS201A"),
                        Professor("Hare", "CS201B"),
                        Professor("Hare", "CS291A"),
                        Professor("Hare", "CS291B"),
                        Professor("Hare", "CS303"),
                        Professor("Hare", "CS449"),
                        Professor("Hare", "CS461"),
                        Professor("Bingham", "CS101A"),
                        Professor("Bingham", "CS101B"),
                        Professor("Bingham", "CS201A"),
                        Professor("Bingham", "CS201B"),
                        Professor("Bingham", "CS191A"),
                        Professor("Bingham", "CS191B"),
                        Professor("Bingham", "CS291A"),
                        Professor("Bingham", "CS291B"),
                        Professor("Bingham", "CS449"),
                        Professor("Kuhail", "CS303"),
                        Professor("Kuhail", "CS341"),
                        Professor("Mitchell", "CS191A"),
                        Professor("Mitchell", "CS191B"),
                        Professor("Mitchell", "CS291A"),
                        Professor("Mitchell", "CS291B"),
                        Professor("Mitchell", "CS303"),
                        Professor("Mitchell", "CS341"),
                        Professor("Rao", "CS291A"),
                        Professor("Rao", "CS291B"),
                        Professor("Rao", "CS303"),
                        Professor("Rao", "CS341"),
                        Professor("Rao", "CS461"),
                        Professor("Staff", "CS101A"),
                        Professor("Staff", "CS101B"),
                        Professor("Staff", "CS201A"),
                        Professor("Staff", "CS201B"),
                        Professor("Staff", "CS191A"),
                        Professor("Staff", "CS191B"),
                        Professor("Staff", "CS291A"),
                        Professor("Staff", "CS291B"),
                        Professor("Staff", "CS303"),
                        Professor("Staff", "CS341"),
                        Professor("Staff", "CS449"),
                        Professor("Staff", "CS461")]

# initialize a list of locations and seats available for that classroom
Location.locations = [Location("Haag 301", 70),
                      Location("Haag 206", 30),
                      Location("Royall 204", 70),
                      Location("Katz 209", 50),
                      Location("Flarsheim 310", 80),
                      Location("Flarsheim 260", 25),
                      Location("Bloch 0009", 30)]

# initialize a list of available class timings (in military time)
Time.timing = [Time("10:00", "10:50", "Mon"),
               Time("11:00", "11:50", "Mon"),
               Time("12:00", "12:50", "Mon"),
               Time("13:00", "13:50", "Mon"),
               Time("14:00", "14:50", "Mon"),
               Time("15:00", "15:50", "Mon"),
               Time("16:00", "16:50", "Mon"),
               Time("10:00", "10:50", "Wed"),
               Time("11:00", "11:50", "Wed"),
               Time("12:00", "12:50", "Wed"),
               Time("13:00", "13:50", "Wed"),
               Time("14:00", "14:50", "Wed"),
               Time("15:00", "15:50", "Wed"),
               Time("16:00", "16:50", "Wed"),
               Time("10:00", "10:50", "Fri"),
               Time("11:00", "11:50", "Fri"),
               Time("12:00", "12:50", "Fri"),
               Time("13:00", "13:50", "Fri"),
               Time("14:00", "14:50", "Fri"),
               Time("15:00", "15:50", "Fri"),
               Time("16:00", "16:50", "Fri")]

# TODO
# 0.  Running Simplified Class Scheduling - Done
# 0.5 Problem Instance to Binary String - Done
# 1.  Multiple days - Done
# 2.  Class Size - Done
# 2.25 Check Selection Function - Done
# 2.5 One group can attend only one class at a time - Done
# 3.  Multiple courses - Done
# 4.  Lab - Done

# cpg = ["000000", "010001", "100100", "111010"] # course, professor, student group pair
# lts = ["00", "01"] # lecture theatres
# slots = ["00", "01"] # time slots

max_score = None

cpg = []
lts = []
slots = []
bits_needed_backup_store = {}  # to improve performance


def bits_needed(x):
    global bits_needed_backup_store
    r = bits_needed_backup_store.get(id(x))
    if r is None:
        r = int(ceil(log2(len(x))))
        bits_needed_backup_store[id(x)] = r
    # return max from r or 1 (one)
    return max(r, 1)


def join_cpg_pair(_cpg):
    res = []
    for i in range(0, len(_cpg), 3):
        res.append(_cpg[i] + _cpg[i + 1] + _cpg[i + 2])
    return res


def convert_input_to_bin():
    global cpg, lts, slots, max_score

    # cpg list creates a list[] of element index number from the searched courses and professors 
    cpg = [Course.find("CS101A"), Professor.find("mutaqi"),
           Course.find("CS101B"), Professor.find("mutaqi"),
           Course.find("CS201A"), Professor.find("khalid"),
           Course.find("CS201B"), Professor.find("basit"),
           Course.find("CS191A"), Professor.find("mutaqi"),
           Course.find("CS191B"), Professor.find("zafar"),
           Course.find("CS291A"), Professor.find("basit"),
           Course.find("CS291B"), Professor.find("basit"),
           Course.find("CS303"), Professor.find("mutaqi"),
           Course.find("CS341"), Professor.find("zafar"),
           Course.find("CS449"), Professor.find("basit"),
           Course.find("CS461"), Professor.find("basit")]

    # iterate over the entire cpg list[]
    for _c in range(len(cpg)):
        if _c % 3:  # Course    
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Course.courses), '0')
        elif _c % 3 == 1:  # Professor
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Professor.professors), '0')
        else:  # Group
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Course.courses), '0')

    cpg = join_cpg_pair(cpg)
    for r in range(len(Location.locations)):
        lts.append((bin(r)[2:]).rjust(bits_needed(Location.locations), '0'))

    for t in range(len(Time.timing)):
        slots.append((bin(t)[2:]).rjust(bits_needed(Time.timing), '0'))

    # print(cpg)
    max_score = (len(cpg) - 1) * 3 + len(cpg) * 3


def course_bits(chromosome):
    i = 0

    return chromosome[i:i + bits_needed(Course.courses)]


def professor_bits(chromosome):
    i = bits_needed(Course.courses)

    return chromosome[i: i + bits_needed(Professor.professors)]


def group_bits(chromosome):
    i = bits_needed(Course.courses) + bits_needed(Professor.professors)

    return chromosome[i:i + bits_needed(Group.groups)]


def slot_bits(chromosome):
    i = bits_needed(Course.courses) + bits_needed(Professor.professors) + \
        bits_needed(Group.groups)

    return chromosome[i:i + bits_needed(Slot.slots)]


def lt_bits(chromosome):
    i = bits_needed(Course.courses) + bits_needed(Professor.professors) + \
        bits_needed(Group.groups) + bits_needed(Slot.slots)

    return chromosome[i: i + bits_needed(Room.rooms)]


def slot_clash(a, b):
    if slot_bits(a) == slot_bits(b):
        return 1
    return 0


# checks that a faculty member teaches only one course at a time.
def faculty_member_one_class(chromosome):
    scores = 0
    for i in range(len(chromosome) - 1):  # select one cpg pair
        clash = False
        for j in range(i + 1, len(chromosome)):  # check it with all other cpg pairs
            if slot_clash(chromosome[i], chromosome[j])\
                    and professor_bits(chromosome[i]) == professor_bits(chromosome[j]):
                clash = True
                # print("These prof. have clashes")
                # print_chromosome(chromosome[i])
                # print_chromosome(chromosome[j])
        if not clash:
            scores = scores + 1
    return scores


# check that a group member takes only one class at a time.
def group_member_one_class(chromosomes):
    scores = 0

    for i in range(len(chromosomes) - 1):
        clash = False
        for j in range(i + 1, len(chromosomes)):
            if slot_clash(chromosomes[i], chromosomes[j]) and\
                    group_bits(chromosomes[i]) == group_bits(chromosomes[j]):
                # print("These courses have slot/lts clash")
                # print_chromosome(chromosomes[i])
                # print_chromosome(chromosomes[j])
                # print("____________")
                clash = True
                break
        if not clash:
            # print("These courses have no slot/lts clash")
            # print_chromosome(chromosomes[i])
            # print_chromosome(chromosomes[j])
            # print("____________")
            scores = scores + 1
    return scores


# checks that a course is assigned to an available classroom. 
def use_spare_classroom(chromosome):
    scores = 0
    for i in range(len(chromosome) - 1):  # select one cpg pair
        clash = False
        for j in range(i + 1, len(chromosome)):  # check it with all other cpg pairs
            if slot_clash(chromosome[i], chromosome[j]) and lt_bits(chromosome[i]) == lt_bits(chromosome[j]):
                # print("These courses have slot/lts clash")
                # printChromosome(chromosome[i])
                # printChromosome(chromosome[j])
                clash = True
        if not clash:
            scores = scores + 1
    return scores


# checks that the classroom capacity is large enough for the courses that
# are assigned to that classroom.
def classroom_size(chromosomes):
    scores = 0
    for _c in chromosomes:
        if Group.groups[int(group_bits(_c), 2)].size <= Room.rooms[int(lt_bits(_c), 2)].size:
            scores = scores + 1
    return scores


# check that room is appropriate for particular class/lab
def appropriate_room(chromosomes):
    scores = 0
    for _c in chromosomes:
        if Course.courses[int(course_bits(_c), 2)].is_lab == Room.rooms[int(lt_bits(_c), 2)].is_lab:
            scores = scores + 1
    return scores


# check that lab is allocated appropriate time slot
def appropriate_timeslot(chromosomes):
    scores = 0
    for _c in chromosomes:
        if Course.courses[int(course_bits(_c), 2)].is_lab == Slot.slots[int(slot_bits(_c), 2)].is_lab_slot:
            scores = scores + 1
    return scores

def evaluate(chromosomes):
    global max_score
    score = 0
    score = score + use_spare_classroom(chromosomes)
    score = score + faculty_member_one_class(chromosomes)
    score = score + classroom_size(chromosomes)
    score = score + group_member_one_class(chromosomes)
    score = score + appropriate_room(chromosomes)
    score = score + appropriate_timeslot(chromosomes)
    return score / max_score

def cost(solution):
    # solution would be an array inside an array
    # it is because we use it as it is in genetic algorithms
    # too. Because, GA require multiple solutions i.e population
    # to work.
    return 1 / float(evaluate(solution))

def init_population(n):
    global cpg, lts, slots
    chromosomes = []
    for _n in range(n):
        chromosome = []
        for _c in cpg:
            chromosome.append(_c + random.choice(slots) + random.choice(lts))
        chromosomes.append(chromosome)
    return chromosomes

def print_chromosome(chromosome):
    print(Course.courses[int(course_bits(chromosome), 2)], " | ",
          Professor.professors[int(professor_bits(chromosome), 2)], " | ",
          Group.groups[int(group_bits(chromosome), 2)], " | ",
          Slot.slots[int(slot_bits(chromosome), 2)], " | ",
          Room.rooms[int(lt_bits(chromosome), 2)])

# Simple Searching Neighborhood
# It randomly changes timeslot of a class/lab
def ssn(solution):
    rand_slot = random.choice(slots)
    rand_lt = random.choice(lts)
    
    a = random.randint(0, len(solution) - 1)
    
    new_solution = copy.deepcopy(solution)
    new_solution[a] = course_bits(solution[a]) + professor_bits(solution[a]) +\
        group_bits(solution[a]) + rand_slot + lt_bits(solution[a])
    return [new_solution]

# Swapping Neighborhoods
# It randomy selects two courses and swap their time slots
def swn(solution):
    a = random.randint(0, len(solution) - 1)
    b = random.randint(0, len(solution) - 1)
    new_solution = copy.deepcopy(solution)
    temp = slot_bits(solution[a])
    new_solution[a] = course_bits(solution[a]) + professor_bits(solution[a]) +\
        group_bits(solution[a]) + slot_bits(solution[b]) + lt_bits(solution[a])

    new_solution[b] = course_bits(solution[b]) + professor_bits(solution[b]) +\
        group_bits(solution[b]) + temp + lt_bits(solution[b])
    # print("Diff", solution)
    # print("Meiw", new_solution)
    return [new_solution]

def acceptance_probability(old_cost, new_cost, temperature):
    if new_cost < old_cost:
        return 1.0
    else:
        return math.exp((old_cost - new_cost) / temperature)

def simulated_annealing():
    alpha = 0.95
    T = 0.05
    T_min = 0.05
    
    convert_input_to_bin()
    population = init_population(1) # as simulated annealing is a single-state method
    old_cost = cost(population[0])
    # print("Cost of original random solution: ", old_cost)
    # print("Original population:")
    # print(population)

    for __n in range(4000):
        new_solution = swn(population[0])
        new_solution = ssn(population[0])
        new_cost = cost(new_solution[0])
        ap = acceptance_probability(old_cost, new_cost, T)
        if ap > random.random():
            population = new_solution
            old_cost = new_cost
        T = T * alpha
    # print(population)
    # print("Cost of altered solution: ", cost(population[0]))
    print("\n------------- Simulated Annealing --------------\n")
    for lec in population[0]:
        print_chromosome(lec)
    print("Score: ", evaluate(population[0]))


def main():
    # initlize pseudo-random number
    random.seed()

    # start simulated annealing and find best schedule
    simulated_annealing()

main()
