from searchdir.node import *
from searchdir.util import *

## This method must implement depdth-first search (DFS)
## It must return the solution node and the number of visited nodes
def depthfirst_search(initialState):
    print('DFS ----------------------------------')
    root = Node(initialState)

    return depthfirst_search_rec(root)

def depthfirst_search_rec(node, visitedCtr=0):
    visitedCtr += 1

    if node.state.isGoal():
        return node, visitedCtr

    if node.isRepeated():
        return None, visitedCtr

    frontier = Stack()
    for expanded in node.expand():
        frontier.push(expanded)

    while not frontier.isEmpty():
        expanded = frontier.pop()
        solution, subCtr = depthfirst_search_rec(expanded, visitedCtr)
        visitedCtr += subCtr

        if solution:
            return expanded, visitedCtr

    return None, visitedCtr
