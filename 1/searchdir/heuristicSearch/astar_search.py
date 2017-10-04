
from operator import attrgetter
from searchdir.node import *
from searchdir.util import PriorityQueue

## This method must implement A* search
## It must return the solution node and the number of visited nodes
def astar_search(initialState):
    print('A* ------------------------------------')
    root = Node(initialState)
    open_nodes = PriorityQueue(priority_function)
    closed = []
    visitedCtr = 0
    open_nodes.enqueue(root)
    while not open_nodes.isEmpty():
        current = open_nodes.dequeue()
        visitedCtr += 1
        if current.state.isGoal():
            return current, visitedCtr
        closed.append(current)
        for neighbor in node.expand():
            cost = current.g + 1
            if open_nodes.__contains__(neighbor) and cost < neighbor.getcost():
                open_nodes.remove(neighbor)
            if not open_nodes.__contains__(neightbor) and not neighbor in closed:
                open_nodes.enqueue(neighbor)

def priority_function(node):
    return node.state.f