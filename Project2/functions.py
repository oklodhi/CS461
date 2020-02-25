# Omer Khan
# Project 2
# CS461 Brian Hare

import random as r
import copy

# professor class for professor name, courses taught, time teaching, and location teaching at
class Professor:
    def __init__(self,name,courses):
        self.name = name
        self.courses = courses
        self.time = []

# location class for location time, location name, and max allowed capacity 
class Location:
    def __init__(self,name,size,timings):
        self.name = name
        self.size = size
        self.time = copy.deepcopy(timings)

# time class for course time start, course time end, course day of the week, and whether timeslot is taken
class Time:
    def __init__(self,start,end):
        self.start = start
        self.end = end
        self.available = True

# class course for course name, students enrolled or size, professor of course, location and time of course
class Course:
    def __init__(self,name,size):
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

    def random_schedule(self):
        for c in range(0,len(self.courses)):
            self.courses[c].instructor = self.profs[r.randint(0,len(self.profs)-1)]
            location_num = r.randint(0,len(self.classrooms)-1)
            self.courses[c].place = self.classrooms[location_num]
            self.courses[c].time = self.classrooms[location_num].time[r.randint(0,len(self.classrooms[location_num].time)-1)]
        
    # get a random course from course list
    def get_random_course(self):
        courselist = copy.deepcopy(self.courses)
        for c in range(len(courselist)-1,-1,-1):
            if courselist[c].time:
                del courselist[c]
        if courselist:
            return courselist[r.randint(0,len(courselist)-1)]
        else:
            return None

    # get a random professor from professor list
    def get_random_professor(self,course):
        valid_profs = []
        for p in self.profs:
            if course.name in p.courses:
                valid_profs.append(p)
        if valid_profs:
            return valid_profs[r.randint(0,len(valid_profs)-1)]
        else:
            return None

    # get a random classroom from location list
    def get_random_location(self,size):
        valid_rooms = []
        for c in self.classrooms:
            if c.size >= size:
                valid_rooms.append(c)
        valid_rooms.sort(key=lambda classrooms: classrooms.size, reverse=False)

        if valid_rooms:
            return valid_rooms[r.randint(0,len(valid_rooms)-1)]
        else:
            return None

    # helper function to search if element exists
    def contains(self,list, filter):
        for x in list:
            if filter(x):
                return True
        return False

    # get a random time from timing list
    def get_random_time(self,professor,location):
        valid_time = []
        for t in location.time:
            if t.available == True and not self.contains(professor.time, lambda time: time.start == t.start):
                valid_time.append(t)

        if valid_time:
            return valid_time[r.randint(0,len(valid_time)-1)]
        else:
            return None

    # pretty print the info
    def pprint(self):
        for s in self.courses:
            print(s.name)
            print(s.instructor.name)
            print(s.place.name)
            print(s.time.start)
            print()

    # create a schedule for a single course
    def create_single_course(self,currentcourse):
        currentprofessor = None
        currentlocation = None
        currenttime = None
        
        while( currentprofessor == None and currentlocation == None and currenttime == None):
            currentprofessor = self.get_random_professor(currentcourse)
            currentlocation = self.get_random_location(currentcourse.size)
            currenttime = self.get_random_time(currentprofessor,currentlocation)

        index_c = 0
        for c in range(0,len(self.courses)):
            if self.courses[c].name == currentcourse.name:
                index_c = c
                break
        index_i = 0
        for i in range(0,len(self.profs)):
            if self.profs[i].name == currentprofessor.name:
                index_i = i
                break
        index_p = 0
        for p in range(0,len(self.classrooms)):
            if self.classrooms[p].name == currentlocation.name:
                index_p = p
                break
        index_t = 0
        for t in range(0,len(self.classrooms[index_p].time)):
            if self.classrooms[index_p].time[t].start == currenttime.start:
                index_t = t
                break
        
        self.courses[index_c].instructor = currentprofessor
        self.courses[index_c].place = currentlocation
        self.courses[index_c].time = currenttime
        if(self.profs[index_i].name != 'Staff'):
            self.profs[index_i].time.append(currenttime)
        #for t in currentlocation.time:
            #if t == currenttime:
               #t.available = False 

        self.classrooms[index_p].time[index_t].available = False
        #print("Course   index:",index_c, '\tCourse   Name: ', self.courses[index_c].name)
        #print("Teacher  index:",index_i, '\tTeacher  Name: ', self.profs[index_i].name)
        #print("Location index:",index_c, '\tLocation Name: ', self.classrooms[index_p].name)
        #print("Time     index:",index_t, '\tTime    Start: ', self.classrooms[index_p].time[index_t].start)
        #print()

    # generate an entire valid schedule
    def generate_schedule(self):
        for i in range(0,len(self.courses)):
            self.create_single_course(self.courses[i])
        #self.pprint()

    # calculate fitness score based on the given constraints
    def calculate_fitness_score(self):
        self.fitness = 0
        # taught by instructor or staff
        for c in self.courses:
            if c.instructor.name == "Staff":
                self.fitness += 1
            elif c.name in c.instructor.courses:
                self.fitness += 3
            # if room size is twice enrollment
            if (c.size <= c.place.size):
                self.fitness += 5
                # if room is twice as enrollment
                if( c.place.size <= c.size*2):
                    self.fitness += 2
                    
        # instructor only teaches 1 course at the same time
        for p in range(0,len(self.profs)):
            self.profs[p].time = []
            for c in self.courses:
                if c.instructor.name == self.profs[p].name:
                    self.profs[p].time.append(c.time)
            for t in range(0, len(self.profs[p].time)):
                for i in range(t+1,len(self.profs[p].time)):
                    if self.profs[p].time[t].start != self.profs[p].time[i].start:
                        if self.profs[p].name != 'Staff':
                            self.fitness += 5
        # if corequisite course at same time 201 and 291
        if (self.courses[2].time.start == self.courses[6].time.start):
            self.fitness -= 15
        if (self.courses[3].time.start == self.courses[7].time.start):
            self.fitness -= 15
            
        # if corequisite courses are adjacent 
        index1 = 0
        for t in range(0,len(self.classrooms[0].time)):
            if self.classrooms[0].time[t].start == self.courses[2].time.start:
                index1 = t
                break
        index2 = 0
        for t in range(0,len(self.classrooms[0].time)):
            if self.classrooms[0].time[t].start == self.courses[3].time.start:
                index2 = t
                break
        index3 = 0
        for t in range(0,len(self.classrooms[0].time)):
            if self.classrooms[0].time[t].start == self.courses[6].time.start:
                index3 = t
                break
        index4 = 0
        for t in range(0,len(self.classrooms[0].time)):
            if self.classrooms[0].time[t].start == self.courses[7].time.start:
                index4 = t
                break
        if abs(index1 - index3) == 1:
            self.fitness += 5
            
            # check if in same building
            if (self.courses[2].place.name == self.courses[6].place.name):
                    self.fitness += 5
            else:
                if (self.courses[2].place.name == "Katz 209" or \
                   self.courses[6].place.name == "Katz 209"):
                    self.fitness -= 3
                if (self.courses[2].place.name == "Bloch 0009" or \
                   self.courses[6].place.name == "Bloch 0009"):
                    self.fitness -= 3

        if abs(index2 - index4) == 1:
            self.fitness += 5
            
            # check if in same building
            if (self.courses[3].place.name == self.courses[7].place.name):
                    self.fitness += 5
            else:
                if (self.courses[3].place.name == "Katz 209" or \
                   self.courses[7].place.name == "Katz 209"):
                    self.fitness -= 3
                if (self.courses[3].place.name == "Bloch 0009" or \
                   self.courses[7].place.name == "Bloch 0009"):
                    self.fitness -= 3
                    
        # if corequisite course at same time 101 and 191
        if (self.courses[0].time.start == self.courses[4].time.start):
            self.fitness -= 15
        if (self.courses[1].time.start == self.courses[5].time.start) :
            self.fitness -= 15
            
        # if corequisite course are adjacent 
        index1 = 0
        for t in range(0,len(self.classrooms[0].time)):
            if self.classrooms[0].time[t].start == self.courses[0].time.start:
                index1 = t
                break
        index2 = 0
        for t in range(0,len(self.classrooms[0].time)):
            if self.classrooms[0].time[t].start == self.courses[1].time.start:
                index2 = t
                break
        index3 = 0
        for t in range(0,len(self.classrooms[0].time)):
            if self.classrooms[0].time[t].start == self.courses[4].time.start:
                index3 = t
                break
        index4 = 0
        for t in range(0,len(self.classrooms[0].time)):
            if self.classrooms[0].time[t].start == self.courses[5].time.start:
                index4 = t
                break
        if abs(index1 - index3) == 1:
            self.fitness += 5
            
            # check if in same building
            if (self.courses[0].place.name == self.courses[4].place.name):
                    self.fitness += 5
            else:
                if (self.courses[0].place.name == "Katz 209" or \
                   self.courses[4].place.name == "Katz 209"):
                    self.fitness -= 3
                if (self.courses[0].place.name == "Bloch 0009" or \
                   self.courses[4].place.name == "Bloch 0009"):
                    self.fitness -= 3

        if abs(index2 - index4) == 1:
            self.fitness += 5
            # check if in same building
            if (self.courses[1].place.name == self.courses[5].place.name):
                    self.fitness += 5
            else:
                if (self.courses[1].place.name == "Katz 209" or \
                   self.courses[5].place.name == "Katz 209"):
                    self.fitness -= 3
                if (self.courses[1].place.name == "Bloch 0009" or \
                   self.courses[5].place.name == "Bloch 0009"):
                    self.fitness -= 3
        if abs(index1 - index2) >= 3:
            self.fitness += 5
        if abs(index3 - index4) >= 3:
            self.fitness += 5
                
        # if instructor teaching more than 4 courses
        num_profs = [0]*(len(self.profs))
        for p in range(0,len(self.profs)):
            new = 0
            for c in self.courses:
                if c.instructor.name == self.profs[p].name:
                    new += 1
                num_profs[p] = new
        for p in num_profs:
            if p > 4:
                self.fitness -= 5*(p-4)
        # Rao or Mitchell teaching more than Hare or Bingham
        if (num_profs[3]) > (num_profs[0]) or \
           (num_profs[3]) > (num_profs[1]) or \
           (num_profs[4]) > (num_profs[0]) or \
           (num_profs[4]) > (num_profs[1]):
            self.fitness -= 10
        
    def sa_random_change(self,T):
        for c in range(0,len(self.courses)-1):
            rnum1 = r.uniform(0, 1)
            rnum2 = r.uniform(0, 1)
            rnum3 = r.uniform(0, 1)
            if rnum1 < T:
                # change time
                self.courses[c].time = self.courses[c].place.time[r.randint(0,len(self.courses[c].place.time)-1)]
            if rnum2 < T:
                # change location
                self.courses[c].place = self.classrooms[r.randint(0,len(self.classrooms)-1)]
            if rnum3 < T:
                # change professor
                self.courses[c].instructor = self.profs[r.randint(0,len(self.profs)-1)]
            

def simulated_annealing(courses, timings, classrooms, profs):
    alpha = 0.90
    T = 1
    T_min = 0.00001
    
    cursolution = Schedule(courses, timings, classrooms, profs)
    #cursolution.generate_schedule()
    cursolution.random_schedule()
    cursolution.calculate_fitness_score()
    print(cursolution.pprint())
    print('Initial solution: ', cursolution.fitness)
    print('#########################')

    concur_changes = 0
    concur_nochanges = 0
    iterations = 0
    while iterations > -1:
        newsolution = copy.deepcopy(cursolution)
        newsolution.fitness = 0
        newsolution.sa_random_change(T)
        newsolution.calculate_fitness_score()
        if (newsolution.fitness > cursolution.fitness):
            cursolution = newsolution
            concur_changes += 1
            concur_nochanges = 0
        else:
            concur_changes = 0
            concur_nochanges += 1
        iterations += 1
        if concur_nochanges >= 4000:
            break;
        elif concur_changes >= 400 or iterations >= 4000:
            concur_nochanges = 0
            concur_changes = 0
            iterations = 0
            T = T * alpha
            print('T Updated: ', T)
    cursolution.courses.sort(key=lambda courses: courses.time.start, reverse=False)
    cursolution.pprint()
    print('T: ', T)
    print('End solution', cursolution.fitness)
        
    

























    
