from utils import *
from logic import *
from WumpusWorld import *
from RouteProblem import *
import timeit
import random
import sys
import multiprocessing

class ActionPriority:
  GRAB = 0
  SAFE = 1
  UNKNOWN = 2
  NOT_SAFE = 3

class WumpusAgent:
  def __init__(self, world=None, verbose=False):
    self.world = WumpusWorld(world)
    self.wumpus_kb = PropKB()
    self.payoff = 0
    self.moves = 0
    self.plan = []
    self.verbose = verbose
    self.killedWumpus = False

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
      prefix2 = '~' if perceptionValue else ''
      self.wumpus_kb.retract(expr(prefix2 + str(self.sensations[posX][posY][perception])))
      self.wumpus_kb.tell(expr(prefix + str(self.sensations[posX][posY][perception])))  

  def intelligentExploreWorld(self):
    start = timeit.default_timer()
    iteration = 0

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
        if self.verbose:
          print("Adding new reachable locations...")
        for location in self.getValidAdjacentLocations(posX, posY):
          if location not in self.visited:
            if self.verbose:
              print(str(location))
            if percept[Sensations.BREEZE]:
              self.unsafeRooms.add(location)
            elif percept[Sensations.STENCH]:
              self.wumpusRooms.add(location)
            else:
              self.safeRooms.add(location)

        # recheck safety of fringe locations we were not sure about
        tempUnsafe = self.unsafeRooms.copy()
        for locationX, locationY in tempUnsafe:
          # if the location contains a pit, remove it from consideration
          if self.checkIfTrue(self.pits[locationX][locationY]):
            self.unsafeRooms.discard((locationX, locationY))
            print(str(locationX) + "," + str(locationY) + " contains a pit. Eliminated location from consideration.")
          
          # check if there is no longer any chance that the location has a pit
          elif self.checkIfTrue(~self.pits[locationX][locationY]):
            self.unsafeRooms.discard((locationX, locationY))
            # check if the room might have a wumpus
            if not self.killedWumpus:
              if self.checkIfTrue(~self.wumpuss[locationX][locationY]):
                self.safeRooms.add((locationX, locationY))
              else:
                self.wumpusRooms.add((locationX, locationY))
            else:
              self.safeRooms.add((locationX, locationY))

        tempWumpus = self.wumpusRooms.copy()
        for locationX, locationY in tempWumpus:
          # if the location contains a pit, remove it from consideration
          if self.checkIfTrue(self.pits[locationX][locationY]):
            self.wumpusRooms.discard((locationX, locationY))
          
          # check for pit
          elif self.checkIfTrue(~self.pits[locationX][locationY]):
            # check if the room is now safe
            if self.killedWumpus or self.checkIfTrue(~self.wumpuss[locationX][locationY]):
              self.wumpusRooms.discard((locationX, locationY))
              self.safeRooms.add((locationX, locationY))
          else:
            # chance of pit so we move this room to the set of unsafe rooms
            self.wumpusRooms.discard((locationX, locationY))
            self.unsafeRooms.add((locationX, locationY))

        if self.verbose:
          self.printInfo()
        # Try to get to an unvisited safe room if possible
        # If not, we try to get to unvisited room that may contain a wumpus
        # Last resort, we try to get to unvisited room that may contain a pit
        if len(self.safeRooms) > 0:
          if self.verbose:
            print("Finding path to a safe room")
          routeProblem = RouteProblem(WumpusWorld(self.world), self.safeRooms, self.visited.union(self.safeRooms))
          self.plan = self.astar_search(routeProblem)
          if self.verbose:
            print(routeProblem.allowed)
        elif len(self.wumpusRooms) > 0:
          if self.verbose:
            print("Finding path to a wumpus room")

          self.plan = self.astar_search(RouteProblem(WumpusWorld(self.world), self.wumpusRooms, self.visited.union(self.wumpusRooms)))
        elif len(self.unsafeRooms) > 0:
          if self.verbose:
            print("Finding path to an unsafe room")
          self.plan = self.astar_search(RouteProblem(WumpusWorld(self.world), self.unsafeRooms, self.visited.union(self.unsafeRooms)))
        else:
          # We are surrounded by walls and/or pits. Puzzle is not solvable.
          break
        if self.verbose:
          print(str(self.plan))

      else:
        if not self.killedWumpus and len(self.plan) == 1:
          # The last action is always the movement forward into a goal tile
          # Before doing so, we should check if the tile might contain a wumpus and fire an arrow if there is a chance
          currentX, currentY = self.world.getAgentPosition()
          moveX, moveY = Directions.DIRECTION_VECTORS[self.world.direction]
          if not self.checkIfTrue(~self.wumpuss[currentX + moveX][currentY + moveY]):
            self.payoff += self.world.applyAction(Actions.FIRE_ARROW)
            self.moves += 1
            if self.world.getAgentSensations()[Sensations.SCREAM]:
              # remove old stench from the knowledge base so as not to cause contradictions
              for i in range(self.world.getSize()):
                for j in range(self.world.getSize()):
                  self.wumpus_kb.retract(self.sensations[i][j][Sensations.STENCH])
              self.killedWumpus = True

        action = self.plan.pop(0)
        if self.verbose:
          print(str(action))
        self.payoff += self.world.applyAction(action)
        self.moves += 1
        percept = self.world.getAgentSensations()
        self.tellSensations(percept)
    
      iteration += 1
      if self.verbose:
        self.printWorld(iteration)
      

    if self.verbose:
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
    
    if self.verbose:
      self.printResults(timeit.default_timer() - start)

  def printResults(self, delta):
    if self.world.isAgentDead():
      self.payoff -= 1000
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
    if self.verbose:
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

  def printWorld(self, iteration):
    print("Iteration {}:".format(iteration))
    dir = self.world.direction
    dirStr = '←' if dir == Directions.LEFT else '↑' if dir == Directions.UP else '→' if dir == Directions.RIGHT else '↓'
    for j in reversed(range(self.world.getSize())):
      for i in range(self.world.getSize()):
        if i == 0:
          print("\n --------------- \n|", end='')
          
        currentRoom = self.world.getRoom(i, j)
        val = 'G ' if currentRoom.hasGold else 'P ' if currentRoom.hasPit else 'W ' if currentRoom.hasWumpus else '  '
        val += dirStr if self.world.getAgentPosition() == (i,j) else ' '
        print(val + "|", end='')

    print("\n --------------- \n", end='')
    
    sensations = self.world.getAgentSensations()
    print("Breeze: {}, Stench: {}, Glitter: {}, Bump: {}, Scream: {}\n\n".format(sensations[0], sensations[1], sensations[2], sensations[3], sensations[4]))


results = [0, 0, 0, 0]
def simulation2500(id, verbose):
  for i in range(250):
    agent = WumpusAgent(None, verbose)
    while not agent.world.isValidWorld():
      agent = WumpusAgent(None, verbose)

    agent.intelligentExploreWorld()
    agent.payoff += -1000 if agent.world.isAgentDead() else 0
    results[id] += agent.payoff
    print("{} finished iteration {} with payoff {}".format(id, i, agent.payoff))
    print(results)


#if __name__ == "__main__":
  # start script here
  # verbose = True if len(sys.argv) > 1 and sys.argv[1] == "-v" else False

  # p1 = multiprocessing.Process(target=simulation2500, args=(0, verbose))
  # p2 = multiprocessing.Process(target=simulation2500, args=(1, verbose))
  # p3 = multiprocessing.Process(target=simulation2500, args=(2, verbose))
  # p4 = multiprocessing.Process(target=simulation2500, args=(3, verbose))
  # p1.start()
  # p2.start()
  # p3.start()
  # p4.start()
  # p1.join()
  # p2.join()
  # p3.join()
  # p4.join()

  # print(results)
  # averagePayoff = (results[0] + results[1] + results[2] + results[3]) / 1000
  # print("Average payoff is {}".format(averagePayoff))

agent = WumpusAgent(None, True)
agent.intelligentExploreWorld()

