from searchdir.node import *
from searchdir.util import *

## This method must implement depdth-first search (DFS)
## It must return the solution node and the number of visited nodes
def depthfirst_search(initialState):
    print('DFS ----------------------------------')
    root = Node(initialState)
    visited = set()
    toVisit = Stack()
    toVisit.push(root)

    while not toVisit.isEmpty():
        node = toVisit.pop()
        nodeHash = node.state.toString()

        if node.state.isGoal():
            return node, len(visited)
        
        if nodeHash in visited:
            continue

        visited.add(nodeHash)

        for expanded in node.expand():
            toVisit.push(expanded)

    return None, len(visited)
