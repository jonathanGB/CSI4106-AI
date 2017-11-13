from utils import *
from logic import *
import random
from enum import Enum

class Directions(Enum):
  UP = 1
  RIGHT = 2
  DOWN = 3
  LEFT = 4

class WumpusWorld:
  def __init__(self):
    self.size = 4
    self.wumpus_kb = PropKB()
    self.sensations = [[] for _ in range(self.size)]
    self.pits = [[] for _ in range(self.size)]
    self.wumpuss = [[] for _ in range(self.size)]
    self.golds = [[] for _ in range(self.size)]
    self.position = [0, 0] # position of the agent
    self.direction = Directions.UP # defaults directions is up

    self.createWumpusWorld()

  def createWumpusWorld(self):
    # init
    freePositions = [ij for ij in range(1, 16)] # stores i x j of all free locations (0 is discarded from the start)

    # initialize expressions for sensations, pits, wumpuss, and golds at every index
    for i in range(self.size):
      for j in range(self.size):
        self.sensations[i].append({
          'breeze': expr('Br{}{}'.format(i,j)),
          'stench': expr('St{}{}'.format(i,j)),
          'glitter': expr('Gl{}{}'.format(i,j)) 
        })
        self.pits[i].append(expr('Pi{}{}'.format(i,j)))
        self.wumpuss[i].append(expr('Wu{}{}'.format(i,j)))
        self.golds[i].append(expr('Go{}{}'.format(i,j)))

    # pick wumpus location (can't be initial position)
    wumpus = random.choice(freePositions)
    wumpusI, wumpusJ = self.getIandJ(wumpus)
    self.wumpus_kb.tell(self.wumpuss[wumpusI][wumpusJ])
    self.updateSensation('stench', wumpusI, wumpusJ)
    freePositions.remove(wumpus) # wumpus location is not free anymore

    # pick gold location (can't be initial position nor wumpus)
    gold = random.choice(freePositions)
    goldI, goldJ = self.getIandJ(gold)
    self.wumpus_kb.tell(self.golds[goldI][goldJ])
    self.updateSensation('glitter', goldI, goldJ)
    freePositions.remove(gold) # gold location is not free anymore

    # pick pits for rest of free positions (can't be initial position, nor wumpus, nor gold)
    for ij in freePositions:
      # we initialize a pit with only 20% probability
      if random.random() > 0.2:
        continue

      pitI, pitJ = self.getIandJ(ij)
      self.wumpus_kb.tell(self.pits[pitI][pitJ])
      self.updateSensation('breeze', pitI, pitJ)


    #print(self.wumpus_kb.clauses)

  # given a product ixj, returns a tuple containing i and j
  def getIandJ(self, ij):
    return (ij // self.size, ij % self.size)

  # updates sensations surrounding tile (i,j)
  def updateSensation(self, sensation, i, j):
    if i - 1 >= 0:
      self.wumpus_kb.tell(self.sensations[i-1][j][sensation])
    if i + 1 < self.size:
      self.wumpus_kb.tell(self.sensations[i+1][j][sensation])
    if j - 1 >= 0:
      self.wumpus_kb.tell(self.sensations[i][j-1][sensation])
    if j + 1 < self.size:
      self.wumpus_kb.tell(self.sensations[i][j+1][sensation])

WumpusAgent = WumpusWorld()
