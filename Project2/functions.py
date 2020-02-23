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
        for c in self.courses:
            # taught by instructor or staff
            if c.instructor.name != "Staff":
                self.fitness += 3
            else:
                self.fitness += 1
            # if room size is twice enrollment
            if( 2*c.place.size <= c.size):
                self.fitness += 2
                
        # if instructor teaching more than 4 courses
        for p in self.profs:
            if len(p.time) > 4:
                self.fitness -= 5*(len(p.time)-4)
        # Rao or Mitchell vs Hare or Bingham
        if (len(self.profs[3].time) > len(self.profs[0].time)) or \
           (len(self.profs[3].time) > len(self.profs[1].time)) or \
           (len(self.profs[4].time) > len(self.profs[0].time)) or \
           (len(self.profs[4].time) > len(self.profs[1].time)):
            self.fitness -= 10
        # if corequisite course at same time 201 and 291
        if (self.courses[2].time.start == self.courses[6].time.start) or \
           (self.courses[2].time.start == self.courses[7].time.start):
            self.fitness -= 15
        if (self.courses[3].time.start == self.courses[4].time.start) or \
           (self.courses[3].time.start == self.courses[6].time.start):
            self.fitness -= 15
        # if corequisite courses are adjacent 
        index1 = 0
        for t in range(0,len(self.classrooms[2].time)):
            if self.classrooms[t].time[t].start == self.courses[2].time.start:
                index1 = t
                break
        index2 = 0
        for t in range(0,len(self.classrooms[3].time)):
            if self.classrooms[t].time[t].start == self.courses[3].time.start:
                index2 = t
                break
        index3 = 0
        for t in range(0,len(self.classrooms[6].time)):
            if self.classrooms[t].time[t].start == self.courses[6].time.start:
                index3 = t
                break
        index4 = 0
        for t in range(0,len(self.classrooms[0].time)):
            if self.classrooms[t].time[t].start == self.courses[7].time.start:
                index4 = t
                break
        if abs(index1 - index3) == 1 or \
           abs(index1 - index4) == 1:
            self.fitness += 5
            # check if in same building
            if (self.courses[2].place.name == self.courses[6].place.name) or \
               (self.courses[2].place.name == self.courses[7].place.name):
                    self.fitness += 5
            else:
                if (self.courses[2].place.name == "Katz 209" or \
                   self.courses[6].place.name == "Katz 209" or \
                   self.courses[7].place.name == "Katz 209"):
                    self.fitness -= 3
                if (self.courses[2].place.name == "Bloch 0009" or \
                   self.courses[6].place.name == "Bloch 0009" or \
                   self.courses[7].place.name == "Bloch 0009"):
                    self.fitness -= 3

        if abs(index2 - index3) == 1 or \
           abs(index2 - index4) == 1:
            self.fitness += 5
            # check if in same building
            if (self.courses[3].place.name == self.courses[6].place.name) or \
               (self.courses[3].place.name == self.courses[7].place.name):
                    self.fitness += 5
            else:
                if (self.courses[3].place.name == "Katz 209" or \
                   self.courses[6].place.name == "Katz 209" or \
                   self.courses[7].place.name == "Katz 209"):
                    self.fitness -= 3
                if (self.courses[3].place.name == "Bloch 0009" or \
                   self.courses[6].place.name == "Bloch 0009" or \
                   self.courses[7].place.name == "Bloch 0009"):
                    self.fitness -= 3
        
        # if corequisite course at same time 101 and 191
        if (self.courses[0].time.start == self.courses[4].time.start) or \
           (self.courses[0].time.start == self.courses[5].time.start):
            self.fitness -= 15
        if (self.courses[1].time.start == self.courses[4].time.start) or \
           (self.courses[1].time.start == self.courses[5].time.start):
            self.fitness -= 15
        # if corequisite course are adjacent 
        index1 = 0
        for t in range(0,len(self.classrooms[0].time)):
            if self.classrooms[t].time[t].start == self.courses[0].time.start:
                index1 = t
                break
        index2 = 0
        for t in range(0,len(self.classrooms[1].time)):
            if self.classrooms[t].time[t].start == self.courses[1].time.start:
                index2 = t
                break
        index3 = 0
        for t in range(0,len(self.classrooms[4].time)):
            if self.classrooms[t].time[t].start == self.courses[4].time.start:
                index3 = t
                break
        index4 = 0
        for t in range(0,len(self.classrooms[5].time)):
            if self.classrooms[t].time[t].start == self.courses[5].time.start:
                index4 = t
                break
        if abs(index1 - index3) == 1 or \
           abs(index1 - index4) == 1:
            self.fitness += 5
            # check if in same building
            if (self.courses[0].place.name == self.courses[4].place.name) or \
               (self.courses[0].place.name == self.courses[5].place.name):
                    self.fitness += 5
            else:
                if (self.courses[0].place.name == "Katz 209" or \
                   self.courses[4].place.name == "Katz 209" or \
                   self.courses[5].place.name == "Katz 209"):
                    self.fitness -= 3
                if (self.courses[0].place.name == "Bloch 0009" or \
                   self.courses[4].place.name == "Bloch 0009" or \
                   self.courses[5].place.name == "Bloch 0009"):
                    self.fitness -= 3

        if abs(index2 - index3) == 1 or \
           abs(index2 - index4) == 1:
            self.fitness += 5
            # check if in same building
            if (self.courses[1].place.name == self.courses[4].place.name) or \
               (self.courses[1].place.name == self.courses[5].place.name):
                    self.fitness += 5
            else:
                if (self.courses[1].place.name == "Katz 209" or \
                   self.courses[4].place.name == "Katz 209" or \
                   self.courses[5].place.name == "Katz 209"):
                    self.fitness -= 3
                if (self.courses[1].place.name == "Bloch 0009" or \
                   self.courses[4].place.name == "Bloch 0009" or \
                   self.courses[5].place.name == "Bloch 0009"):
                    self.fitness -= 3
        if abs(index1 - index2) >= 3:
            self.fitness += 5
        if abs(index3 - index4) >= 3:
            self.fitness += 5




























    
