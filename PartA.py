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
        self.traveled = []
        # energy is determining whether robot is able to compelte the order
        # time is determining which order robot should take first
        self.active = False

class order:
    #TODO: setup class
    def __init__(self, x, y):
        self.goalX = x
        self.goalY = y
        self.time = 60 # assuming robot moves 1 m/s

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
    #print(goal[0], goal[1])
    x = 0
    for row in grid:
        y = 0 
        for col in row:
            h = abs(goal[0] - x) + abs(goal[1] - y)
            grid[x][y] = h
            y = y + 1
        x = x + 1

    #obstacle add in high heuristic value
    grid[1][2] = 100

def getPath( grid, start, goal): #start is essentially the robot's current position
    R = 4 #4x4 grid
    C = 4 #4x4 grid
    robotX=start[0]
    robotY=start[1]
    path = []
    path.append([robotX, robotY])

    options = []
    isNotAtGoal = True
    while isNotAtGoal:
        #Check right
        if (robotY + 1) < C:
            options.append([robotX, robotY + 1, grid[robotX][robotY + 1]]) #x, y, heuristic value
        #Check down
        if (robotX + 1) < R:
            options.append([robotX + 1, robotY, grid[robotX + 1][robotY]])
        #Check left
        if (robotY - 1) >= 0:
            options.append([robotX, robotY - 1, grid[robotX][robotY - 1]])
        #Check up
        if (robotX - 1) >= 0:
            options.append([robotX- 1, robotY, grid[robotX - 1][robotY]])
        
        #Get minimum
        minH = 10000
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
        path.append([robotX, robotY])
        options.clear()

        #Debug print statement
        #print("Path is:", path, "\tThe goal is:", goal[0], goal[1])

        if ((robotX == goal[0]) and (robotY == goal[1])): #and = &&
            return path

def checkOrders(robot_list):
    delete_list = []
    if(len(order_list) >= 1):
        for orders in order_list:
            #print("Order recieved!", orders.goalX, orders.goalY)
            #TODO: Assign robots the order!
            for bot in robot_list:
                if len(bot.orders) == 0:
                    #Robot has zero orders, give it the order1,1
                    if(bot.active == False):
                        (bot.orders).append(orders)
                        bot.active = True
                        delete_list .append(orders)
                        #calculate heuristic
                        calcHeuristic(grid, [orders.goalX, orders.goalY])
                        #give bot a path
                        bot.path = getPath(grid, [bot.posX, bot.posY], [orders.goalX, orders.goalY])
                        break
                    else:
                        (bot.orders).append(orders)
                        bot.active = True
                        delete_list .append(orders)
                        break
    for obj in delete_list:
        order_list.remove(obj)
    delete_list.clear()
    if(len(order_list) >= 1):
        for orders in order_list:
            #print("Order recieved!", orders.goalX, orders.goalY)
            #TODO: Assign robots the order!
            for bot in robot_list:
                    if len(bot.orders) < 2 and len(bot.orders) > 0: #currently one active robot
                        #TODO: check order's time & robots energy if it can handle new order if so assign robot the order
                        #print('Initial')
                        calcHeuristic(grid, [0, 0])
                        returnInitial = getPath(grid, [bot.posX, bot.posY], [0, 0]) #path to go back home (initial node)
                        #print('previous')
                        calcHeuristic(grid, [(bot.orders[0]).goalX, (bot.orders[0]).goalY])
                        prevOrder = getPath(grid, [0, 0], [(bot.orders[0]).goalX, (bot.orders[0]).goalY]) # prev order from initial node (0,0)                            #print('new order')
                        calcHeuristic(grid, [orders.goalX, orders.goalY])
                        newOrder = getPath(grid, [(bot.orders[0]).goalX, (bot.orders[0]).goalY], [orders.goalX, orders.goalY])
                        #print('direct prev order')
                        calcHeuristic(grid, [(bot.orders[0]).goalX, (bot.orders[0]).goalY])
                        directPrevOrder = getPath(grid, [bot.posX, bot.posY], [(bot.orders[0]).goalX, (bot.orders[0]).goalY]) # current to prev order
                        calcHeuristic(grid,  [0, 0])
                        #print('direct return intial')
                        directReturnInitial = getPath(grid, [(bot.orders[0]).goalX, (bot.orders[0]).goalY], [0, 0]) # prev order to initial state
                        #print('direct new order')
                        #calcHeuristic(grid, [(bot.orders[0]).goalX, (bot.orders[0]).goalY])
                        calcHeuristic(grid, [1, 3])
                        directNewOrder = getPath(grid, [0, 0], [orders.goalX, orders.goalY]) # initial state to new order
                                #s1 = returnInitial + prevOrder + newOrder 
                                #s2 = prevOrder (from current position) + directReturnInitial + directNewOrder
                        s1 = len(returnInitial) + len(prevOrder) + len(newOrder) - 3
                        s2 = len(directPrevOrder) + len(directReturnInitial) + len(directNewOrder) - 3
                        #print("s1:", s1, ", s2:", s2)
                        if s1>s2:
                            s=s2
                            if (bot.energy > (s)) and (orders.time>((len(directReturnInitial) + len(directNewOrder)-2))):  #orderprev_time>length(returninitial+prevorder)
                                (bot.orders).append(orders)
                                delete_list.append(orders)
                                bot.active = True
                                break
                        else:
                            s=s1
                            if (bot.energy > (s)) and (bot.orders[0].time>(len(returnInitial)+len(prevOrder)-2)) and (orders.time>((len(returnInitial)+len(prevOrder)+len(newOrder)-3))):  #orderprev_time>length(returninitial+prevorder)
                                (bot.orders).insert(0,orders)
                                delete_list.append(orders)
                                bot.active = True
                                bot.path = returnInitial
                                break
                            
            for obj in delete_list:
                order_list.remove(obj)
            delete_list.clear()

def move_robots(robot_list):
    for bot in robot_list:
        if bot.active == True: # if bot has order
            #move robot to correct position
            newPos = bot.path[0]
            bot.posX = newPos[0]
            bot.posY = newPos[1]
            bot.traveled.append(bot.path[0])
            (bot.path).pop(0)
            #check if robot has made it to goal destination
            #drain energy and calculate new time for orders
            bot.energy = bot.energy - 1
            for obj in bot.orders:
                obj.time = obj.time - 1

            if len(bot.path) < 1:
                #print(bot.name + " has moved to the location: (" + str(bot.posX) + ", " + str(bot.posY) + ").")
                #print(bot.name + " has arrived at it's destination!")
                print(bot.name + " arrived at it's destination using the path:", bot.traveled)
                bot.traveled.clear()
                if len(bot.orders) > 0:
                    (bot.orders).pop(0)
                #Start next trip or if robot is empty automatically go to (0,0)
                if len(bot.orders) > 0:
                    #start path for next order
                    #calculate heuristic
                    calcHeuristic(grid, [(bot.orders[0]).goalX, (bot.orders[0]).goalY])
                    #give bot a path
                    bot.path = getPath(grid, [bot.posX, bot.posY], [(bot.orders[0]).goalX, (bot.orders[0]).goalY])
                    
                elif (bot.posX == 0) and (bot.posY == 0):
                    bot.active = False
                else:
                    calcHeuristic(grid, [0,0])
                    bot.path = getPath(grid, [bot.posX, bot.posY], [0,0])
                    #print("Bot path after back to start:", bot.path)
            else:
                #display to the user the robot's move (i.e. print statement)
                #print(bot.name + " has moved to the location: (" + str(bot.posX) + ", " + str(bot.posY) + ").")
                pass
        else:
            #Charge robots
            bot.energy = 100 
def main():
    print("Starting part A in ECE 479/579 final project!")
    robot_list = [robot("r1"), robot("r2"), robot("r3")]
    while True:
        print()
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