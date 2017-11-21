from utils import *
from logic import *
from WumpusWorld import *
from RouteProblem import *
import timeit
import random

class ActionPriority:
  GRAB = 0
  SAFE = 1
  UNKNOWN = 2
  NOT_SAFE = 3

class WumpusAgent:
  def __init__(self):
    self.world = WumpusWorld()
    self.wumpus_kb = PropKB()
    self.payoff = 0
    self.moves = 0
    self.plan = []

    self.safeRooms = set() # set of tuples to store safe rooms we are able to reach
    self.wumpusRooms = set() # set of tuples to store rooms that may contain a wumpus
    self.unsafeRooms = set() # set of tuples to store rooms that may contain a pit
    self.visited = set() # set of rooms we have already visited (guaranteed to be safe)

    # expressions for the knowledge base
    self.sensations = [[] for _ in range(self.world.getSize())]
    self.pits = [[] for _ in range(self.world.getSize())]
    self.wumpuss = [[] for _ in range(self.world.getSize())]
    self.golds = [[] for _ in range(self.world.getSize())]
    
    self.symbols = []

    # initialize expressions for sensations, pits, wumpuss, and golds at every index
    for i in range(self.world.getSize()):
      for j in range(self.world.getSize()):
        self.sensations[i].append([
          expr('Br{}{}'.format(i,j)),
          expr('St{}{}'.format(i,j)),
          expr('Gl{}{}'.format(i,j)),
          expr('Bu{}{}'.format(i,j)),
          expr('Sc{}{}'.format(i,j))
        ])
        self.pits[i].append(expr('Pi{}{}'.format(i,j)))
        self.wumpuss[i].append(expr('Wu{}{}'.format(i,j)))
        self.golds[i].append(expr('Go{}{}'.format(i,j)))
        self.symbols.extend(self.sensations[i][j])
      self.symbols.extend(self.pits[i])
      self.symbols.extend(self.wumpuss[i])
      self.symbols.extend(self.golds[i])
    
    

    # populate the database with wumpus world rules
    for i in range(self.world.getSize()):
      for j in range(self.world.getSize()):
        # breeze
        self.wumpus_kb.tell(self.sensations[i][j][Sensations.BREEZE] | '<=>' | self.getValidAdjacentRoomExpressions(i,j,self.pits))
        # stench
        self.wumpus_kb.tell(self.sensations[i][j][Sensations.STENCH] | '<=>' | self.getValidAdjacentRoomExpressions(i,j,self.wumpuss))
        # glitter
        self.wumpus_kb.tell(self.sensations[i][j][Sensations.GLITTER] | '<=>' | self.golds[i][j])
        # scream means no stench
        self.wumpus_kb.tell(self.sensations[i][j][Sensations.SCREAM] | '==>' | ~self.sensations[i][j][Sensations.STENCH])
    self.wumpus_kb.tell('~Pi00')
    self.wumpus_kb.tell('~Go00')

  # utility method for generating a conjoined expression for valid adjacent rooms to a given room
  def getValidAdjacentRoomExpressions(self, i, j, expressions):
    validExpressions = []
    if i - 1 >= 0:
      # add expression for left room
      validExpressions.append(str(expressions[i-1][j]))
    if i + 1 < self.world.getSize():
      # add expression for right room
      validExpressions.append(str(expressions[i+1][j]))
    if j - 1 >= 0:
      # add expression for bottom room
      validExpressions.append(str(expressions[i][j-1]))
    if j + 1 < self.world.getSize():
      # add expression for top room
      validExpressions.append(str(expressions[i][j+1]))

    return expr('(' + ' | '.join(validExpressions) + ')')

  def tellSensations(self, percept):
    posX, posY = self.world.getAgentPosition()
    for perception, perceptionValue in enumerate(percept):
      prefix = '' if perceptionValue else '~' 
      self.wumpus_kb.tell(expr(prefix + str(self.sensations[posX][posY][perception])))  

  def intelligentExploreWorld(self):
    start = timeit.default_timer()
    

    while not self.world.isAgentDead():
      if len(self.plan) == 0:
        posX, posY = self.world.getAgentPosition()
        percept = self.world.getAgentSensations()
        self.tellSensations(percept)
        
        # check if we are on gold
        if percept[Sensations.GLITTER]:
          self.payoff += self.world.applyAction(Actions.GRAB_OBJECT)
          self.moves += 1
          break

        self.visited.add((posX, posY))
        self.removeLocationFromFringe((posX, posY))

        # add new reachable locations to the fringe
        for location in self.getValidAdjacentLocations(posX, posY):
          if location not in self.visited:
            self.unsafeRooms.add(location)

        # recheck safety of fringe locations we were not sure about
        tempUnsafe = self.unsafeRooms.copy()
        for locationX, locationY in tempUnsafe:
          # if the location contains a pit, remove it from consideration
          if self.checkIfTrue(self.pits[locationX][locationY]):
            self.unsafeRooms.discard((locationX, locationY))
          
          # check if there is no longer any chance that the location has a pit
          elif self.checkIfTrue(~self.pits[locationX][locationY]):
            self.unsafeRooms.discard((locationX, locationY))
            # check if the room might have a wumpus
            if self.checkIfTrue(~self.wumpuss[locationX][locationY]):
              self.safeRooms.add((locationX, locationY))
            else:
              self.wumpusRooms.add((locationX, locationY))

        tempWumpus = self.wumpusRooms.copy()
        for locationX, locationY in tempWumpus:
          # if the location contains a pit, remove it from consideration
          if self.checkIfTrue(self.pits[locationX][locationY]):
            self.wumpusRooms.discard((locationX, locationY))
          
          # check for pit
          elif self.checkIfTrue(~self.pits[locationX][locationY]):
            # check if the room is now safe
            if self.checkIfTrue(~self.wumpuss[locationX][locationY]):
              self.safeRooms.add((locationX, locationY))
          else:
            # chance of pit so we move this room to the set of unsafe rooms
            self.wumpusRooms.discard((locationX, locationY))
            self.unsafeRooms.add((locationX, locationY))

        # Try to get to an unvisited safe room if possible
        # If not, we try to get to unvisited room that may contain a wumpus
        # Last resort, we try to get to unvisited room that may contain a pit
        if len(self.safeRooms) > 0:
          print("Finding path to a safe room")
          self.plan = self.astar_search(RouteProblem(WumpusWorld(self.world), self.safeRooms, self.visited.union(self.safeRooms)))
        elif len(self.wumpusRooms) > 0:
          print("Finding path to a wumpus room")
          self.plan = self.astar_search(RouteProblem(WumpusWorld(self.world), self.wumpusRooms, self.visited.union(self.wumpusRooms)))
          # before moving into the tile that might have a wumpus, take a shot
          self.plan.insert(len(self.plan) - 2, Actions.FIRE_ARROW)
        elif len(self.unsafeRooms) > 0:
          print("Finding path to an unsafe room")
          self.plan = self.astar_search(RouteProblem(WumpusWorld(self.world), self.unsafeRooms, self.visited.union(self.unsafeRooms)))
        else:
          # We are surrounded by walls and/or pits. Puzzle is not solvable.
          break

      else:
        self.payoff += self.world.applyAction(self.plan.pop())
        self.moves += 1
        print("Action applied.")
        self.printInfo()
      


    self.printResults(timeit.default_timer() - start)

  def printInfo(self):
    print("Current location: " + str(self.world.getAgentPosition()))
    print("Safe rooms: " + str(self.safeRooms))
    print("Wumpus rooms: " + str(self.wumpusRooms))
    print("Unsafe rooms: " + str(self.unsafeRooms))
    print("Visited rooms: " + str(self.visited))

  def removeLocationFromFringe(self, location):
    if location in self.safeRooms:
      self.safeRooms.remove(location)
    elif location in self.wumpusRooms:
      self.wumpusRooms.remove(location)
    elif location in self.unsafeRooms:
      self.unsafeRooms.remove(location)

  def getValidAdjacentLocations(self, i, j):
    validLocations = []
    if i - 1 >= 0:
      # add left location
      validLocations.append((i-1,j))
    if i + 1 < self.world.getSize():
      # add right location
      validLocations.append((i+1,j))
    if j - 1 >= 0:
      # add bottom location
      validLocations.append((i,j-1))
    if j + 1 < self.world.getSize():
      # add top location
      validLocations.append((i,j+1))

    return validLocations

  def dumbExploreWorld(self):
    start = timeit.default_timer()
    lastAction = None
    percept = None

    while not self.world.isAgentDead():
      posX, posY = self.world.getAgentPosition()

      # these last actions might have changed the sensations of the agent
      if lastAction == None or lastAction == Actions.FIRE_ARROW or lastAction == Actions.MOVE_FORWARD:
        # update knowledge base
        percept = self.world.getAgentSensations()
        self.tellSensations(percept)

      if lastAction == Actions.MOVE_FORWARD:
        # check if we are on gold
        if percept[Sensations.GLITTER]:
          self.payoff += self.world.applyAction(Actions.GRAB_OBJECT)
          self.moves += 1
          break      

      if lastAction != Actions.FIRE_ARROW and percept[Sensations.STENCH]:
        self.payoff += self.world.applyAction(Actions.FIRE_ARROW)
        self.moves += 1
        lastAction = Actions.FIRE_ARROW
        continue

      action = random.choice((Actions.TURN_LEFT, Actions.TURN_RIGHT, Actions.MOVE_FORWARD))
      self.payoff += self.world.applyAction(action)
      self.moves += 1
      lastAction = action

    self.printResults(timeit.default_timer() - start)

  def printResults(self, delta):
    if self.world.isAgentDead():
      print("Agent died! :(")
    if self.world.isGoldPickedUp():
      print("Gold found! :)")

    print("Took {} moves ({}s)\nPayoff: {}".format(self.moves, delta, self.payoff))

  # use dpll to check if an expression is true
  def checkIfTrue(self, expression):
    self.wumpus_kb.tell(~expression)
    result = dpll(self.wumpus_kb.clauses, self.symbols, {})
    self.wumpus_kb.retract(~expression)
    return not result

  def astar_search(self, routeProblem):
    print('A* ------------------------------------')
    open_nodes = PriorityQueue(min, self.priority_function)
    visited = set() # used to keep track of visited nodes
    open_nodes.append(routeProblem)

    while not len(open_nodes) == 0:
        current = open_nodes.pop()
        currentHash = current.state.toString() # to be stored in the set of visted nodes

        if current.isGoal():
            return current.extractSolution()

        if currentHash in visited:
            continue

        visited.add(currentHash)

        for neighbor in current.expand():
            open_nodes.append(neighbor)

    return []
  
  def priority_function(self, routeProblem):
    return routeProblem.f

# start script here
agent = WumpusAgent()
agent.intelligentExploreWorld()