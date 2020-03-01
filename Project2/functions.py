# Omer Khan
# Project 2
# CS461 Brian Hare

import random as r
import copy

# professor class for professor name, courses taught, time teaching, and location teaching at
class Professor:
    def __init__(self, name, courses):
        self.name = name
        self.courses = courses
        self.time = []

# location class for location time, location name, and max allowed capacity
class Location:
    def __init__(self, name, size, timings):
        self.name = name
        self.size = size
        self.time = copy.deepcopy(timings)

# time class for course time start, course time end, course day of the week, and whether timeslot is taken
class Time:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.available = True

# class course for course name, students enrolled or size, professor of course, location and time of course
class Course:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.time = None
        self.instructor = None
        self.place = None

# class schedule for each generated schedule
class Schedule:
    def __init__(self, courses, timings, classrooms, profs):
        self.fitness = 0
        self.courses = copy.deepcopy(courses)
        self.timings = copy.deepcopy(timings)
        self.classrooms = copy.deepcopy(classrooms)
        self.profs = copy.deepcopy(profs)

    # get a completely random schedule
    def random_schedule(self):
        for c in range(0, len(self.courses)):
            self.courses[c].instructor = self.profs[r.randint(0, len(self.profs) - 1)]
            location_num = r.randint(0, len(self.classrooms) - 1)
            self.courses[c].place = self.classrooms[location_num]
            self.courses[c].time = self.classrooms[location_num].time[
                r.randint(0, len(self.classrooms[location_num].time) - 1)]
    # pretty print the info
    def pprint(self):
        for s in self.courses:
            print(s.name)
            print(s.instructor.name)
            print(s.place.name)
            print(s.time.start)
            print()

    # calculate fitness score based on the given constraints
    def calculate_fitness_score(self):
        self.fitness = 0
        flag_clash=True
        
        # taught by instructor or staff
        for c in self.courses:
            if ((c.name in c.instructor.courses) and c.instructor.name != 'Staff'):
                self.fitness += 3
            if c.instructor.name == "Staff":
                self.fitness += 1
            for c_temp in self.courses:
                if c==c_temp:
                    continue
                else:
                    if((c.place == c_temp.place) and (c.time.start == c_temp.time.start)):
                        flag_clash=False
            if(flag_clash):
                self.fitness+=5
            flag_clash=True
            
            # if room size is big enough
            if (c.size <= c.place.size):
                self.fitness += 5
                # if room is no more than twice enrollment
                if (c.place.size <= c.size * 2):
                    self.fitness += 2

        # instructor only teaches 1 course at the same time
        counter=0
        professor={}
        staff={}
        for p in range(0, len(self.profs)):
            self.profs[p].time = []
            professor[self.profs[p].name]={}
            for c in self.courses:
                if c.instructor.name == self.profs[p].name:
                    if c.time.start not in professor[self.profs[p].name].keys():
                        professor[self.profs[p].name][c.time.start]=1
                    else:
                        professor[self.profs[p].name][c.time.start]=0
        try:
            professor.pop("Staff")
        except:
            pass
        for key in professor.keys():
            for key1 in professor[key].keys():
                counter+=professor[key][key1]
        self.fitness+=5*counter

        # if instructor teaching more than 4 courses
        num_profs = {}
        num_profs['Rao'] = 0
        num_profs['Bingham'] = 0
        num_profs['Kuhail'] = 0
        num_profs['Hare'] = 0
        num_profs['Mitchell'] = 0
        num_profs['Staff'] = 0
        for p in range(0, len(self.profs)):
            for c in self.courses:
                if c.instructor.name == self.profs[p].name:
                    num_profs[self.profs[p].name] += 1
        for prof in num_profs.keys():
            if num_profs[prof] > 4:
                self.fitness -= 5 * (num_profs[prof] - 4)

        # Rao or Mitchell teaching more than Hare or Bingham
        if ((num_profs['Rao']) > (num_profs['Hare'])):
            self.fitness -= 10
        if ((num_profs['Rao']) > (num_profs['Bingham'])):
            self.fitness -= 10
        if ((num_profs['Mitchell']) > (num_profs['Hare'])):
            self.fitness -= 10
        if ((num_profs['Mitchell']) > (num_profs['Bingham'])):
            self.fitness -= 10

        # if corequisite course at same time 201 and 291
        if (self.courses[2].time.start == self.courses[6].time.start):
            self.fitness -= 15
        if (self.courses[2].time.start == self.courses[7].time.start):
            self.fitness -= 15
        if (self.courses[3].time.start == self.courses[6].time.start):
            self.fitness -= 15
        if (self.courses[3].time.start == self.courses[7].time.start):
            self.fitness -= 15

        # if corequisite courses are adjacent 201 and 291
        index1 = 0
        for t in range(0, len(self.classrooms[0].time)):
            if self.classrooms[0].time[t].start == self.courses[2].time.start:
                index1 = t
                break
        index2 = 0
        for t in range(0, len(self.classrooms[0].time)):
            if self.classrooms[0].time[t].start == self.courses[3].time.start:
                index2 = t
                break
        index3 = 0
        for t in range(0, len(self.classrooms[0].time)):
            if self.classrooms[0].time[t].start == self.courses[6].time.start:
                index3 = t
                break
        index4 = 0
        for t in range(0, len(self.classrooms[0].time)):
            if self.classrooms[0].time[t].start == self.courses[7].time.start:
                index4 = t
                break
        if abs(index1 - index3) == 1:
            self.fitness += 5
        if abs(index1 - index4) == 1:
            self.fitness += 5
        if abs(index2 - index3) == 1:
            self.fitness += 5
        if abs(index2 - index4) == 1:
            self.fitness += 5

        # check if in same building 201 and 291
        if (self.courses[2].place.name.split(" ")[0] == self.courses[6].place.name.split(" ")[0]):
            self.fitness += 5
        else:
            if (self.courses[2].place.name.split(" ")[0] == "Katz 209".split(" ")[0] and \
                    self.courses[6].place.name.split(" ")[0] != "Katz 209".split(" ")[0]):
                self.fitness -= 3
            if (self.courses[2].place.name.split(" ")[0] == "Bloch 0009".split(" ")[0] and \
                    self.courses[6].place.name.split(" ")[0] != "Bloch 0009".split(" ")[0]):
                self.fitness -= 3

        if (self.courses[3].place.name.split(" ")[0] == self.courses[7].place.name.split(" ")[0]):
            self.fitness += 5
        else:
            if (self.courses[3].place.name.split(" ")[0] == "Katz 209".split(" ")[0] and \
                    self.courses[7].place.name.split(" ")[0] != "Katz 209".split(" ")[0]):
                self.fitness -= 3
            if (self.courses[3].place.name.split(" ")[0] == "Bloch 0009".split(" ")[0] and \
                    self.courses[7].place.name.split(" ")[0] != "Bloch 0009".split(" ")[0]):
                self.fitness -= 3

        if (self.courses[2].place.name.split(" ")[0] == self.courses[7].place.name.split(" ")[0]):
            self.fitness += 5
        else:
            if (self.courses[2].place.name.split(" ")[0] == "Katz 209".split(" ")[0] and \
                    self.courses[7].place.name.split(" ")[0] != "Katz 209".split(" ")[0]):
                self.fitness -= 3
            if (self.courses[2].place.name.split(" ")[0] == "Bloch 0009".split(" ")[0] and \
                    self.courses[7].place.name.split(" ")[0] != "Bloch 0009".split(" ")[0]):
                self.fitness -= 3

        if (self.courses[3].place.name.split(" ")[0] == self.courses[6].place.name.split(" ")[0]):
            self.fitness += 5
        else:
            if (self.courses[3].place.name.split(" ")[0] == "Katz 209".split(" ")[0] and \
                    self.courses[6].place.name.split(" ")[0] != "Katz 209".split(" ")[0]):
                self.fitness -= 3
            if (self.courses[3].place.name.split(" ")[0] == "Bloch 0009".split(" ")[0] and \
                    self.courses[6].place.name.split(" ")[0] != "Bloch 0009".split(" ")[0]):
                self.fitness -= 3

        # if corequisite course at same time 101 and 191
        if (self.courses[0].time.start == self.courses[4].time.start):
            self.fitness -= 15
        if (self.courses[0].time.start == self.courses[5].time.start):
            self.fitness -= 15
        if (self.courses[1].time.start == self.courses[4].time.start):
            self.fitness -= 15
        if (self.courses[1].time.start == self.courses[5].time.start):
            self.fitness -= 15

        # if corequisite courses are adjacent 101 and 191
        index1 = 0
        for t in range(0, len(self.classrooms[0].time)):
            if self.classrooms[0].time[t].start == self.courses[0].time.start:
                index1 = t
                break
        index2 = 0
        for t in range(0, len(self.classrooms[0].time)):
            if self.classrooms[0].time[t].start == self.courses[1].time.start:
                index2 = t
                break
        index3 = 0
        for t in range(0, len(self.classrooms[0].time)):
            if self.classrooms[0].time[t].start == self.courses[4].time.start:
                index3 = t
                break
        index4 = 0
        for t in range(0, len(self.classrooms[0].time)):
            if self.classrooms[0].time[t].start == self.courses[5].time.start:
                index4 = t
                break
        if abs(index1 - index3) == 1:
            self.fitness += 5
        if abs(index1 - index4) == 1:
            self.fitness += 5
        if abs(index2 - index3) == 1:
            self.fitness += 5
        if abs(index2 - index4) == 1:
            self.fitness += 5

        # check if in same building 101 and 191
        if (self.courses[0].place.name.split(" ")[0] == self.courses[4].place.name.split(" ")[0]):
            self.fitness += 5
        else:
            if (self.courses[0].place.name.split(" ")[0] == "Katz 209".split(" ")[0] and \
                    self.courses[4].place.name.split(" ")[0] != "Katz 209".split(" ")[0]):
                self.fitness -= 3
            if (self.courses[0].place.name.split(" ")[0] == "Bloch 0009".split(" ")[0] and \
                    self.courses[4].place.name.split(" ")[0] != "Bloch 0009".split(" ")[0]):
                self.fitness -= 3

        if (self.courses[1].place.name.split(" ")[0] == self.courses[5].place.name.split(" ")[0]):
            self.fitness += 5
        else:
            if (self.courses[1].place.name.split(" ")[0] == "Katz 209".split(" ")[0] and \
                    self.courses[5].place.name.split(" ")[0] != "Katz 209".split(" ")[0]):
                self.fitness -= 3
            if (self.courses[1].place.name.split(" ")[0] == "Bloch 0009".split(" ")[0] and \
                    self.courses[5].place.name.split(" ")[0] != "Bloch 0009".split(" ")[0]):
                self.fitness -= 3

        if (self.courses[0].place.name.split(" ")[0] == self.courses[4].place.name.split(" ")[0]):
            self.fitness += 5
        else:
            if (self.courses[0].place.name.split(" ")[0] == "Katz 209".split(" ")[0] and \
                    self.courses[4].place.name.split(" ")[0] != "Katz 209".split(" ")[0]):
                self.fitness -= 3
            if (self.courses[0].place.name.split(" ")[0] == "Bloch 0009".split(" ")[0] and \
                    self.courses[4].place.name.split(" ")[0] != "Bloch 0009".split(" ")[0]):
                self.fitness -= 3

        if (self.courses[1].place.name.split(" ")[0] == self.courses[5].place.name.split(" ")[0]):
            self.fitness += 5
        else:
            if (self.courses[1].place.name.split(" ")[0] == "Katz 209".split(" ")[0] and \
                    self.courses[5].place.name.split(" ")[0] != "Katz 209".split(" ")[0]):
                self.fitness -= 3
            if (self.courses[1].place.name.split(" ")[0] == "Bloch 0009".split(" ")[0] and \
                    self.courses[5].place.name.split(" ")[0] != "Bloch 0009".split(" ")[0]):
                self.fitness -= 3

        # if (CS101A, CS101B) and (CS191A, CS191B) are 3 hours or more apart
        index1 = 0
        for t in range(0, len(self.classrooms[0].time)):
            if self.classrooms[0].time[t].start == self.courses[0].time.start:
                index1 = t
                break
        index2 = 0
        for t in range(0, len(self.classrooms[0].time)):
            if self.classrooms[0].time[t].start == self.courses[1].time.start:
                index2 = t
                break
        index3 = 0
        for t in range(0, len(self.classrooms[0].time)):
            if self.classrooms[0].time[t].start == self.courses[4].time.start:
                index3 = t
                break
        index4 = 0
        for t in range(0, len(self.classrooms[0].time)):
            if self.classrooms[0].time[t].start == self.courses[5].time.start:
                index4 = t
                break
        if abs(index1 - index2) >= 3:
            self.fitness += 5
        if abs(index3 - index4) >= 3:
            self.fitness += 5

    # make random changes to the schedule for simulated sannealing
    def sa_random_change(self, T):
        rnum1 = r.uniform(0, 1)
        x=r.randint(0, len(self.courses)-1)
        if rnum1 < T:
            self.courses[x].time = self.courses[x].place.time[r.randint(0, len(self.courses[x].place.time) - 1)]
            self.courses[x].place = self.classrooms[r.randint(0, len(self.classrooms) - 1)]
            self.courses[x].instructor = self.profs[r.randint(0, len(self.profs) - 1)]

# simulated annealing function
def simulated_annealing(courses, timings, classrooms, profs):
    # drop T by 90% each iteration
    alpha = 0.90
    # T starts at 1
    T = 1
    # min T allowed
    T_min = 0.00001

    # generate 1 random (imperfect) schedule and find its fitness, and print
    cursolution = Schedule(courses, timings, classrooms, profs)
    cursolution.random_schedule()
    cursolution.calculate_fitness_score()
    print(cursolution.pprint())
    print('Initial solution: ', cursolution.fitness)
    print('#########################')

    # tracking variables
    concur_changes = 0
    concur_nochanges = 0
    iterations = 0
    # main simulation for annealing
    while iterations > -1:
        # copy the random schedule, and calculate fitness again
        newsolution = copy.deepcopy(cursolution)
        newsolution.fitness = 0
        # make random changes to each course, and calculate fitness
        newsolution.sa_random_change(T)
        newsolution.calculate_fitness_score()
        # if new fitness is better than old, old schedule = new
        if (newsolution.fitness > cursolution.fitness):
            cursolution = newsolution
            concur_changes += 1
            concur_nochanges = 0
        else:
            # no changes were valid
            concur_changes = 0
            concur_nochanges += 1
        iterations += 1
        # if schedule ran 4000 or more iterations without changes
        if concur_nochanges >= 4000:
            break;
        # or if 400 concurrent changes were made
        elif concur_changes >= 400 or iterations >= 4000:
            concur_nochanges = 0
            concur_changes = 0
            iterations = 0
            # decrease T
            T = T * alpha
            print('T Updated: ', T)

    # sort the schedule by time and print schedule, T and final fitness
    cursolution.courses.sort(key=lambda courses: courses.time.start, reverse=False)
    cursolution.pprint()
    print('T: ', T)
    print('End solution', cursolution.fitness)
