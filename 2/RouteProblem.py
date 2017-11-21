from WumpusWorld import *
class RouteProblem:
  def __init__(self, state, goals, allowed, action=None, cost=0, previous=None):
        self.state = state  # state represented by the node
        self.previous = previous  # previous node in the solution path
        self.goals = goals
        self.allowed = allowed
        self.g = cost  # cost to reach this node from initial state
        self.h = self.heuristic()  # heuristic: estimate of remaining cost to reach a solution
        self.f = self.g + self.h  # total estimated cost
        self.action = action  # action that resulted in the state represented by the node

    ####################
    # Public methods
    ####################

    def isGoal(self):
        return self.state.getAgentPosition() in goals

    # Returns a list of all new nodes that represents next possible states in the exploration
    def expand(self):
        return map(lambda s: self._createNodeIfAllowed(s), self.state.possibleActions())

    # Extracts the sequence of states and actions that lead to current node
    def extractSolution(self):
        solution = []
        currentNode = self
        if currentNode is not None:
            while currentNode.previous:
                solution.append((currentNode.action))
                currentNode = currentNode.previous
            solution.reverse()
        return solution


        # Extracts the sequence of states and actions that lead to current node

    def extractSolutionAndDepth(self):
        solution = []
        depth = 0
        currentNode = self
        if currentNode is not None:
            while currentNode.previous:
                solution.append((currentNode.action))
                depth += 1
                currentNode = currentNode.previous
            solution.reverse()
        return solution, depth

    def getcost(self):
        return self.g

    def heuristic(self):
        # TODO calculate heuristic
        return -1


    ####################
    # Private methods
    ####################

    def _createNodeIfAllowed(self, action):
        newState = WumpusWorld(self.state)
        cost = newState.executeAction(action)
        if newState.getAgentPosition() in self.allowed
            return RouteProblem(newState, self.goals, self.allowed, action, self.g + cost, self)
        return None
