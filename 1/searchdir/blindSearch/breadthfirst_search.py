from searchdir.node import *
from searchdir.util import *

## This method must implement Breadth-first search (BFS)
## It must return the solution node and the number of visited nodes
def breadthfirst_search(initialState):
    print('BFS------------------------------')
    root = Node(initialState)
    toVisit = Queue()
    toVisit.enqueue(root)

    return breadthfirst_search_rec(toVisit)

def breadthfirst_search_rec(toVisit, visitedCtr=0):
    if toVisit.isEmpty():
        return None, visitedCtr

    node = toVisit.dequeue()
    visitedCtr += 1

    if node.state.isGoal():
        return node, visitedCtr

    if node.isRepeated():
        return breadthfirst_search_rec(toVisit, visitedCtr)

    for expanded in node.expand():
        toVisit.enqueue(expanded)

    return breadthfirst_search_rec(toVisit, visitedCtr)
