# Omer Khan
# Project 2
# CS461 Brian Hare

from functions import *

# list of professors and the courses they teach
profs = [   Professor("Hare", ["CS101A","CS101B","CS201A","CS201B","CS291A","CS291B","CS303","CS449","CS461"]),
            Professor("Bingham", ["CS101A","CS101B","CS201A","CS201B","CS191A","CS191B","CS291A","CS291B","CS449"]),
            Professor("Kuhail", ["CS303","CS341"]),
            Professor("Mitchell", ["CS191A","CS191B","CS291A","CS291B","CS303","CS341"]),
            Professor("Rao", ["CS291A","CS291B","CS303","CS341","CS461"]),
            Professor("Staff", ["CS101A","CS101B","CS201A","CS201B","CS191A","CS191B","CS291A","CS291B","CS303","CS341","CS449","CS461"])]

# list of times, start time, end time and day of the week
timings = [ Time("10:00", "10:50"),
            Time("11:00", "11:50"),
            Time("12:00", "12:50"),
            Time("13:00", "13:50"),
            Time("14:00", "14:50"),
            Time("15:00", "15:50"),
            Time("16:00", "16:50")]

#list of locations and max room capacity, and also availability of timings
classrooms = [  Location("Haag 301", 70, timings),
                Location("Haag 206", 30, timings),
                Location("Royall 204", 70, timings),
                Location("Katz 209", 50, timings),
                Location("Flarsheim 310", 80, timings),
                Location("Flarsheim 260", 25, timings),
                Location("Bloch 0009", 30, timings)]

# list of courses to be taught and their respective enrollment size
courses_dictionary = [ Course("CS101A", 40),
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

# start simulated annealing and pass in all the above lists for reference
simulated_annealing(courses_dictionary, timings, classrooms, profs)


