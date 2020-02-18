import random as r

class Prof:
    def __init__(self,name,courses,):
        self.name = name
        self.courses = courses
        self.time = None
        self.loc = None


class Location:
    def __init__(self,name,size,time):
        self.time = time
        self.name = name
        self.size = size

class Time:
    def __init__(self,start,end,day):
        self.start = start
        self.end = end
        self.day = day
        self.filled = False

class Course:
    def __init__(self,name,size):
        self.name = name
        self.size = size
        self.teacher = None
        self.location = None
        self.time = None
    

professors = [ Prof("Hare", ["CS101A","CS101B","CS201A","CS201B","CS291A","CS291B","CS303","CS449","CS461"]),
                    Prof("Bingham", ["CS101A","CS101B","CS201A","CS201B","CS191A","CS191B","CS291A","CS291B","CS449"]),
                    Prof("Kuhail", ["CS303","CS341"]),
                    Prof("Mitchell", ["CS191A","CS191B","CS291A","CS291B","CS303","CS341"]),
                    Prof("Rao", ["CS291A","CS291B","CS303","CS341","CS461"]),
                    Prof("Staff", ["CS101A","CS101B","CS201A","CS201B","CS191A","CS191B","CS291A","CS291B","CS303","CS341","CS449","CS461"])]

time = [  Time("10:00", "10:50", "Mon"),
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

loc =      [ Location("Haag 301", 70, time),
                      Location("Haag 206", 30,time),
                      Location("Royall 204", 70,time),
                      Location("Katz 209", 50,time),
                      Location("Flarsheim 310", 80,time),
                      Location("Flarsheim 260", 25,time),
                      Location("Bloch 0009", 30,time)]


courses =       [ Course("CS101A", 40),
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

def randSchedule():
    # chooses a class to schedule
    for cur_class in courses:
        #find valid teachers for said class
        valid_teacher = []
        st = None # sister class time
        for teacher in professors:
            if cur_class.name in teacher.courses:
                valid_teacher.append(teacher.name)
        # find the sister class, to check the time for ref
        for sis_class in courses:
            if(sis_class.name[0:len(sis_class.name)-1]==cur_class.name[0:len(cur_class.name)-1] and sis_class.name != cur_class.name):
               st = sis_class.time
               
        # create a loc array based on best matched rooms
        valid_room = []
        for l in range (0,len(loc)):
            if(loc[l].size >= cur_class.size):
                valid_room.append(l)
        for i in range (0,len(valid_room)):
            for j in range (i+1,len(valid_room)):
                if( loc[valid_room[i]].size > loc[valid_room[j]].size):
                    valid_room[i],valid_room[j] = valid_room[j],valid_room[i]
                    
                    

        
        print(cur_class.name,[loc[room].name for room in valid_room])
        
    #see sister courses time slot
    
    
    # find time
    # assigh location and time to teacher
    # see if teacher can teach at theat time

    
def Simulated_Annealing():
    alpha = .05
    T = .95
    T_min = .05
    randSchedule()
# create a random schedule 


randSchedule()

