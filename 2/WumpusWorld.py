import random
from enum import Enum
from math import sqrt
from copy import copy, deepcopy

class Directions:
  UP = 0
  RIGHT = 1
  DOWN = 2
  LEFT = 3
  DIRECTION_VECTORS = {
    0: (0,1), #Up
    1: (1,0), #Right
    2: (0,-1),#Down
    3: (-1,0) #Left
  }

class Actions(Enum):
  MOVE_FORWARD = 0
  TURN_LEFT = 1
  TURN_RIGHT = 2
  GRAB_OBJECT = 3
  FIRE_ARROW = 4

# used for sensations array indices
class Sensations:
  BREEZE = 0
  STENCH = 1
  GLITTER = 2
  BUMP = 3
  SCREAM = 4

class Room:
  def __init__(self):
    self.hasPit = False
    self.hasGold = False
    self.hasWumpus = False
    self.sensations = [False, False, False, False, False]

  def __str__(self):
    return '''
             hasPit:    {}
             hasGold:   {}
             hasWumpus: {}
             sensations: {{
               BREEZE:  {}
               STENCH:  {}
               GLITTER: {}
               BUMP:    {}
               SCREAM:  {}
             }}
           '''.format(self.hasPit, self.hasGold, self.hasWumpus, self.sensations[0], self.sensations[1], self.sensations[2], self.sensations[3], self.sensations[4])

class WumpusWorld:

  def __init__(self, other=None):
    self._size = 4
    self._rooms = copy(other._rooms) if isinstance(other, WumpusWorld) else [[Room() for _ in range(self._size)] for _ in range(self._size)]

    self._wumpusPosition = other._wumpusPosition if isinstance(other, WumpusWorld) else None
    self._agentDead = other._agentDead if isinstance(other, WumpusWorld) else False
    self._goldPickedUp = other._goldPickedUp if isinstance(other, WumpusWorld) else False
    self._agentPosition = other._agentPosition if isinstance(other, WumpusWorld) else (0,0) # position of the agent
    self.direction = other.direction if isinstance(other, WumpusWorld) else Directions.RIGHT # defaults directions is right
    self._agentSensations = copy(other._agentSensations) if isinstance(other, WumpusWorld) else [False, False, False, False, False] # sensations available to

    ''' in case other is a map to create a specific world
        other = {
          "wumpusPosition": (x,y),
          "goldPosition": (x,y),
          "pitPositions": [(x1,y1),(x2,y2),...]
        }
    '''
    if other and not isinstance(other, WumpusWorld):
      wumpusX, wumpusY = other['wumpusPosition']
      self._wumpusPosition = (wumpusX, wumpusY)
      self._rooms[wumpusX][wumpusY].hasWumpus = True
      self.updateSensation(Sensations.STENCH, True, wumpusX, wumpusY)

      goldX, goldY = other['goldPosition']
      self._rooms[goldX][goldY].hasGold = True
      self._rooms[goldX][goldY].sensations[Sensations.GLITTER] = True

      for pit in other['pitPositions']:
        pitX, pitY = pit
        self._rooms[pitX][pitY].hasPit = True
        self.updateSensation(Sensations.BREEZE, True, pitX, pitY)
    elif not other:
      self.createWumpusWorld()

  def getRoom(self, i, j):
    return self._rooms[i][j]

  def createWumpusWorld(self):
    # init
    freePositions = [ij for ij in range(1, 16)] # stores i x j of all free locations (0 is discarded from the start)

    # pick wumpus location (can't be initial position)
    wumpus = random.choice(freePositions)
    wumpusI, wumpusJ = self.getIandJ(wumpus)
    self._wumpusPosition = (wumpusI, wumpusJ)
    self._rooms[wumpusI][wumpusJ].hasWumpus = True
    self.updateSensation(Sensations.STENCH, True, wumpusI, wumpusJ)
    freePositions.remove(wumpus) # wumpus location is not free anymore

    # pick gold location (can't be initial position nor wumpus)
    gold = random.choice(freePositions)
    goldI, goldJ = self.getIandJ(gold)
    self._rooms[goldI][goldJ].hasGold = True
    self._rooms[goldI][goldJ].sensations[Sensations.GLITTER] = True
    freePositions.remove(gold) # gold location is not free anymore

    # pick pits for rest of free positions (can't be initial position, nor wumpus, nor gold)
    for ij in freePositions:
      # we initialize a pit with only 20% probability
      if random.random() > 0.2:
        continue

      pitI, pitJ = self.getIandJ(ij)
      self._rooms[pitI][pitJ].hasPit = True
      self.updateSensation(Sensations.BREEZE, True, pitI, pitJ)

    self._updateAgentSensations()

  def getAgentPosition(self):
    return self._agentPosition

  def isGoldPickedUp(self):
    return self._goldPickedUp

  def isAgentDead(self):
    return self._agentDead

  # given a product ixj, returns a tuple containing i and j
  def getIandJ(self, ij):
    return (ij // self._size, ij % self._size)

  def getAgentSensations(self):
    return self._agentSensations

  def getSize(self):
    return self._size

  # updates sensations surrounding tile (i,j)
  def updateSensation(self, sensation, isSensed, i, j):
    if i - 1 >= 0:
      self._rooms[i-1][j].sensations[sensation] = isSensed
    if i + 1 < self._size:
      self._rooms[i+1][j].sensations[sensation] = isSensed
    if j - 1 >= 0:
      self._rooms[i][j-1].sensations[sensation] = isSensed
    if j + 1 < self._size:
      self._rooms[i][j+1].sensations[sensation] = isSensed

  # set the agent sensations to the sensations available in the room it is in
  def _updateAgentSensations(self):
    agentX, agentY = self._agentPosition
    self._agentSensations = self._rooms[agentX][agentY].sensations

  def getPossibleActions(self):
    # assuming no actions possible if the agent is in the same room as a pit or a wumpus
    positionX, positionY = self._agentPosition
    if self._rooms[positionX][positionY].hasPit or self._rooms[positionX][positionY].hasWumpus:
      return []
    return [Actions.MOVE_FORWARD, Actions.TURN_LEFT, Actions.TURN_RIGHT, Actions.GRAB_OBJECT, Actions.FIRE_ARROW]

  # returns payoff of action
  def applyAction(self, action):
    if action == Actions.MOVE_FORWARD:
      moveLocation = tuple(map(lambda x, y: x + y, Directions.DIRECTION_VECTORS[self.direction], self._agentPosition))
      
      # if we move out of bounds in x or y
      if -1 in moveLocation or self._size in moveLocation:
        self._agentSensations[Sensations.BUMP] = True
        return -1
      
      # we're inbounds
      self._agentPosition = moveLocation
      self._updateAgentSensations()
      moveLocationX, moveLocationY = moveLocation
      currentRoom = self._rooms[moveLocationX][moveLocationY]
      if currentRoom.hasPit or currentRoom.hasWumpus:
        self._agentDead = True

      return -1

    if action == Actions.TURN_LEFT:
      self.direction = (self.direction - 1) % 4
      return -1

    if action == Actions.TURN_RIGHT:
      self.direction = (self.direction + 1) % 4
      return -1
      
    if action == Actions.GRAB_OBJECT:
      agentX, agentY = self._agentPosition
      currentRoom = self._rooms[agentX][agentY]

      if not currentRoom.hasGold:
        return -1

      # we found the gold
      currentRoom.hasGold = False
      currentRoom.sensations[Sensations.GLITTER] = False
      self._goldPickedUp = True
      return 1000

    if action == Actions.FIRE_ARROW:
      if WumpusWorld.isWumpusDead:
        return -10

      # get vector from agent to wumpus
      wumpusDirectionX, wumpusDirectionY = tuple(map(lambda x, y: x - y, self._wumpusPosition, self._agentPosition))
      # vector norm (length)
      wumpusDirectionNorm = sqrt(wumpusDirectionX ** 2 + wumpusDirectionY ** 2)
      # get unit vector from agent to wumpus
      wumpusDirectionUnit = tuple(map(lambda x: x / wumpusDirectionNorm, (wumpusDirectionX, wumpusDirectionY)))
      # get unit vector of arrow direction
      arrowDirectionUnit = Directions.DIRECTION_VECTORS[self.direction]

      # check if both vectors are equal (arrow hits wumpus)
      if wumpusDirectionUnit == arrowDirectionUnit:
        wumpusX, wumpusY = self._wumpusPosition
        self._rooms[wumpusX][wumpusY].hasWumpus = False
        WumpusWorld.isWumpusDead = True
        self.updateSensation(Sensations.STENCH, False, wumpusX, wumpusY)


        # scream in all rooms
        for i in range(self._size):
          for j in range(self._size):
            self._rooms[i][j].sensations[Sensations.SCREAM] = True

      return -10

  # returns a unique string based on current state of the world
  def toString(self):
    # for pathfinding, we only need to know the agent's position and direction
    return str(self._agentPosition) + str(self.direction)

WumpusWorld.isWumpusDead = False
