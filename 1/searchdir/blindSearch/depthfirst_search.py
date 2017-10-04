from searchdir.node import *
from searchdir.util import *

## This method must implement depdth-first search (DFS)
## It must return the solution node and the number of visited nodes
def depthfirst_search(initialState):
    print('DFS ----------------------------------')
    root = Node(initialState)
    visited = {}
    toVisit = Stack()
    toVisit.push(root)

    while not toVisit.isEmpty():
        node = toVisit.pop()

        if node.state.isGoal():
            return node, len(visited)
        
        visited[node.state.toString()] = True

        for expanded in node.expand():
            if expanded.state.toString() in visited:
                continue
            toVisit.push(expanded)

    return None, visitedCtr
