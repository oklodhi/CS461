# class courses that keeps track of each course thats taught and its respective enrollment size
class Course:
    courses = None

    def __init__(self, name, size):
        self.name = name
        self.size = size

    @staticmethod
    def find(name):
        for i in range(len(Course.courses)):
            if Course.courses[i].name == name:
                return i
        return -1

    def __repr__(self):
        return "Course: " + self.name + ", Size: " + str(self.size)

# class professor that keeps track of each professor and the respective course they teach
class Professor:
    professors = None

    def __init__(self, name, course):
        self.name = name
        self.course = course

    @staticmethod
    def find(name):
        for i in range(len(Professor.professors)):
            if Professor.professors[i].name == name and Professor.professors[i].course == course:
                return i
        return -1

    def __repr__(self):
        return "Professor: " + self.name

# class location that keeps track of building and room number and its respective seats available in class
class Location:
    locations = None

    def __init__(self, name, size):
        self.name = name
        self.size = size

    @staticmethod
    def find(name):
        for i in range(len(Location.locations)):
            if Location.locations[i].name == name:
                return i
        return -1

    def __repr__(self):
        return "Location: " + self.name + " Size: " + str(self.size)

# class time that keeps track of class start and end times and days of class
class Time:
    timing = None

    def __init__(self, start, end, day):
        self.start = start
        self.end = end
        self.day = day

    def __repr__(self):
        return "Time: " + self.start + "-" + self.end + " Day: " + self.day
