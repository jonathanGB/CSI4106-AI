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
        minEstimate = 100
        agentX, agentY = self.state.getAgentPosition()
        for goalX, goalY in self.goals:
            xDelta = goalX - agentX # horizontal distance between agent and goal
            yDelta = goalY - agentY # vertical distance between agent and goal
            goalDirection = (self.getSign(xDelta),self.getSign(yDelta))
            agentDirection = Directions.DIRECTION_VECTORS[self.state.direction]
            rotationCount = 2
            if goalDirection == agentDirection:
                rotationCount = 0 # no rotations needed if agent is already facing the goal
            elif reduce(lambda x1, x2, y1, y2: abs(x1-y1 * x2-y2) == 1,agentDirection, goalDirection):
                # only 1 rotation is needed if the agent's direction is adjacent to the goal e.g. Right (1,0) and Up (0,1)
                rotationCount = 1 
            
            goalEstimate = abs(xDelta) + abs(yDelta) + rotationCount
            if goalEstimate < minEstimate:
                minEstimate = goalEstimate

        return minEstimate

    def getSign(self, num):
        return (num > 0) - (num < 0)


    ####################
    # Private methods
    ####################

    def _createNodeIfAllowed(self, action):
        newState = WumpusWorld(self.state)
        # payoffs except for gold are negative so we take the negation to get a positive cost
        cost = -1 * newState.executeAction(action)
        if newState.getAgentPosition() in self.allowed
            return RouteProblem(newState, self.goals, self.allowed, action, self.g + cost, self)
        return None
