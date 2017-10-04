from searchdir.node import *
from searchdir.util import *

## This method must implement Breadth-first search (BFS)
## It must return the solution node and the number of visited nodes
def breadthfirst_search(initialState):
    print('BFS------------------------------')
    root = Node(initialState)
    visited = {}
    toVisit = Queue()
    toVisit.enqueue(root)

    while not toVisit.isEmpty():
        node = toVisit.dequeue()

        if node.state.isGoal():
            return node, len(visited)

        visited[node.state.toString()] = True

        for expanded in node.expand():
            if expanded.state.toString() in visited:
                continue
            toVisit.enqueue(expanded)

    return None, visitedCtr