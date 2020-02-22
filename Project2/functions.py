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

class Schedule:
    def __init__(self, courses, timings, classrooms, profs):
        self.fitness = 0
        self.courses = copy.deepcopy(courses)
        self.timings = copy.deepcopy(timings)
        self.classrooms = copy.deepcopy(classrooms)
        self.profs = copy.deepcopy(profs)
    
    def get_random_course(self):
        courselist = copy.deepcopy(self.courses)
        for c in range(len(courselist)-1,-1,-1):
            if courselist[c].time:
                del courselist[c]
        if courselist:
            return courselist[r.randint(0,len(courselist)-1)]
        else:
            return None

    def get_random_professor(self,course):
        valid_profs = []
        for p in self.profs:
            if course.name in p.courses:
                valid_profs.append(p)
        if valid_profs:
            return valid_profs[r.randint(0,len(valid_profs)-1)]
        else:
            return None
        
    def get_random_location(self,size):
        valid_rooms = []
        for c in self.classrooms:
            if c.size >= size:
                valid_rooms.append(c)
        valid_rooms.sort(key=lambda classrooms: classrooms.size, reverse=False)

        if valid_rooms[0]:
            return valid_rooms[0]
        else:
            return None

    def contains(self,list, filter):
        for x in list:
            if filter(x):
                return True
        return False

    def get_random_time(self,professor,location):
        valid_time = []
        for t in location.time:
            if t.available == True and not self.contains(professor.time, lambda time: time.start == t.start):
                valid_time.append(t)

        if valid_time:
            return valid_time[r.randint(0,len(valid_time)-1)]
        else:
            return None

    def pprint(self):
        for s in self.courses:
            print(s.name)
            print(s.instructor.name)
            print(s.place.name)
            print(s.time.start)
            print()

    def create_single_course(self,course):
        currentcourse = course

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
        print(index_c)
        print(index_i)
        print(index_p)
        print(index_t)

        
        self.courses[index_c].instructor = currentprofessor
        self.courses[index_c].place = currentlocation
        self.courses[index_c].time = currenttime
        self.profs[index_i].time.append(currenttime)
##        for t in currentlocation.time:
##            if t == currenttime:
##                t.available = False 

        self.classrooms[index_p].time[index_t].available = False

        print(currentcourse.name)
        print(self.courses[index_c].instructor.name)
        print(self.courses[index_c].place.name)
        print(self.courses[index_c].time.start)
        
    def generate_schedule(self):
        for i in range(0,len(self.courses)):
            self.create_single_course(self.courses[i])
        #self.pprint()



























    
