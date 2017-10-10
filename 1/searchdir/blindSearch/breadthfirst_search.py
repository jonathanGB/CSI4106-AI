from searchdir.node import *
from searchdir.util import *

## This method must implement Breadth-first search (BFS)
## It must return the solution node and the number of visited nodes
def breadthfirst_search(initialState):
    print('BFS------------------------------')
    root = Node(initialState)
    visited = set() # keep track of visited nodes
    toVisit = Queue()
    toVisit.enqueue(root)

    while not toVisit.isEmpty():
        node = toVisit.dequeue()
        nodeHash = node.state.toString() # stored in the set of visited nodes

        if node.state.isGoal():
            return node, len(visited)

        if nodeHash in visited:
            continue

        visited.add(nodeHash)

        for expanded in node.expand():
            toVisit.enqueue(expanded)

    return None, len(visited)