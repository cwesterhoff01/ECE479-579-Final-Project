import time, threading

#Global variables
order_list = []

#Class definitions
class robot:
    def __init__(self, name):
        self.name = name
        self.energy = 100
        self.orders = []
        self.posX = 0
        self.posY = 0
        #path is determined by grid x,y. Values in 2D array represent heuristic values

        # energy is determining whether robot is able to compelte the order
        # time is determining which order robot should take first
class order:
    #TODO: setup class
    def __init__(self, x, y):
        self.goalX = x
        self.goalY = y
        self.time = 0 # assuming robot moves 1 m/s

#orderThread
class orderThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        while True:
            #Enter coordinates
                #Example entry
                # 2, 3 fdfsf
            user_input = input()
            cordinates = user_input.split(',')
            newOrder = order(int(cordinates[0]),int(cordinates[1]))
            order_list.append(newOrder)

#Functions
def calcHeuristic(grid, goal):
    print(goal[0], goal[1])
    x = 0
    for row in grid:
        y = 0 
        for col in row:
            h = abs(goal[0] - x) + abs(goal[1] - y)
            grid[x][y] = h
            y = y + 1
        x = x + 1

def checkOrders():
    if(len(order_list) >= 1):
            for orders in order_list:
                print("Order recieved!", orders.goalX, orders.goalY)
                #TODO: Assign robots the order!

            order_list.clear()

def move_robots(robot_list):
    for bot in robot_list:
        if len(bot.orders) > 0:
            print(bot.name, "has move available!")
            #TODO: move robot to correct position
                #drain energy and calculate new time for orders
                #display to the user the robot's move (i.e. print statement)
            #TODO: check if robot has made it to goal destination
                #Start next trip or if robot is empty automatically go to (0,0)

def main():
    print("Starting parting A in ECE 479/579 final project")
    robot_list = [robot("r1"), robot("r2"), robot("r3")]

    grid = [ 
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ]
    while True:
        #Delay time to simulate robots moving
        time.sleep(5)
        #Check new orders and assign them to the correct robot
        checkOrders()
        #move the robots
        move_robots(robot_list)

if __name__ == "__main__":
    thread = orderThread("Order Thread")
    thread.start()
    main()