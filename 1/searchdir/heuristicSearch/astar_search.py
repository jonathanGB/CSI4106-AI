
from operator import attrgetter
from searchdir.node import *
from searchdir.util import PriorityQueue

## This method must implement A* search
## It must return the solution node and the number of visited nodes
def astar_search(initialState):
    print('A* ------------------------------------')
    root = Node(initialState)
    open_nodes = PriorityQueue(priority_function)
    visited = set() # used to keep track of visited nodes
    open_nodes.enqueue(root)

    while not open_nodes.isEmpty():
        current = open_nodes.dequeue()[2]
        currentHash = current.state.toString() # to be stored in the set of visted nodes

        if current.state.isGoal():
            return current, len(visited)

        if currentHash in visited:
            continue

        visited.add(currentHash)

        for neighbor in current.expand():
            open_nodes.enqueue(neighbor)

    return None, len(visited)

def priority_function(node):
    return node.f