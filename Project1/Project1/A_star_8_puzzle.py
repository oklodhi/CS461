# Omer Khan
# CS 461 Project 1
# Brian Hare

import operator

# class puzzle for puzzle manipulation and processing
class Puzzle:
    def __init__(self):
        # contructor initializes puzzle size and open and closed lists
        self.n = 3
        self.open = []
        self.closed = []
    
    def h(self,state,goal):
        # calculate the manhattan distance of tile
        temp = 0
        temp2 = 0
        for i in range(0,self.n):
            for j in range(0,self.n):
                if state[i][j] != goal[i][j] and state[i][j] != '0':
                    num = int(state[i][j])-1
                    col = int(num/self.n)
                    row = num%self.n
                    temp = abs(i-col)+abs(j-row)
                    temp2 += temp
        return temp2

    def loadFile(self):
    # load and read file that contains the random puzzle starting states
        givenPuzzles = []
        with open('program_1_data.txt', 'r') as fn:
            for line in fn:
                givenPuzzles.append(line.split())
        for i in range (len(givenPuzzles)-1,0,-1):
            if not givenPuzzles[i]:
                del givenPuzzles[i]
        for i in range (len(givenPuzzles)-3,-1,-3):
            givenPuzzles[i]=givenPuzzles[i:i+3]
            del givenPuzzles[i+2]
            del givenPuzzles[i+1]
        print("Loading File Complete\n" )
        return givenPuzzles

    def checkSolvable(self,Puzzle):
    # check if the random puzzle state is solvable by using the mathematical way of 'inversion'
    # even inversion = solvable, odd inversion = unsolvable
        inversion = 0
        # current x location of the tile
        for i in range(len(Puzzle)):
            # current y location of the tile
            for j in range(len(Puzzle[0])):
                # x location of comparison tile     
                for k in range(i,len(Puzzle)):
                    if k == i:
                        start = j
                    else:
                        start = 0
                    # y location of comparison tile
                    for l in range(start,len(Puzzle[0])):          
                        if int(Puzzle[i][j]) > int(Puzzle[k][l]) and int(Puzzle[k][l]) != 0:
                            inversion += 1
        if inversion%2 == 1:
            return False
        return True

    def solvePath(self, grid, n):
    # saves the path from puzzle start state to goal state, if puzzle is solvable, and print solution to a file
        file = open("puzzle_%d_solution.txt" % n, "w")
        
        path = []
        temp = grid
        while(temp !=0):
            path.insert(0,temp)
            temp = temp.parent
        for state in path:
            for x in state.data:
                for y in x:
                    file.write('%s' % y)
                    file.write(' ')
                file.write("\n")
            file.write("\n")
    
    def process(self, Puzzles):
    # main process of the program
    # inputs the puzzles, and checks if each puzzle is solvable or not
        goal = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '0']]
        num = 1
        for i in range (0,len(Puzzles)):
            self.open = []
            self.closed = []
            print("Solving puzzle",i+1, "...")
            start = Puzzles[i]
            for x in start:
                for y in x:
                    print(y,' ',end = '')
                print()
            print()
            if self.checkSolvable(Puzzles[i]):
                start = States(start,0,0,0,0)
                start.huer = self.h(start.data,goal)
                start.fvalue = start.huer + start.level
                # Put the start node in the open list 
                self.open.append(start)
                while True:
                    current = self.open[0]
                    # If distance from current node to next node = 0, then we are at goal state
                    if(self.h(current.data,goal) == 0):
                        break
                    for i in current.generate_child_states():
                        if i.compare(self.closed):
                            pass
                        else:
                            i.huer = self.h(i.data,goal)
                            i.fvalue = i.huer + i.level
                            self.open.append(i)
                    self.closed.append(self.open[0])
                    del self.open[0]

                    # sort the open list based on manhattan distance
                    self.open.sort(key=operator.attrgetter("fvalue","huer"), reverse=False)
                    if(len(self.open) == 0):
                        print('NO SOLUTIONS')
                        break
                print('Solution found!')
                print('Total states visited: ', len(self.closed))
                print('Solution at tree depth:',current.level)
                print('Solution printed to: puzzle_%d_solution.txt' % num)
                self.solvePath(current, num)
                print("\n--------------------------")
            else:
                print("Not Solvable\n--------------------------")
            num+=1

# class states that handle manpulation of the different states of a given puzzle
class States:
    def __init__(self,data,level,fvalue,huer, parent):
    # constructor to set data of the node, level of the node, fvalue for a state, huer to calcualte fvalue, and parent state
        self.data = data
        self.level = level
        self.fvalue = fvalue
        self.huer = huer
        self.parent = parent

    def compare(self, state):
    # compares the current state to a saved state
        for j in state:
            if( self.data == j.data):
                return True
        return False
    
    def generate_child_states(self):
    # generate the children nodes of any given node by moving the blank space up, down, left, right
        x,y = self.find(self.data,'0')
        # value_list contains position values for moving the blank space up, down, left, right
        value_list = [[x, y-1],[x, y+1],[x-1, y],[x+1, y]]
        childrens = []
        for i in value_list:
            child = self.possible_states(self.data,x,y,i[0],i[1])
            if child is not None:
                child_states = States(child,self.level+1,0,0,self)
                childrens.append(child_states)
        return childrens
        
    def possible_states(self,puzzle,x1,y1,x2,y2):
        # check for validity when moving the blank space
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            temp_puzzle = []
            temp_puzzle = self.copy(puzzle)
            temp = temp_puzzle[x2][y2]
            temp_puzzle[x2][y2] = temp_puzzle[x1][y1]
            temp_puzzle[x1][y1] = temp
            return temp_puzzle
        else:
            return None
        
    def copy(self,root):
        # create a copy matrix of given state
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp    
            
    def find(self,puzzle,x):
        # find the [i][j] position of the empty space
        for i in range(0,len(self.data)):
            for j in range(0,len(self.data)):
                if puzzle[i][j] == x:
                    return i,j

# create a puzzle object, load the file, and process the puzzles in file
newPuzzle = Puzzle()
Puzzles = newPuzzle.loadFile() 
newPuzzle.process(Puzzles)
