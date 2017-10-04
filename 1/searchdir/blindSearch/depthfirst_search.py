from searchdir.node import *
from searchdir.util import *

## This method must implement depdth-first search (DFS)
## It must return the solution node and the number of visited nodes
def depthfirst_search(initialState):
    print('DFS ----------------------------------')
    root = Node(initialState)
    visitedCtr = 0
    toVisit = Stack()
    toVisit.push(root)

    while not toVisit.isEmpty():
        node = toVisit.pop()
        visitedCtr += 1

        if node.state.isGoal():
            return node, visitedCtr

        if node.isRepeated():
            continue

        for expanded in node.expand():
            toVisit.push(expanded)

    return None, visitedCtr
