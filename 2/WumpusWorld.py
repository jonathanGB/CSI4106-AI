from utils import *
from logic import *
import random
from enum import Enum

class Directions:
  UP = 0
  RIGHT = 1
  DOWN = 2
  LEFT = 3

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

class WumpusWorld:

  def __init__(self):
    self._size = 4
    self._rooms = [[Room() for _ in range(self._size)] for _ in range(self._size)]
    
    # used for applying movement to the agent
    self._moveVectors = {
        Directions.UP: [0,1],
        Directions.LEFT: [-1,0],
        Directions.DOWN: [0,-1],
        Directions.RIGHT: [1,0]
      }

    self._wumpusPosition = None
    self._agentDead = False
    self._goldPickedUp = False
    self._agentPosition = [0, 0] # position of the agent
    self.direction = Directions.RIGHT # defaults directions is up
    self._agentSensations = [False, False, False, False, False] # sensations available to the agent 

    self.createWumpusWorld()

  def createWumpusWorld(self):
    # init
    freePositions = [ij for ij in range(1, 16)] # stores i x j of all free locations (0 is discarded from the start)

    # pick wumpus location (can't be initial position)
    wumpus = random.choice(freePositions)
    wumpusI, wumpusJ = self.getIandJ(wumpus)
    self._wumpusPosition = [wumpusI, wumpusJ]
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
    self._agentSensations = self._rooms[self._agentPosition[0]][self._agentPosition[1]].sensations

  def getPossibleActions(self, position):
    # assuming no actions possible if the agent is in the same room as a pit or a wumpus
    if self._rooms[position[0]][position[1]].hasPit or self._rooms[position[0]][position[1]].hasWumpus:
      return []
    return [Actions.MOVE_FORWARD, Actions.TURN_LEFT, Actions.TURN_RIGHT, Actions.GRAB_OBJECT, Actions.FIRE_ARROW]

  def applyAction(self, action):
    payoff = -1
    if action == Actions.MOVE_FORWARD:
      moveLocation = tuple(map(lambda x, y: x + y, self._moveVectors[self.direction], self._agentPosition))
      if -1 in moveLocation or self._size in moveLocation:
        self._agentSensations[Sensations.BUMP] = True
      else:
        self._agentPosition = moveLocation
        self._updateAgentSensations
        if currentRoom.hasPit or currentRoom.hasWumpus:
          payoff = -1000
          self._agentDead = True

    elif action == Actions.TURN_LEFT:
      self.direction = (self.direction - 1) % 4

    elif action == Actions.TURN_RIGHT:
      self.direction = (self.direction + 1) % 4
      
    elif action == Actions.GRAB_OBJECT:
      if self._rooms[self._agentPosition[0]][self._agentPosition[1]].hasGold:
        self._rooms[self._agentPosition[0]][self._agentPosition[1]].hasGold = False
        self._rooms[self._agentPosition[0]][self._agentPosition[1]].sensations[Sensations.GLITTER] = False
        self._agentSensations[Sensations.GLITTER] = False
        payoff = 1000
        self._goldPickedUp = True

    elif action == Actions.FIRE_ARROW:
      wumpusDirection = tuple(map(lambda x, y: x - y, self._wumpusPosition, self._agentPosition))
      arrowDirection = self._moveVectors[self.direction]

      # check if the arrow will hit the wumpus
      if (arrowDirection[0] == 0 and wumpusDirection[0] == 0 and wumpusDirection[1]/arrowDirection[1] > 0) or (arrowDirection[1] == 0 and wumpusDirection[1] == 0 and wumpusDirection[0]/arrowDirection[0] > 0):
        self.updateSensation(Sensations.STENCH, False, self._wumpusPosition[0], self._wumpusPosition[1])
        self._updateAgentSensations()
        self._agentSensations[Sensations.SCREAM] = True
        
      payoff = -10

    return payoff

world = WumpusWorld()
