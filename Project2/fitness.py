        for c in self.courses:
            # taught by instructor or staff
            if c.instructor.name == "Staff":
                self.fitness += 1
            elif c.name in c.instructor.courses:
                self.fitness += 3
            # if room size is twice enrollment
            if (c.place.size >= c.size):
                self.fitness += 5
                if( 2*c.place.size <= c.size):
                    self.fitness += 2
        # if instructor teaching more than 4 courses\
        num_profs = [0]*(len(self.profs))
        for c in self.courses:
            for p in range(0,len(self.profs)-1):
                if c.instructor.name == self.profs[p].name:
                    num_profs[p] += 1
        for p in num_profs:
            if p > 4:
                self.fitness -= 5*(p-4)
        # Rao or Mitchell vs Hare or Bingham
        if (num_profs[3]) > (num_profs[0]) or \
           (num_profs[3]) > (num_profs[1]) or \
           (num_profs[4]) > (num_profs[0]) or \
           (num_profs[4]) > (num_profs[1]):
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
            if self.classrooms[0].time[t].start == self.courses[2].time.start:
                index1 = t
                break
        index2 = 0
        for t in range(0,len(self.classrooms[3].time)):
            if self.classrooms[0].time[t].start == self.courses[3].time.start:
                index2 = t
                break
        index3 = 0
        for t in range(0,len(self.classrooms[6].time)):
            if self.classrooms[0].time[t].start == self.courses[6].time.start:
                index3 = t
                break
        index4 = 0
        for t in range(0,len(self.classrooms[0].time)):
            if self.classrooms[0].time[t].start == self.courses[7].time.start:
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
