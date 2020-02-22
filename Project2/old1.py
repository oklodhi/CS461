# Omer Khan
# CS461 Brian Hare
# Project 2

# library imports
import random as r

verbose = True

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
loc = [ Location("Haag 301", 70, time),
        Location("Haag 206", 30,time),
        Location("Royall 204", 70,time),
        Location("Katz 209", 50,time),
        Location("Flarsheim 310", 80,time),
        Location("Flarsheim 260", 25,time),
        Location("Bloch 0009", 30,time)]

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

# generate a random schedule
def randSchedule():
    # chooses a class to schedule
    for _class in range (0,len(courses)):
        
        if(verbose):
            print('\n-------------------',courses[_class].name,'-------------------')
        #find valid teachers for said class
        valid_teacher = []

        # sister class time
        st = None

        # find a professor who teaches the class and create a list of those professors 
        for teacher in professors:
            if courses[_class].name in teacher.courses:
                valid_teacher.append(teacher)
                
        # keep track of sister class time for reference
        for sis_class in courses:
            if(sis_class.name[0:len(sis_class.name)-1] == courses[_class].name[0:len(courses[_class].name)-1] and sis_class.name != courses[_class].name):
               st = sis_class.time
               
        # create a list of best available rooms to teach class in
        valid_room = []

        # iterate through all locations
        for l in range (0,len(loc)):
            #schedule.sort(key=lambda x: x[2])
            # if the location can seat the enrollment size, then append the location to our list
            if(loc[l].size >= courses[_class].size):
                valid_room.append(l)
    
        # randomize the sorting of valid_room list
        r.shuffle(valid_room)
        # choose a random teacher to schedule to teach the class
        chosen_teacher = valid_teacher[r.randint(0,len(valid_teacher)-1)]

        # iterate through available rooms
        for i in valid_room:
            # get all the times of i room
            timeslots = loc[i].time

            # iterate through all the times for that specific room
            for t in range (len(timeslots)-1,0,-1):
                # if this class has a sister time, and it is scheduled at same time
                # then delete delete that time from possible timing
                if st:
                    if( timeslots[t].start == st.start):
                        del timeslots[t]
                # if that time is already filled, then delete timing
                elif (timeslots[t].isFilled):
                    del timeslots[t]
                # if the chosen professor is already teaching at that time, then delete timing
                elif chosen_teacher.time:
                    if (timeslots[t] in chosen_teacher.time):
                        del timeslots[t]

            # if any time exists in timeslots list
            if(len(timeslots)-1 != 0):
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
                for k in range(0,len(loc[i].time)-1):
                    # set the location time to isFilled aka time and room is busy being used
                    if loc[i].time[k] == timeslots[chosen_time]:
                        loc[i].time[k].isFilled = True
                break
            else:
                print("No slots left in Location: ", loc[i].name)
            
# simulated annealing                  
def simulated_annealing():
    alpha = .05
    T = .95
    T_min = .05
    randSchedule()

''' MAIN START HERE '''
randSchedule()

schedule = []
# and print
for i in range (0,len(courses)):
    s = [courses[i].name, courses[i].size, courses[i].time.start, courses[i].teacher.name, [courses[i].location.name, courses[i].location.size]] 
    schedule.append(s)

# sort list by start times
schedule.sort(key=lambda x: x[2])
print('\n\n')
for i in schedule:
    print(i)
