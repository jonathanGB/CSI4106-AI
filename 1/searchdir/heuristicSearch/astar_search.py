
from operator import attrgetter
from searchdir.node import *
from searchdir.util import PriorityQueue

## This method must implement A* search
## It must return the solution node and the number of visited nodes
def astar_search(initialState):
    print('A* ------------------------------------')
    root = Node(initialState)
    open_nodes = PriorityQueue(priority_function)
    visitedCtr = 0
    open_nodes.enqueue(root)
    while not open_nodes.isEmpty():
        current = open_nodes.dequeue()[2]
        visitedCtr += 1
        if current.state.isGoal():
            return current, visitedCtr

        for neighbor in current.expand():
            cost = current.g + 1
            if neighbor.isRepeated():
                continue
            open_nodes.enqueue(neighbor)

def priority_function(node):
    return node.f