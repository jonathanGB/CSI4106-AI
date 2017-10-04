from searchdir.node import *
from searchdir.util import *

## This method must implement Breadth-first search (BFS)
## It must return the solution node and the number of visited nodes
def breadthfirst_search(initialState):
    print('BFS------------------------------')
    root = Node(initialState)
    visitedCtr = 0
    toVisit = Queue()
    toVisit.enqueue(root)

    while not toVisit.isEmpty():
        node = toVisit.dequeue()
        visitedCtr += 1

        if node.state.isGoal():
            return node, visitedCtr

        if node.isRepeated():
            continue

        for expanded in node.expand():
            toVisit.enqueue(expanded)

    return None, visitedCtr