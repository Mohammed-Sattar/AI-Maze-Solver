from image_processing import *
from Problem import *

reached = []  # reached table
states = []  # contains the sequence of states that lead to the goal
frontierMaxSize = 0  # to store the maximum size of the frontier
num_expanded=0

def get_num_expanded():
    return num_expanded

def BFS(problem):  # breadth-first search
    global frontierMaxSize, reached, num_expanded
    node = Node(problem.initial)  # root node
    if problem.isGoal(node.state):  # goal test
        return node
    frontier = Frontier("FIFO")  # create a FIFO queue as a frontier
    frontier.push(node)  # add root to frontier
    reached = [problem.initial]  # add root to reached
    while not frontier.isEmpty():  # repeat until the frontier is empty
        if frontierMaxSize < frontier.size():  # for retrieving the maximum frontier size
            frontierMaxSize = frontier.size()
        node = frontier.pop()  # dequeue a node
        num_expanded+=1
        for child in expand(problem, node):  # repeat for each possible successor of this node
            s = child.state
            if problem.isGoal(s):  # goal test (early checking)
                return child
            if not s in reached:  # if the child has not been visited yet, add it to both frontier and reached
                reached.append(s)
                frontier.push(child)
    return "Failure"  # when no solution is found


# def DLS(problem, L):
#     global reached,frontierMaxSize
#     node = Node(problem.initial)
#     frontier = Frontier("LIFO")
#     frontier.push(node)
#     reached = [problem.initial]
#     result="Failure"
#     while not frontier.isEmpty():
#         if frontierMaxSize<frontier.size():
#             frontierMaxSize=frontier.size()
#         node = frontier.pop()
#         if problem.isGoal(node.state): return node
#         if node.depth > L: return "cuttoff"
#         for child in expand(problem, node):
#             s = child.state
#             if not s in reached:
#                 reached.append(s)
#                 frontier.push(child)
#
#     return result
# def ID(problem):
#     for L in range(sys.maxsize):
#         result=DLS(problem,L)
#         if result!="cuttoff": return result


def best_first_search(problem, f, weight=1,
                      lim=sys.maxsize):  # takes the problem as well as an evaluation function along with a "weight" (for special use)
    global frontierMaxSize, reached ,num_expanded
    node = Node(state=problem.initial)  # root node
    node.evaluation = f(problem, node, weight)  # assign a priority according to some evaluation function f
    frontier = Frontier("Priority")  # create a priority queue as a frontier
    frontier.push(node, node.evaluation)  # enqueue the root
    reached = {problem.initial: node}  # add the intial as key and root as a value
    while not frontier.isEmpty():  # repeat until the frontier is empty
        if (frontier.size() > lim):  # for beam searcn , limit is set to infinity by default
            frontier = limitFron(frontier, lim)
        if frontierMaxSize < frontier.size():  # for retrieving the maximum frontier size
            frontierMaxSize = frontier.size()
        node = frontier.pop()[1]  # it is stored in the priority queue as (priority,node) that is why we take index 1
        num_expanded+=1
        print(get_num_expanded())
        if problem.isGoal(node.state): return node  # goal test
        for child in expand(problem, node):  # repeat for each possible successor of this node
            s = child.state
            child.evaluation = f(problem, node,
                                 weight)  # assign a priority to the child along with a "weight" (in most cases 1)
            if not s in reached or child.path_cost < reached[
                s].path_cost:  # a condition to make sure the mapping state:node is the shortest onw
                reached[s] = child  # if the state is not in reahched or the new child has a shorter path
                frontier.push(child, child.evaluation)

    return "Failure"  # return failure if no solution is found


def greedyManh_search(problem):  # greedy search that uses Manhattan heuristic
    return best_first_search(problem, ManhattanHeuristic)


def greedyEucl_search(problem):  # greedy search that uses Euclidean heuristic
    return best_first_search(problem, EuclideanHeuristic)


def A_starManh(problem):  # A* search that uses Manhattan heuristic
    return best_first_search(problem, A_starManhHeuristic)


def A_starEucl(problem):  # A* search that uses Euclidean heuristic
    return best_first_search(problem, A_starEuclHeuristic)


def weightedA_starManh(problem, w):  # Weighted A* search that uses Manhattan heuristic
    return best_first_search(problem, A_starManhHeuristic, w)


def weightedA_starEucl(problem, w):  # Weighted A* search that uses Euclidean heuristic
    return best_first_search(problem, A_starEuclHeuristic, w)


def UCS(problem):  # Uniform cost search
    return best_first_search(problem, cost)


def beam_searchManh(problem, lim):  # beam serach with Manhattan heuristic
    return best_first_search(problem, f=A_starManhHeuristic, lim=lim)


def beam_searchEucl(problem, lim):  # beam search with Euclidean heuristic
    return best_first_search(problem, f=A_starEuclHeuristic, lim=lim)


def DFS(problem):  # depth-first search (can be implemented as best-first search with minus depth as
    # an evaluation function)
    return best_first_search(problem, minusDepth)
# temp=BFS(maze) #21
# temp=greedyEucl_search(maze) #576
# temp=greedyManh_search(maze) #580
# temp=A_starEucl(maze) #47
# temp=A_starManh(maze) #68
# temp=weightedA_starEucl(maze,1.4) #91
# temp = weightedA_starManh(maze,1.4) #189
# temp=beam_searchEucl(maze,40)
# temp = UCS(maze)
# print(temp.depth)
# print(frontierMaxSize)
# while temp.parent != None:
#     states.append(temp.state)
#     temp = temp.parent
#
# states.reverse()
# # Agent_actions.reverse()
# # for i in Agent_actions:
# #     print(i)
# print(states)
