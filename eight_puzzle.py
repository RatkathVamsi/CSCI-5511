#Sri Krishna Vamsi Koneru, koner033@umn.edu, 5881358
import time

#classes
class Problem:

    def __init__(self, initial, goal,heuristic_function):
        self.initial = initial
        self.goal = goal
        self.heuristic_function= heuristic_function

    def find_zero_tile(self, state):
        return state.index(0)

    def actions(self, state):
        allowed_actions = ['U', 'D', 'L', 'R']
        blank_index = self.find_zero_tile(state)

        if blank_index % 3 == 0:
            allowed_actions.remove('R')
        if blank_index < 3:
            allowed_actions.remove('D')
        if blank_index % 3 == 2:
            allowed_actions.remove('L')
        if blank_index > 5:
            allowed_actions.remove('U')

        return allowed_actions

   

    def result(self, state, action):
        blank = self.find_zero_tile(state)
        new_state = list(state)

        delta = {'D': -3, 'U': 3, 'R': -1, 'L': 1}
        neighbor = blank + delta[action]
        new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

        return list(new_state)

    def goal_check(self, state):
        return state == self.goal
    
    def path_cost(self, c, state1, action, state2):
        return c + 1
    
    
    def h(self, node):
        if self.heuristic_function=='manhattan_distance':
            dist=0
            for i in range (0,9):
                    if node.state[i]!=0:
                        if i!=0:
                            row1,col1= divmod(node.state.index(i),3)
                            row2,col2=divmod(self.goal.index(i),3)
                            dist+=abs(row1-row2)+abs(col1-col2)
         
            return dist
        
        elif self.heuristic_function=='num_wrong_tiles':
            const=0
            for i in range(0,9):
                if node.state[i]!=0:
                    if node.state[i]!=self.goal[i]:
                        const+=1
            return const
        else:
            print("Invalid heuristic function")

#Heuristics
def num_wrong_tiles(problem):
    const=0
    for i in range(0,9):
        if problem.initial[i]!=0:
            if problem.initial[i]!=problem.goal[i]:
                const+=1
    return const

def manhattan_distance(problem):
    dist=0
    for i in range (0,9):
        if problem.initial[i]!=0:
            if i!=0:
                   row1,col1= divmod(problem.initial.index(i),3)
                   row2,col2=divmod(problem.goal.index(i),3)
                   dist+=abs(row1-row2)+abs(col1-col2)
         
    return dist


class Node:

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        if parent is not None:
            self.depth = parent.depth + 1
        else:
            self.depth=0


    def expand(self, problem):
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        return [node.action for node in self.path()[1:]]

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

#bfs
def breadth_first(problem):
  
    frontier = [Node(problem.initial)]
    reached=set()

    while frontier:
        node = frontier.pop(0)
        if problem.goal_check(node.state):
            return node
        
        state_tuple=tuple(node.state)
        if state_tuple not in reached:
            reached.add(state_tuple)
            frontier.extend(node.expand(problem))
    return None

#iterative_deepening
def depth_first_search(problem):
   
    frontier = [Node(problem.initial)] 

    while frontier:
        node = frontier.pop()
        if problem.goal_check(node.state):
            return node
        frontier.extend(node.expand(problem))
    return None

def depth_limited_search(problem, limit=50):

    def dls(node, problem, limit=50):
        if problem.goal_check(node.state):
            return node
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                result = dls(child, problem, limit - 1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else None

    return dls(Node(problem.initial), problem, limit)

def iterative_deepening(problem):
    d_limit = 0
    while True:
        result = depth_limited_search(problem, d_limit)
        if result != 'cutoff':
            return result
        d_limit += 1

#a* 
def astar(problem):
    open_set = []
    closed_set = set()

    initial_node = Node(problem.initial)
    initial_node.path_cost = 0
    initial_node.heuristic = problem.h(initial_node)
    open_set.append(initial_node)

    while open_set:
        open_set.sort(key=lambda node: node.path_cost + node.heuristic)  

        current_node = open_set.pop(0)

        if problem.goal_check(current_node.state):
            return current_node.solution()

        closed_set.add(tuple(current_node.state))

        for child_action in problem.actions(current_node.state):
            child_state = problem.result(current_node.state, child_action)

            if tuple(child_state) in closed_set:
                continue

            child_node = Node(child_state)
            child_node.parent = current_node
            child_node.action = child_action
            child_node.path_cost = current_node.path_cost + problem.path_cost(current_node.path_cost, current_node.state, child_action, child_state)
            child_node.heuristic = problem.h(child_node)

            if not any(node.state == child_state and node.path_cost <= child_node.path_cost for node in open_set):
                open_set.append(child_node)

    return None

#state representation
def visualize(node):
    v=node.state
    for i in range(3):
        for j in range(3):
            print(v[i * 3 + j],end=" ")
        print()
    print()

 #main       
def main():
    lst=[]
    trz=str(input("Enter number"))
    lst=[int(x) for x in str(trz)]
    
    
    l=len(lst)
    if(l==9):
        goal=[1,2,3,8,0,4,7,6,5]

        problem= Problem(lst,goal,heuristic_function="num_wrong_tiles")
        problem1=Problem(lst,goal,heuristic_function='manhattan_distance')
        
        initial_state= problem.initial
        viz=Node(initial_state)
        visualize(viz)
        s_time=time.time()
        bfs=breadth_first(problem)
        e_time=time.time() - s_time
        print(f"{bfs.solution()}\n The time taken for bfs is {e_time} seconds")
        s_time=time.time()
        idp=iterative_deepening(problem)
        e_time=time.time()
        ex_time=e_time-s_time
        print(f"{idp.solution()}\n Iterative deepening took {ex_time} seconds")
        s_time=time.time()
        out=astar(problem)
        e_time=time.time() - s_time
        print(f"{out}\n A* using num_wrong_tiles took {e_time} seconds")
        s_time=time.time()
        out1=astar(problem1)
        e_time=time.time() - s_time
        print(f"{out1}\n A* using manhattan_distance took {e_time} seconds")

    else:
        print("check and enter the matrix again")

if __name__ == "__main__":

    main()

#I referenced the github code for class structure and took help while implementing the methods