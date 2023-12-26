#/usr/bin/env python3
# File: Genself.maze
# Original: self.mazeGenerator.py
# Mission: Refactor original to Object Orientation.
'''
Holiday work in progress.
'''
import random

WIDTH = 39 # Width of the self.maze (must be odd).
HEIGHT = 19 # Height of the self.maze (must be odd).
assert WIDTH % 2 == 1 and WIDTH >= 3
assert HEIGHT % 2 == 1 and HEIGHT >= 3
SEED = 1
random.seed(SEED)

ChEMPTY, ChMARK, ChWALL = ' ', '@', 'X'

import enum

class Nsew(enum.Enum):
    NORTH, SOUTH, EAST, WEST = 'n', 's', 'e', 'w'

class Map:
    def __init__(self, width=WIDTH, height=HEIGHT):
        '''Create the filled-in self.maze
        data structure to start. '''
        self.maze = {}
        for x in range(width):
            for y in range(height):
                # Every space is a ChWALL at first.
                self.maze[(x, y)] = ChWALL
        self._width = width
        self._height = height

    
class MapMaker(Map):
    
    def __init__(self, width=WIDTH, height=HEIGHT):
        super().__init__(width, height)
        self.hasvisited = []
        self.unvisitedNeighbors = []
        self.nextIntersection = None
        
    def printmaze(self, xpos=None, ypos=None):
        """
Displays the self.maze data structure in
the self.maze argument. The xpos and ypos
arguments are coordinates of the current
'@' location of the algorithm as it generates
the self.maze.
        """
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if xpos == x and ypos == y:
                    # Display the '@' ChMARK here:
                    print(ChMARK, end='')
                else:
                    # Display the ChWALL or ChEMPTY space:
                    print(self.maze[(x, y)], end='')
            print() # Print a newline after printing the row.


    def visit(self, x, y):
        """"Carve out" ChEMPTY spaces in the self.maze at x, y and then
        recursively move to neighboring unvisited spaces. This
        function backtracks when the ChMARK has reached a dead end."""
        self.maze[(x, y)] = ChEMPTY # "Carve out" the space at x, y.
        #printself.maze(self.maze, x, y) # Display the self.maze as we generate it.
        #print('\n\n')

        while True:
            # Check which neighboring spaces adjacent to
            # the ChMARK have not been visited already:
            self.unvisitedNeighbors = []
            if y > 1 and (x, y - 2) not in self.hasvisited:
                self.unvisitedNeighbors.append(Nsew.NORTH)

            if y < HEIGHT - 2 and (x, y + 2) not in self.hasvisited:
                self.unvisitedNeighbors.append(Nsew.SOUTH)

            if x > 1 and (x - 2, y) not in self.hasvisited:
                self.unvisitedNeighbors.append(Nsew.WEST)

            if x < WIDTH - 2 and (x + 2, y) not in self.hasvisited:
                self.unvisitedNeighbors.append(Nsew.EAST)

            if len(self.unvisitedNeighbors) == 0:
                # BASE CASE
                # All neighboring spaces have been visited, so this is a
                # dead end. Backtrack to an earlier space:
                return
            else:
                # RECURSIVE CASE
                # Randomly pick an unvisited neighbor to visit:
                self.nextIntersection = random.choice(self.unvisitedNeighbors)

                # Move the ChMARK to an unvisited neighboring space:

                if self.nextIntersection == Nsew.NORTH:
                    nextX = x
                    nextY = y - 2
                    self.maze[(x, y - 1)] = ChEMPTY # Connecting hallway.
                elif self.nextIntersection == Nsew.SOUTH:
                    nextX = x
                    nextY = y + 2
                    self.maze[(x, y + 1)] = ChEMPTY # Connecting hallway.
                elif self.nextIntersection == Nsew.WEST:
                    nextX = x - 2
                    nextY = y
                    self.maze[(x - 1, y)] = ChEMPTY # Connecting hallway.
                elif self.nextIntersection == Nsew.EAST:
                    nextX = x + 2
                    nextY = y
                    self.maze[(x + 1, y)] = ChEMPTY # Connecting hallway.

                self.hasvisited.append((nextX, nextY)) # ChMARK as visited.
                self.visit(nextX, nextY) # Recursively visit this space.
    



amap = MapMaker()
# Carve out the paths in the self.maze data structure:
amap.hasvisited = [(1, 1)] # Start by visiting the top-left corner.
amap.visit(1, 1)

# Display the final resulting self.maze data structure:
amap.printmaze()
