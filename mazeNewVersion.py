"""
1st left click:Start node 
2nd left click:End node
3rd left click:making barriers
to remove barrier:righ click on it
"""

import pygame
from queue import PriorityQueue

#Graphic interface of the maze

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH)) #(window)setting up the display(this how the display is gonna be)(WIDTH,WIDTH)is the dimension

pygame.display.set_caption("A* Path Solver")

RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,255,0)
YELLOW=(255,255,0)
WHITE=(255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQUIOISE = (64,224,208)


class Node: #definition and state of the node
    def __init__(self,row,col,width,total_rows): 
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.width = width
        self.color = WHITE
        self.total_rows = total_rows
        self.neighbors = []
    def get_pos(self):
        return self.row,self.col
    """if the node is white we still didnt yet visited it
       if its red we already visited it
       if its a black its a barrier    
       if its orange its start node
       if its turquioise its the end
       if its purple its the right path   
    """
    def is_closed(self):#means have we already visited this node
        return self.color == RED
    def is_open(self):
        return self.colot == GREEN
    def is_barrier(self):
        return self.color == BLACK
    def is_start(self):
        return self.color == ORANGE
    def is_end(self):
        return self.color == TURQUIOISE
    def reset(self):
        self.color = WHITE
    def make_start(self):
        self.color = ORANGE
    def make_closed(self):
        self.color = RED
    def make_open(self):
        self.open = GREEN
    def make_barrier(self):
        self.color = BLACK
    def make_end(self):
        self.color = TURQUIOISE
    def make_path(self):
        self.color = PURPLE
    def draw(self,WIN):#method we use to draw cube on the screen
        pygame.draw.rect(surface=WIN, color=self.color, rect=(self.x,self.y,self.width,self.width)) #to draw a rectangle using pygame library
    def update_neighbors(self,grid):
        self.neighbors=[]
        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_barrier():#DOWN
            self.neighbors.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row-1][self.col].is_barrier():#UP
            self.neighbors.append(grid[self.row-1][self.col])

        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_barrier():#RIGHT
            self.neighbors.append(grid[self.row][self.col+1])

        if self.col >0 and not grid[self.row][self.col-1].is_barrier():#LEFT
            self.neighbors.append(grid[self.row][self.col-1])


    def __lt__(self,other):#(less than)compare two nodes together
        return False #we gonna take that the other node always greater than the this node




def h(p1,p2):#heuristic function(using Manhattan distance)
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1-x2)+abs(y1-y2)


def make_grid(rows,width):#its a data structure that holds all of the nodes to manipulate them
    """how many rows u want in ur grid (row size = col size)
                 and the width how much u want it to be"""
              
    grid = []
    gap = width//rows # the width of each of the cube (integer division)
    for i in range(rows):#the row
        grid.append([])#its gonna make a 2D list
        for j in range(rows):#the column
            spot = Node(row=i, col=j, width=gap, total_rows=rows)
            grid[i].append(spot)#in the grid row i, we add the spot inside of it (list inside of list)
    return grid



def draw_grid(WIN,rows,width):#to draw the grid lines 
    gap = width//rows
    for i in range(rows):
        pygame.draw.line(WIN,GREY,(0,i*gap),(width,i*gap))   #for every raw we gonna draw an horizontal line(last two arguments started line and ended line)
        for j in range(rows):
            pygame.draw.line(WIN,GREY,(j*gap,0),(j*gap,width)) #for every raw we gonna draw a vertical line


def draw(win,grid,rows,width):#main draw function
    win.fill(WHITE)#fills the entire screen with one color(WHITE)

    for row in grid: #grid is a 2D list
        for node in row: 
            node.draw(win) #drawing all of the spots or nodes

    draw_grid(win, rows, width)
    pygame.display.update() #updata things on the display


def get_click_pos(pos,rows,width):#discribe what cube or node we clicked on(which nodes have to change colors when i clicked on it)
                  ###pos is the mouse position
    gap = width // rows
    y,x = pos #mouse coordinates

    row = y//gap
    col = x//gap

    return row,col #the row and col the person clicked on



def reconstract_path(came_from,current,draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


#A* algorithm


def algorithm(draw,grid,start,end):
    open_set = PriorityQueue()
    count = 0
    g_score = {node:float('inf') for row in grid for node in row}
    g_score[start]=0
    came_from ={} #what node came from where 
    f_score = {node:float('inf') for row in grid for node in row}
    f_score[start] = h(start.get_pos(),end.get_pos())

    open_set.put((0,count,start))


    open_set_hash = {start} #same as PeriorityQueue but we can see the nodes inside of it

    



    
   
    

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#if we pressed x icon on the window the game will stop
                pygame.quit()
        currentNode = open_set.get()[2]
        open_set_hash.remove(currentNode)

        if currentNode == end:
            reconstract_path(came_from, end, draw)
            end.make_end()
            return True
        for neighbor in currentNode.neighbors:
            temp_g_score = g_score[currentNode]+1 #we add 1 to the g_score of current because we moved 1 step to it
            if temp_g_score<g_score[neighbor]: #if the next g_score of child node is less than currentNode(better way) we update path
                came_from[neighbor]=currentNode
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(),end.get_pos())
                if neighbor not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if currentNode != start: #if the node we just looked at is not the start node make it red and its not gonna add back to the open set
            currentNode.make_closed()
        

    return False #we didnt find the path












def main(win,width): #the main function
    ROWS = 30 #amount of rows i wanna use
    grid = make_grid(ROWS, width) #generates the grid and gives me 2D array of nodes(spot)

    start = None
    end = None
    #variable to keep track on the start and end position
    run = True 
    #if we run the main loop or not and if we started the algorithm

    while run:
        draw(win=win, grid=grid, rows=ROWS, width=width) #draw every loop 
        for event in pygame.event.get():#each of the starting of the while loop we look at the event that happened(mouse press,keyboard button..)
            if event.type == pygame.QUIT: #check if the event is closing the game(x button on the top-right corner in the screen)
                run = False
            if pygame.mouse.get_pressed()[0]:#if we pressed on the left mouse button(0)
                pos = pygame.mouse.get_pos()
                row,col = get_click_pos(pos, ROWS, width)#row and col of the node(spot) we clicked on
                node = grid[row][col] #gives the node we clicked on
                if not start and node!=end:#if we didnt make the start position yet and we make sure the start isnt the end
                    start = node
                    start.make_start()
                elif not end and node!=start: #if we didnt make an end yet and we make sure the end isnt the start
                    end = node
                    end.make_end()
                elif node!=end and node!=start:
                    node.make_barrier()


            elif pygame.mouse.get_pressed()[2]:#if we pressed on the right mouse button(2)(1 is the middle mouse button)
                pos = pygame.mouse.get_pos()
                row,col = get_click_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()#when we click the node with the right click we reset it to be white
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:#keyboard button pressed
                if event.key == pygame.K_SPACE and start and end:#if space button pressed and we still didnt start the game
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm(lambda: draw(win,grid,ROWS,width),grid,start,end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    pygame.quit() #when we exit the while loop the game stop

 


main(WIN, WIDTH)












