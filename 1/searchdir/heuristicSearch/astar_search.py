
from operator import attrgetter
from searchdir.node import *
from searchdir.util import PriorityQueue

## This method must implement A* search
## It must return the solution node and the number of visited nodes
def astar_search(initialState):
    print('A* ------------------------------------')
    root = Node(initialState)
    open_nodes = PriorityQueue(priority_function)
    visited = {}
    open_nodes.enqueue(root)
    while not open_nodes.isEmpty():
        current = open_nodes.dequeue()[2]

        if current.state.isGoal():
            return current, len(visited)

        visited[current.state.toString()] = True

        for neighbor in current.expand():
            if neighbor.state.toString() in visited:
                continue

            open_nodes.enqueue(neighbor)

def priority_function(node):
    return node.f