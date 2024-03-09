from Algorithms import*
# from image_processing import image_to_matrix
import image_processing
from PIL import Image
from Problem import *
from tkinter import messagebox
import turtle

# defining the variables
start_pos = ()
end_pos = ()
states = []
image_path = ""
maze = []




# Defining the methods that will be used in the code
def get_end_position():
    global end_pos
    timmy.penup()
    messagebox.showinfo("End Position", "Click somewhere to set the goal position")

    def on_click(x, y):
        global end_pos
        print(f"end position at ({x}, {y})")
        end_pos = (x, y)

        my_screen.onclick(None)  # Unbind click event after the first click

    my_screen.onclick(on_click)

def get_start_position():
    global start_pos
    timmy.penup()

    # Show a message box
    messagebox.showinfo("Start Position", "Click somewhere to set the starting position.")

    def on_click(x, y):
        global start_pos
        timmy.setpos(x, y)
        print(f"start position at {timmy.pos()}")
        start_pos = (x, y)

        my_screen.onclick(None)  # Unbind click event after the first click

    my_screen.onclick(on_click)

def translate_x_to_matrix(x_index):
    # this maps the x coordinate back to its position in the matrix
    x_index = (x_index + (width/2)) / movement_size_width
    return round(x_index)

def translate_y_to_matrix(y_index):
    # this maps the y coordinate back to its position in the matrix
    y_index /= movement_size_height
    y_index -= (px_height/2)
    y_index /= -1
    return round(y_index)

def get_start_pos ():
    global start_pos
    # start_pos = (translate_x_to_matrix(start_pos[0]), translate_y_to_matrix(start_pos[1]))
    start_pos = (translate_y_to_matrix(start_pos[1]), translate_x_to_matrix(start_pos[0]))


    return start_pos

def get_end_pos ():
    global end_pos
    # end_pos = (translate_x_to_matrix(end_pos[0]), translate_y_to_matrix(end_pos[1]))
    end_pos = (translate_y_to_matrix(end_pos[1]), translate_x_to_matrix(end_pos[0]))

    return end_pos


def set_x (x_index):
    x_index = (x_index * movement_size_width) - (width/2)
    return x_index

def set_y (y_index):
    y_index = -y_index + (px_height/2)
    # y_index = (y_index * movement_size_height)  + (height/2)
    y_index *= movement_size_height
    return y_index



# start of the code execution
image_path = input("\nEnter the path to the image file:\n")
maze = image_processing.image_to_matrix(image_path)
getMatrix(maze)

matrix_height = len(maze)
matrix_width = len(maze[0])

print("maze height:", matrix_height)
print("maze width:", matrix_width)


timmy = turtle.Turtle()
# setting the properties of the turtle
timmy.resizemode("user")
timmy.shapesize(0.5, 0.5,0)
timmy.shape("square")
timmy.color("dark red")
timmy.pensize(3)
timmy.speed(5)

my_screen = turtle.Screen()
my_screen.listen()
my_screen.bgpic(image_path)
# getting the number of pixels in the width and height of the image
width, height = Image.open(image_path).size    
px_width = round(width / 4)     # the size of the matrix width created from the image
px_height = round(height / 4)
movement_size_width = width / px_width
movement_size_height = height / px_height

my_screen.setup(width=(width + 30), height=(height + 20))
my_screen.screensize(width, height)


# while (maze[start_pos[0]][start_pos[1]] == 0 or maze[end_pos[0]][end_pos[1]] == 0):
while (True):
    get_start_position()
    input("Press enter to continue...")
    get_end_position() 
    input("Press enter to continue...")

    get_start_pos()
    get_end_pos()

    print(f"\n\n\n(main) start pos: {start_pos}")
    print(f"(main) end pos: {end_pos} \n\n\n")
    print(f"\n\n\nStart position: {start_pos}")
    print(f"Goal position: {end_pos} \n\n\n")

    if (start_pos[0] > matrix_height or start_pos[0] < 0 or start_pos[1] > matrix_width or start_pos[1] < 0):
        print(f"Start position {start_pos} is out of bounds")
        print("Try again!")
    elif (end_pos[0] > matrix_height or end_pos[0] < 0 or end_pos[1] > matrix_width or end_pos[1] < 0):
        print(f"End position {end_pos} is out of bounds")
        print("Try again!")
    elif (maze[start_pos[0]][start_pos[1]] == 0):
        print(f"Start position {start_pos} is on a wall")
        print("Try again!")
    elif (maze[end_pos[0]][end_pos[1]] == 0):
        print(f"End position {end_pos} is on a wall")
        print("Try again!")
    else:
        break
    

# timmy.setpos(set_x(2), set_y(0)) # setting the starting position
timmy.up()

valid_choice = False

while (not valid_choice):
    global Depth, Cost, Num_expanded
    valid_choice = True

    algorithm_choice = input( "\nAlgorithm Options:\n 1. BFS\n 2. DFS\n 3. Greedy\n 4. A*\n 5. Weighted A*\n 6. UCS\n 7. Beam\n" + 
                         "Which algorithm would you like to use to solve the maze? Enter one of the numbers:\n")
    

    maze_problem = Maze(start_pos, [end_pos])
    if (algorithm_choice == 1 or algorithm_choice == "1"):

        print("BFS chosen")
        temp = BFS(maze_problem)
        
        Depth = temp.depth
        Cost = temp.path_cost
        Num_expanded = get_num_expanded()

        while temp.parent != None:
            states.append(temp.state)
            temp = temp.parent

        states.reverse()

        
        
    elif (algorithm_choice == 2 or algorithm_choice == "2"):
        print("DFS chosen")
        temp = DFS(maze_problem)

        Depth = temp.depth
        Cost = temp.path_cost
        Num_expanded = get_num_expanded()

        while temp.parent != None:
            states.append(temp.state)
            temp = temp.parent

        states.reverse()
        
        # states = run_dfs(maze, start_pos, end_pos)[0]

        # dfs_algorithm = DFS(maze, start_pos, end_pos)
        # states = dfs_algorithm.states
    elif (algorithm_choice == 3 or algorithm_choice == "3"):
        print("Greedy chosen")
        
        while (True):
            heirstic_choice = input("\n\nHeuristic Options:\n 1. Manhattan\n 2. Equalidian\n" + 
            "Which heurisitic function would like to use? Enter a number:\n")

            if (heirstic_choice == "1"):
                temp = greedyManh_search(maze_problem)

                Depth = temp.depth
                Cost = temp.path_cost
                Num_expanded = get_num_expanded()

                while temp.parent != None:
                    states.append(temp.state)
                    temp = temp.parent

                states.reverse()
                
                break
            elif (heirstic_choice == "2"):
                temp = greedyEucl_search(maze_problem)
                
                Depth = temp.depth
                Cost = temp.path_cost
                Num_expanded = get_num_expanded()

                while temp.parent != None:
                    states.append(temp.state)
                    temp = temp.parent

                states.reverse()

                break
            else:
                print("Invalid value for heuristic choice. Try again!")
        
    elif (algorithm_choice == 4 or algorithm_choice == "4"):
        print("A* chosen")
        while (True):
            heirstic_choice = input("\n\nHeuristic Options:\n 1. Manhattan\n 2. Equalidian\n" + 
            "Which heurisitic function would like to use? Enter a number:\n")

            if (heirstic_choice == "1"):
                temp = A_starManh(maze_problem)

                Depth = temp.depth
                Cost = temp.path_cost
                Num_expanded = get_num_expanded()

                while temp.parent != None:
                    states.append(temp.state)
                    temp = temp.parent

                states.reverse()

                break
            elif (heirstic_choice == "2"):
                temp = A_starEucl(maze_problem)
                
                Depth = temp.depth
                Cost = temp.path_cost
                Num_expanded = get_num_expanded()

                while temp.parent != None:
                    states.append(temp.state)
                    temp = temp.parent

                states.reverse()

                break
            else:
                print("Invalid value for heuristic choice. Try again!")

    elif (algorithm_choice == 5 or algorithm_choice == "5"):
        print("Weighted A* chosen")
        while (True):
            heirstic_choice = input("\n\nHeuristic Options:\n 1. Manhattan\n 2. Equalidian\n" + 
            "Which heurisitic function would like to use? Enter a number:\n")

            weight = (float)(input("\nEnter a weight for the heuristic:\n"))

            if (heirstic_choice == "1"):
                temp = weightedA_starManh(maze_problem, weight)

                Depth = temp.depth
                Cost = temp.path_cost
                print(get_num_expanded())
                Num_expanded = get_num_expanded()

                while temp.parent != None:
                    states.append(temp.state)
                    temp = temp.parent

                states.reverse()

                break
            elif (heirstic_choice == "2"):
                temp = weightedA_starEucl(maze_problem, weight)

                Depth = temp.depth
                Cost = temp.path_cost
                Num_expanded = get_num_expanded()

                while temp.parent != None:
                    states.append(temp.state)
                    temp = temp.parent

                states.reverse()
                
                

                break
            else:
                print("Invalid value for heuristic choice. Try again!")

    elif (algorithm_choice == 6 or algorithm_choice == "6"):
        print("UCS chosen")
        temp = UCS(maze_problem)
        
        Depth = temp.depth
        Cost = temp.path_cost
        Num_expanded = get_num_expanded()

        while temp.parent != None:
            states.append(temp.state)
            temp = temp.parent

        states.reverse()

    
    elif (algorithm_choice == 7 or algorithm_choice == "7"):
        print("Beam chosen")
        while (True):
            heirstic_choice = input("\n\nHeuristic Options:\n 1. Manhattan\n 2. Equalidian\n" + 
            "Which heurisitic function would like to use? Enter a number:\n")

            weight = (int)(input("\nEnter a frontier limit:\n"))

            if (heirstic_choice == "1"):
                temp = beam_searchManh(maze_problem, weight)
                
                Depth = temp.depth
                Cost = temp.path_cost
                Num_expanded = get_num_expanded()

                while temp.parent != None:
                    states.append(temp.state)
                    temp = temp.parent

                states.reverse()

                break
            elif (heirstic_choice == "2"):
                temp = beam_searchEucl(maze_problem, weight)
                
                Depth = temp.depth
                Cost = temp.path_cost
                Num_expanded = get_num_expanded()

                while temp.parent != None:
                    states.append(temp.state)
                    temp = temp.parent

                states.reverse()

                break
            else:
                print("Invalid value for heuristic choice. Try again!")

    else:
        print("Invalid Value for algorithm choice. Try again!")
        valid_choice = False

    

print(states)
timmy.pendown()
for state in (states):
    # print("originl:", state)
    timmy.setpos(set_x(state[1]), set_y(state[0]))
    # print("mutated: (", set_y(state[0]), ", ", set_x(state[1]), ")")


# my_screen.exitonclick()
turtle.mainloop()

print("\n----------------------")
print(f"Goal is at depth: {Depth}")
print(f"The path cost is: {Cost}")
print(f"The number of expanded nodes is:{Num_expanded}\n\n")