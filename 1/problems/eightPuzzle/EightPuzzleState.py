### Author: Amal Zouaq
### azouaq@uottawa.ca
## Author: Hadi Abdi Ghavidel
## habdi.cnlp@gmail.com

import numpy as np
import random
from searchdir.blindSearch.breadthfirst_search import *
from searchdir.blindSearch.depthfirst_search import *
from searchdir.heuristicSearch.astar_search import *
from searchdir.state import *


class EightPuzzleState(State):

    #initializes the eight puzzle with the configuration passed in parameter (numbers)
    def __init__(self, numbers):
        self.numbers = numbers
        self.empty_tile = 0      #index of the '0' tile



    #returns a boolean value that indicates if the current configuration is the same as the goal configuration
    def isGoal(self):
        return self.numbers == EightPuzzleState.goal


    # returns the set of legal actions in the current state
    def possibleActions(self):
        # initialize list with indexes to the left, right, top, and bottom of the empty tile index respectively
        possible_actions = [self.empty_tile - 1, self.empty_tile + 1, self.empty_tile - 3, self.empty_tile + 3]
        
        # filter out invalid actions
        actions = [action for action in possible_actions if action >= 0 and action <= 8]
        return actions

    # applies the result of the move on the current state
    def executeAction(self, move):
        self.numbers[self.empty_tile] = self.numbers[move]
        self.numbers[move] = 0
        self.empty_tile = move


    # returns true if the current state is the same as other, false otherwise
    def equals(self, other):
        return self.numbers == other.numbers


    # prints the grid representing the current state
    # e.g. -----------
        # |   | 1 | 2 |
        # -----------
        # | 3 | 4 | 5 |
        # -----------
        # | 6 | 7 | 8 |
        # -----------
    def show(self):
        for i in range(0, 9):
            if i % 3 == 0:
                print("\n ----------- \n|", end='')

            val = str(self.numbers[i])
            if val == "0":
                val = " "

            print(" " + val + " |", end='')

        print("\n ----------- \n", end='')
    # returns the cost of the action in parameter
    def cost(self, action):
        return 1

    # returns the value of the heuristic for the current state
    # note that you can alternatively call heuristic1() and heuristic2() to test both heuristics with A*
    def heuristic(self):
        return self.heuristic1()
        # return self.heuristic2()


    ## returns the value of your first heuristic for the current state
    # make sure to explain it clearly in your comment
    def heuristic1(self):
        pass# TO COMPLETE


    # returns the value of your first heuristic for the current state
    # make sure to explain it clearly in your comment
    def heuristic2(self, matrix, goal):
        pass# TO COMPLETE

EightPuzzleState.goal = [0,1,2,3,4,5,6,7,8]

####################### SOLVABILITY ###########################

def issolvable(puzzle):
    puzzle_str = np.array(list(map(int, puzzle)))
    print("Puzzle string: ", puzzle_str)
    if inversions(puzzle_str) % 2:
        return False
    else : return True

def inversions(s):
    k = s[s != 0]
    return sum(
        len(np.array(np.where(k[i + 1:] < k[i])).reshape(-1))
        for i in range(len(k) - 1)
    )

def randomize(puzzle):
    puzzle = puzzle.shuffle_ran(puzzle, 1)
    puzzle_choice = []
    for sublist in puzzle.cells:
        for item in sublist:
            puzzle_choice.append(item)
    return puzzle, puzzle_choice

    def shuffle_ran(self,board, moves):
        newState = board
        if moves==100:
            return newState
        else:
            newState.executeAction(random.choice(list(board.possibleActions())))
            moves= moves+1
            return self.shuffle_ran(newState, moves)

