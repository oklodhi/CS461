# Omer Khan
# CS 461 Project 1
# Brian Hare

class Node:
    def __init__(self,data,level,fvalue):
    # Constructor to set data of the node, level of the node and the fvalue
        self.data = data
        self.level = level
        self.fvalue = fvalue
        
    def generate_child_nodes(self):
    # Generate the children nodes of any given node by moving the blank space up, down, left, right
        x,y = self.find(self.data,'0')
    # value_list contains position values for moving the blank space up, down, left, right
        value_list = [[x, y-1],[x, y+1],[x-1, y],[x+1, y]]
        childrens = []
        for i in value_list:
            child = self.shuffle(self.data,x,y,i[0],i[1])
            if child is not None:
                child_node = Node(child,self.level+1,0)
                childrens.append(child_node)
        return childrens
        
    def shuffle(self,puz,x1,y1,x2,y2):
        # Move the blank space in the direction and if the position value is out of place, then return None
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            temp_puz = []
            temp_puz = self.copy(puz)
            temp = temp_puz[x2][y2]
            temp_puz[x2][y2] = temp_puz[x1][y1]
            temp_puz[x1][y1] = temp
            return temp_puz
        else:
            return None
    def copy(self,root):
        # create a copy matrix of given node
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp    
            
    def find(self,puz,x):
        # Find the position of the empty space
        for i in range(0,len(self.data)):
            for j in range(0,len(self.data)):
                if puz[i][j] == x:
                    return i,j
class Puzzle:
    def __init__(self,size):
        # Contructor initializes puzzle size and open and closed lists
        self.n = size
        self.open = []
        self.closed = []
    def accept(self):
        # Accepts the puzzle from the user """
        puz = []
        for i in range(0,self.n):
            temp = input().split(" ")
            puz.append(temp)
        return puz

    # Manhattan Heuristic f(x) = h(x) + g(x)
    def f(self,start,goal):
        # Calculate f(x) hueristic value
        return self.h(start.data,goal)+start.level
    
    def h(self,start,goal):
        # Calculate distance difference
        temp = 0
        for i in range(0,self.n):
            for j in range(0,self.n):
                if start[i][j] != goal[i][j] and start[i][j] != '0':
                    temp += 1
        return temp
    
    def process(self):
        # Accept Start and Goal Puzzle state"""
        print("Enter the start state matrix \n")
        start = self.accept()      
        goal = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '0']]
        print(goal)
        start = Node(start,0,0)
        start.fval = self.f(start,goal)
        # Put the start node in the open list 
        self.open.append(start)
        print("\n\n")
        while True:
            cur = self.open[0]
            print("")
            print("  | ")
            print("  | ")
            print(" \\\'/ \n")
            for i in cur.data:
                for j in i:
                    print(j,end=" ")
                print("")
            # If distance from current node to next node = 0, then we are at goal state
            if(self.h(cur.data,goal) == 0):
                break
            for i in cur.generate_child_nodes():
                i.fval = self.f(i,goal)
                self.open.append(i)
            self.closed.append(cur)
            
            del self.open[0]
            # sort the opne list based on f value
            self.open.sort(key = lambda x:x.fval,reverse=False)

puz = Puzzle(3)
puz.process()
