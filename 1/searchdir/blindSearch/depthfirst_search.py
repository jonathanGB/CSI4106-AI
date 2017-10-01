from searchdir.node import *
from searchdir.util import *

## This method must implement depdth-first search (DFS)
## It must return the solution node and the number of visited nodes
def depthfirst_search(initialState):
    print('DFS ----------------------------------')
    root = Node(initialState)
    toVisit = Stack()
    toVisit.push(root)

    return depthfirst_search_rec(toVisit)

def depthfirst_search_rec(toVisit, visitedCtr=0):
    if toVisit.isEmpty():
        return None, visitedCtr

    node = toVisit.pop()
    visitedCtr += 1

    if node.state.isGoal():
        return node, visitedCtr

    if node.isRepeated():
        return depthfirst_search_rec(toVisit, visitedCtr)

    for expanded in node.expand():
        toVisit.push(expanded)

    return depthfirst_search_rec(toVisit, visitedCtr)
