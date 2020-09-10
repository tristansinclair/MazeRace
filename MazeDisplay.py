"""
MazeDisplay.py
Reads in a maze.txt file, solves the maze, 
and displays the solved maze.

by: Tristan Sinclair
"""
import pygame
import copy
import time

# Colors
BLACK = (0, 0, 0)
WHITE = (250, 250, 250)
GREEN = (0, 220, 0)
# Width and Height per square
WIDTH = 10
HEIGHT = 10
# Space between squares
MARGIN = 1

"""
Maze
Holds grid, row & column data
"""
class Maze:
    def __init__(self, rows, columns, grid):
        self.rows = rows
        self.columns = columns
        self.grid = grid
    # Checks if a move is valid

    def checkMove(self, location):
        if location.row < 0 or location.row > self.rows - 1 or location.column < 0 or location.column > self.columns - 1 or self.grid[location.row][location.column] == 'B':
            return False
        return True


"""
GridLocation
Holds row and column data
Can be used in a set!
"""
class GridLocation:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __hash__(self):
        return hash((self.row, self.column))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.row == other.row and self.column == other.column


"""
Reads in a txt file maze and turns it into a grid
"""


def importMaze(filename):
    with open(filename) as f:
        grid = [list(line.rstrip()) for line in f]

    rows = len(grid)
    columns = len(grid[0])

    # Check maze format
    for i in range(len(grid)):
        if len(grid[i]) != columns:
            raise Exception("Maze is improperly formatted")

    maze = Maze(rows, columns, grid)
    return maze


"""
Takes in maze object and return solution in a stack of GridLocations
"""


def solveMaze(maze):
    width = maze.columns
    height = maze.rows

    copiedPath = []  # Stack<GridLocation>
    paths = []  # Queue<Stack<GridLocation>>

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


# Test run on importing a maze and finding the solution
maze = importMaze("mazetest2.txt")
answer = solveMaze(maze)
print(answer)

"""
Draws the grid into a window.
Takes in a maze file and the answer
"""


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


# Window dimensions
WINDOW_SIZE = [(HEIGHT + MARGIN) * maze.columns + MARGIN,
               (WIDTH + MARGIN) * maze.rows + MARGIN]
screen = pygame.display.set_mode(WINDOW_SIZE)
# Title
pygame.display.set_caption("Maze Solver")
# Until user closes window
done = False
# FPS
clock = pygame.time.Clock()

# Control function
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)

            # else:
            #     print("Error, space is not available")
            # print("Click ", pos, "Grid coordinates: ", row, column)

    # Background
    screen.fill(WHITE)
    # Draw maze
    drawMaze(maze, answer)
    # FPS < 60
    clock.tick(60)

    pygame.display.flip()

pygame.quit()
