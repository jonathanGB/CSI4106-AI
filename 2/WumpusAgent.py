from utils import *
from logic import *
from WumpusWorld import *
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
    self.plan = PriorityQueue(min, lambda x: x.priority)

    # expressions for the knowledge base
    self.sensations = [[] for _ in range(self.world.getSize())]
    self.pits = [[] for _ in range(self.world.getSize())]
    self.wumpuss = [[] for _ in range(self.world.getSize())]
    self.golds = [[] for _ in range(self.world.getSize())]
    
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
    self.wumpus_kb.tell('~P00')
    self.wumpus_kb.tell('~G00')

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

# start script here
agent = WumpusAgent()
agent.dumbExploreWorld()