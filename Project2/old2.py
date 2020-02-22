# Omer Khan
# CS461 Brian Hare
# Project 2

# library imports
import random as r
import copy

verbose = False

# professor class for professor name, courses taught, time teaching, and location teaching at
class Prof:
    def __init__(self,name,courses,):
        self.name = name
        self.courses = courses
        self.time = []
        self.loc = []

# location class for location time, location name, and max allowed capacity 
class Location:
    def __init__(self,name,size,time):
        self.time = time
        self.name = name
        self.size = size

# time class for course time start, course time end, course day of the week, and whether timeslot is taken
class Time:
    def __init__(self,start,end):
        self.start = start
        self.end = end
        self.isFilled = False

# class course for course name, students enrolled or size, professor of course, location and time of course
class Course:
    def __init__(self,name,size):
        self.name = name
        self.size = size
        self.teacher = None
        self.location = None
        self.time = None
    

# list of professors and the courses they teach
professors = [  Prof("Hare", ["CS101A","CS101B","CS201A","CS201B","CS291A","CS291B","CS303","CS449","CS461"]),
                Prof("Bingham", ["CS101A","CS101B","CS201A","CS201B","CS191A","CS191B","CS291A","CS291B","CS449"]),
                Prof("Kuhail", ["CS303","CS341"]),
                Prof("Mitchell", ["CS191A","CS191B","CS291A","CS291B","CS303","CS341"]),
                Prof("Rao", ["CS291A","CS291B","CS303","CS341","CS461"]),
                Prof("Staff", ["CS101A","CS101B","CS201A","CS201B","CS191A","CS191B","CS291A","CS291B","CS303","CS341","CS449","CS461"])]

# list of times, start time, end time and day of the week
time = [Time("10:00", "10:50"),
        Time("11:00", "11:50"),
        Time("12:00", "12:50"),
        Time("13:00", "13:50"),
        Time("14:00", "14:50"),
        Time("15:00", "15:50"),
        Time("16:00", "16:50")]

#list of locations and max room capacity, and also availability of timings
loc = [ Location("Haag 301", 70, copy.deepcopy(time)),
        Location("Haag 206", 30,copy.deepcopy(time)),
        Location("Royall 204", 70,copy.deepcopy(time)),
        Location("Katz 209", 50,copy.deepcopy(time)),
        Location("Flarsheim 310", 80,copy.deepcopy(time)),
        Location("Flarsheim 260", 25,copy.deepcopy(time)),
        Location("Bloch 0009", 30,copy.deepcopy(time))]

# list of courses to be taught and their respective enrollment size
courses = [ Course("CS101A", 40),
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

# finds valid teachers that can teach the courses
def findTeachers(_class):
    # list that stores valid teachers
    valid_teacher = []
    # iterate over professors
    for teacher in professors:
        # if teacher can 
        if courses[_class].name in teacher.courses:
            valid_teacher.append(teacher)
    return valid_teacher

def findLoc(_class):
    valid_room = []
    for l in range (0,len(loc)):
            #schedule.sort(key=lambda x: x[2])
            # if the location can seat the enrollment size, then append the location to our list
            if(loc[l].size >= courses[_class].size):
                valid_room.append(l)
    return valid_room

def findTimeslots(loc,chosen_teacher,st):
    print('start')
    timeslots = copy.copy(loc.time)
    # iterate through all the times for that specific room
    for t in range (len(timeslots)-1,0 ,-1):
        if chosen_teacher.time:
            for q in chosen_teacher.time:
                print(timeslots[t].start)
                if q.start == timeslots[t].start:
                    del timeslots[t]
        elif (timeslots[t].isFilled):
            del timeslots[t]
        elif st:
            if( timeslots[t].start == st.start):
                del timeslots[t]
    print()
    for t in timeslots:
        print(t.start, end = ' ')
    return timeslots
    
def scheduleClass(valid_teacher,valid_room,_class):
    # sister class time
    st = None  
    # keep track of sister class time for reference
    for sis_class in courses:
        if(sis_class.name[0:len(sis_class.name)-1] == courses[_class].name[0:len(courses[_class].name)-1] and sis_class.name != courses[_class].name):
            st = sis_class.time
            
    for i in valid_room:
        # iterate through available rooms
        for chosen_teacher in valid_teacher:
            # get all the times of i room
            timeslots = findTimeslots(loc[i],chosen_teacher,st)
            # if any time exists in timeslots list
            if(len(timeslots) != 0):
                # choose a random time
                chosen_time = r.randint(0,len(timeslots)-1)
    
                if verbose:
                    print(loc[i].name)
                    print(timeslots[chosen_time].start)
                    for z in timeslots:
                        print(z.start, end = ' ')
    
                # set the course time and location accordingly
                courses[_class].time = timeslots[chosen_time]
                courses[_class].location = loc[i]
                # iterate through professors list
                for k in range(0,len(professors)):
                    # if randomly chosen professor is available
                    if professors[k].name == chosen_teacher.name:
                        # and if its not staff
                        if professors[k].name != "Staff":
                            # then append append the time of course to professor to teach
                            professors[k].time.append(timeslots[chosen_time])
                        # set the course instructor to chosen professor
                        courses[_class].teacher = professors[k]
                # iterate through remaining times at location
                for k in range(0,len(loc[i].time)):
                    # set the location time to isFilled aka time and room is busy being used
                    if loc[i].time[k].start == timeslots[chosen_time].start:
                        loc[i].time[k].isFilled = True
                return
            else:
                print("No slots left in Location: ", loc[i].name)
                for i in loc:
                    print(i.name,len(i.time))
                    for t in i.time:
                        print(t.start,t.isFilled)
                if verbose:
                    for h in loc[i].time:
                        print(h.start,h.isFilled)
                        
# generate a random schedule
def randSchedule():
    # chooses a class to schedule
    for _class in range (0,len(courses)):
        
        if(verbose):
            print('\n-------------------',courses[_class].name,'-------------------')
            
        valid_teacher = findTeachers(_class)
        valid_room = findLoc(_class)
        r.shuffle(valid_room)
        r.shuffle(valid_teacher)
        
        #for i in range (0,len(valid_room)-1):
        #    for j in range (i+1,len(valid_room)-1):
        #        if( loc[valid_room[i]].size > loc[valid_room[j]].size):
        #            valid_room[i],valid_room[j] = valid_room[j],valid_room[i]
        
        # create a list of best available rooms to teach class in
        scheduleClass(valid_teacher,valid_room,_class)


randSchedule()

for c in courses:
    print(c.name,c.size,c.location.name,c.teacher.name,c.time.start)

for t in professors:
    print('\n',t.name, end = ' ')
    for x in t.time:
        print(x.start, end=' ')
print()
for l in courses:
    print(l.location.name,l.time.start)
