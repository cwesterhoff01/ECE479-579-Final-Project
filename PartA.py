import time, threading

#Global variables
order_list = []
grid = [ 
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]
    ]

#Class definitions
class robot:
    def __init__(self, name):
        self.name = name
        self.energy = 100
        self.orders = []
        self.posX = 0
        self.posY = 0
        #path is determined by grid x,y. Values in 2D array represent heuristic values
        self.path = []
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
                # 2, 3
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

def getPath(robot, grid, start, goal): #start is essentially the robot's current position
    R = 4 #4x4 grid
    C = 4 #4x4 grid
    robotX=robot.posX
    robotY=robot.posY
    path = []
    path.append([robotX, robotY])

    options = []
    isNotAtGoal = True
    while isNotAtGoal:
        x = 0
        for i in grid:
            y = 0
            for j in i:
                #Check right
                if (y + 1) < 4:
                    options.append([robotX, robotY + 1, grid[robotX][robotY + 1]]) #x, y, heuristic value
                #Check down
                if (x + 1) < 4:
                    options.append([robot.posX + 1, robot.posY, grid[robot.posX + 1][robot.posY]])
                #Check left
                if (y - 1) >= 0:
                    options.append([robot.posX, robot.posY - 1, grid[robot.posX][robot.posY - 1]])
                #Check up
                if (x - 1) >= 0:
                    options.append([robotX- 1, robotY, grid[robot.posX - 1][robot.posY]])
                
                #Get minimum
                minH = 1000
                minX = 0
                minY = 0
                for z in options:
                    if z[2] < minH: 
                        minH = z[2]
                        minX = z[0]
                        minY = z[1]
                #update move
                robotX = minX
                robotY = minY
                path.append[[robotX, robotY]]
                options.clear()
                y = y + 1
            x = x + 1

def checkOrders(robot_list):
    if(len(order_list) >= 1):
            for orders in order_list:
                print("Order recieved!", orders.goalX, orders.goalY)
                #TODO: Assign robots the order!
                for bot in robot_list:
                    if len(bot.orders) == 0:
                        #Robot has zero orders, give it the order
                        (bot.orders).append(orders)
                        #calculate heuristic
                        calcHeuristic(grid, [orders.goalX, orders.goalY])
                        #give bot a path
                        bot.path = getPath(bot, grid, [bot.posX, bot.posY], [orders.goalX, orders.goalY])
                    else:
                        if len(bot.orders < 2): #currently one active robot
                            #TODO: check order's time & robots energy if it can handle new order if so assign robot the order
                            (bot.orders).append(orders)
                        pass      
            order_list.clear()

def move_robots(robot_list):
    for bot in robot_list:
        if len(bot.orders) > 0: # if bot has order
            #move robot to correct position
            newPos = bot.path[0]
            bot.posX = newPos[0]
            bot.posY = newPos[1]
            (bot.path).pop(0)
            #check if robot has made it to goal destination
                #TODO: #drain energy and calculate new time for orders
            if len(bot.path) < 1:
                print(bot.name + " has arrived at it's destination!")
                delievered = None
                for obj in bot.orders:
                    if (obj.posX == bot.posX) and (obj.posY == bot.posY):
                        delievered = obj
                (bot.orders).remove(delievered)
                #Start next trip or if robot is empty automatically go to (0,0)
                if len(bot.orders) > 0:
                    #start path for next order
                    #calculate heuristic
                    calcHeuristic(grid, [(bot.orders[0]).goalX, (bot.orders[0]).goalY])
                    #give bot a path
                    bot.path = getPath(bot, grid, [bot.posX, bot.posY], [(bot.orders[0]).goalX, (bot.orders[0]).goalY])
                else:
                    #TODO: start order for 0,0
                    pass
            else:
                #display to the user the robot's move (i.e. print statement)
                print(bot.name + " has moved to the location: (" + str(bot.posX) + ", " + str(bot.posY) + ").")
            
def main():
    print("Starting parting A in ECE 479/579 final project")
    robot_list = [robot("r1"), robot("r2"), robot("r3")]
    while True:
        #Delay time to simulate robots moving
        time.sleep(5)
        #Check new orders and assign them to the correct robot
        checkOrders(robot_list)
        #move the robots
        move_robots(robot_list)

if __name__ == "__main__":
    thread = orderThread("Order Thread")
    thread.start()
    main()