"""
MazeDisplay.py
Reads in and displays a maze which can then be solved

by: Tristan Sinclair
"""
import pygame
import copy
import time

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Width and Height per square
WIDTH = 10
HEIGHT = 10


# Space between squares
MARGIN = 1


class Maze:
    def __init__(self, rows, columns, grid):  
        self.rows = rows
        self.columns = columns
        self.grid = grid
    
    def checkMove(self, location):
        if location.row < 0 or location.row > self.rows - 1  or location.column < 0 or location.column > self.columns - 1 or self.grid[location.row][location.column] == 'B':
            return False
        return True

class GridLocation:
    def __init__(self, row, column):
        self.row = row
        self.column = column
    
    def __hash__(self):
        return hash((self.row, self.column))

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.row == other.row and self.column == other.column

def importMaze(filename):
    with open(filename) as f:
        grid = [list(line.rstrip()) for line in f]
    
    rows = len(grid)
    columns = len(grid[0])

    for i in range(len(grid)):
        if len(grid[i]) != columns:
            raise Exception("Maze is improperly formatted") 
    
    maze = Maze(rows, columns, grid)
    return maze

#test = GridLocation(-1, -1)
#maze.checkMove(test)


def solveMaze(maze):
    width = maze.columns
    height = maze.rows

    copiedPath = [] # Stack<GridLocation>
    paths = [] # Queue<Stack<GridLocation>>

    start = GridLocation(0, 0)
    priorLocations = {start}
    path = [start]
    paths.append(path)

    while True:
        path = paths.pop(0)
        location = path[-1]

        # Next Moves
        north = copy.deepcopy(location)
        south = copy.deepcopy(location)
        east = copy.deepcopy(location)
        west = copy.deepcopy(location)

        north.row -= 1
        south.row += 1
        east.column += 1
        west.column -= 1

        moves = [north, south, west, east]

        for move in moves:
            if maze.checkMove(move):
                if move not in priorLocations:
                    copiedPath = copy.deepcopy(path)
                    copiedPath.append(move)
                    if ((move.column == maze.columns - 1) and (move.row == maze.rows - 1)):
                        return copiedPath
                    
                    paths.append(copiedPath)
            priorLocations.add(move)

maze = importMaze("mazetest2.txt")
answer = solveMaze(maze)
print(answer)


def drawMaze(maze, answer):
    for location in answer:
        maze.grid[location.row][location.column] = 'G'
    for row in range(maze.rows):
        for column in range(maze.columns):
            if maze.grid[row][column] == 'W':
                color = WHITE
            elif maze.grid[row][column] == 'B':
                color = BLACK
            elif maze.grid[row][column] == 'G':
                color = GREEN
            elif maze.grid[row][column] == 'S':
                color = GREEN
            elif maze.grid[row][column] == 'F':
                color = GREEN
            pygame.draw.rect(
                screen,
                color,
                [
                    (MARGIN + WIDTH) * column + MARGIN,
                    (MARGIN + HEIGHT) * row + MARGIN,
                    WIDTH,
                    HEIGHT,
                ],
            )
    return


WINDOW_SIZE = [(HEIGHT + MARGIN) * maze.columns + MARGIN, (WIDTH + MARGIN) * maze.rows + MARGIN]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Maze Solver")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            # Set that location to one
            if maze.grid[row][column] == 'W':
                maze.grid[row][column] = 'G'
            else:
                print("Error, space is not available")
            print("Click ", pos, "Grid coordinates: ", row, column)

    # Set the screen background
    screen.fill(WHITE)

    # Draw the grid
    drawMaze(maze, answer)

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.

pygame.quit()