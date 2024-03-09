import math
import queue as q
import sys

from image_processing import matrix
matrix=[]
def getMatrix(maz):
    global matrix
    matrix=maz


class Node:  # The node object will store all the data needed
    count = 0  # shared variable to keep track of the number of nodes created

    def __init__(self, state, parent=None, cost=0, action=None, priority=sys.maxsize, depth=0):
        self.state = state
        self.parent = parent
        self.path_cost = cost
        self.action = action
        self.evaluation = priority
        self.depth = depth
        Node.count += 1
        self.Num = Node.count  # to keep track of the order of generation

    def __lt__(self, other):  # When the valuation function gives the same priority to more than one node
        if self.evaluation == other.evaluation:  # it prioritizes the node generated first
            return self.Num < other.Num
        return self.evaluation < other.evaluation


class Problem:  # a class to formulate the problem. This will not be used, rather inherited from
    def __init__(self, init, goals):
        self.initial = init
        self.goal = goals

    def isGoal(self, state):  # goal test
        return state in self.goal

    def Actions(self, state):  # Applicable actions
        pass

    def Results(self, state, action):  # transition module
        pass

    def Action_Cost(self, state, action, next_state):  # path cost
        pass


class Frontier:  # to store the nodes during search
    def __init__(self, type):  # adaptive to any type of queue
        if type == "FIFO":
            self.queue = q.Queue()
        elif type == "LIFO":
            self.queue = q.LifoQueue()
        elif type == "Priority" or type == "priority":
            self.queue = q.PriorityQueue()

    def pop(self):
        return self.queue.get()

    def push(self, x,
             priority=sys.maxsize):  # priority is set to infinity to ensure that this method can be used with LIFO
                                    # and FIFO
        if priority == sys.maxsize:
            self.queue.put(x)
        else:
            self.queue.put((priority, x))

    def isEmpty(self):
        return self.queue.empty()

    def isFull(self):
        return self.queue.full()

    def size(self):
        return self.queue.qsize()


# below are all the actions that the agent can do. These actions simply modify the state by adding or subtracting
# from the coordinates
def north(pos):
    pos = list(pos)
    pos[0] -= 1
    return tuple(pos)


def south(pos):
    pos = list(pos)
    pos[0] += 1
    return tuple(pos)


def east(pos):
    pos = list(pos)
    pos[1] += 1
    return tuple(pos)


def west(pos):
    pos = list(pos)
    pos[1] -= 1
    return tuple(pos)


def north_east(pos):
    return north(east(pos))


def north_west(pos):
    return north(west(pos))


def south_east(pos):
    return south(east(pos))


def south_west(pos):
    return south(west(pos))


def expand(problem, node):  # yields a child
    s = node.state
    for action in problem.Actions(s):  # repeat for every applicable action on state
        sdash = problem.Result(s, action)
        cost = node.path_cost + 1
        depth = node.depth + 1
        # get the new state,cost, and depth and pass all the data to yield a new node
        yield Node(state=sdash, parent=node, action=action, cost=cost, depth=depth)


class Maze(Problem):  # a subclass of problem to override the unimplemented methods
    def __init__(self, init, goals):
        super().__init__(init, goals)

    def Actions(self, state):
        actions = []  # to store the applicable actions
        for i in (north, south, east, west):
            try:
                x, y = i(state)
                if matrix[x][y] == 1:  # check if the resulted coordinates corresponds to a wall (0) or an open path (1)
                    actions.append(i)  # add to actions if not a wall
            except:  # in case there is an outOfBound exception
                pass
        # if north and east are possible then so is north_east, and the same applies for all diagonal actions
        if north in actions:
            if east in actions:
                actions.append(north_east)
            elif west in actions:
                actions.append(north_west)
        elif (south in actions):
            if east in actions:
                actions.append(south_east)
            elif west in actions:
                actions.append(south_west)

        return actions

    def Result(self, state, action):  # return a new state after applying an action on the original one
        return action(state)

    def Action_Cost(self, state, action, next_state):
        return 1  # the cost is 1 for all actions


maze = Maze((0, 2), [(29, 47)])


def ManhattanHeuristic(maze,node, weight=1):
    goal_x_coordinate = maze.goal[0][0]
    goal_y_coordinate = maze.goal[0][1]
    state_x_coordinate = node.state[0]
    state_y_coordinate = node.state[1]
    resultX = abs(state_x_coordinate - goal_x_coordinate)  # absolute value used to element any negatives
    resultY = abs(state_y_coordinate - goal_y_coordinate)
    result = resultX + resultY
    return result * weight


def EuclideanHeuristic(maze,node, weight=1):
    goal_x_coordinate = maze.goal[0][0]
    goal_y_coordinate = maze.goal[0][1]
    state_x_coordinate = node.state[0]
    state_y_coordinate = node.state[1]
    resultX = (state_x_coordinate - goal_x_coordinate) ** 2
    resultY = (state_y_coordinate - goal_y_coordinate) ** 2
    result = math.sqrt(resultX + resultY)
    return result * weight


def A_starEuclHeuristic(maze,node, weight=1):
    return node.path_cost + EuclideanHeuristic(maze,node, weight)


def A_starManhHeuristic(maze,node, weight=1):
    return node.path_cost + ManhattanHeuristic(maze,node, weight)
def limitFron(fron,lim):
    newfron=Frontier("Priority")
    for i in range(lim):
        element=fron.pop()
        node=element[1]
        priority=element[0]
        newfron.push(node,priority)
    return newfron

def minusDepth(problem,node, w=1):
    return -node.depth

def cost(problem,node,w=1):
    return node.path_cost