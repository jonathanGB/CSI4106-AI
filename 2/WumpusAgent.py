from WumpusWorld import *

class WumpusAgent:
  def __init__(self):
    self.world = WumpusWorld()
    self.wumpus_kb = PropKB()
    self.payoff = 0
    self.position = [0,0]

    # expressions for the knowledge base
    self.sensations = [[] for _ in range(self.size)]
    self.pits = [[] for _ in range(self.size)]
    self.wumpuss = [[] for _ in range(self.size)]
    self.golds = [[] for _ in range(self.size)]
    
    # initialize expressions for sensations, pits, wumpuss, and golds at every index
    for i in range(self.size):
      for j in range(self.size):
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
    for i in range(self.size):
      for j in range(self.size):
        # breeze
        self.wumpus_kb.tell(sensations[i][j][Sensations.BREEZE] | '<=>' | self.getValidAdjacentRoomExpressions(i,j,self.pits))
        # stench
        self.wumpus_kb.tell(sensations[i][j][Sensations.STENCH] | '<=>' | self.getValidAdjacentRoomExpressions(i,j,self.wumpuss))
        # glitter
        self.wumpus_kb.tell(sensations[i][j][Sensations.GLITTER] | '<=>' | self.golds[i][j])

  # utility method for generating a conjoined expression for valid adjacent rooms to a given room
  def getValidAdjacentRoomExpressions(self, i, j, expressions):
    validExpressions = []
    if i - 1 >= 0:
      # add expression for left room
      validExpressions.append(str(expressionns[i-1][j]))
    if i + 1 < self._size:
      # add expression for right room
      validExpressions.append(str(expressions[i+1][j]))
    if j - 1 >= 0:
      # add expression for bottom room
      validExpressions.append(str(expressions[i][j-1]))
    if j + 1 < self._size:
      # add expression for top room
      validExpressions.append(str(expressions[i][j+1]))

    return expr('(' + ' | '.join(validExpressions) + ')')

  def tellSensations(self, percept):
    posX = self.position[0]
    posY = self.position[1]
    for perception, perceptionValue in enumerate(percept):
      prefix = '~'
      if perceptionValue:
        prefix = ''
      self.wumpus_kb.tell(expr(prefix + str(sensations[posX][posY][perception])))
  

  def exploreWorld(self):
    while not self.world.isAgentDead() and not self.world.isGoldPickedUp():
      # update knowledge base
      percept = self.world.getAgentSensations()
      self.tellSensations(percept)

# start script here
# agent = WumpusAgent()