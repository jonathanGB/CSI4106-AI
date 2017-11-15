from WumpusWorld import *

class WumpusAgent:
  def __init__(self):
    self.world = WumpusWorld()
    self.wumpus_kb = PropKB()
    self.isDead = False
    self.pickedUpGold = False

    # expressions for the knowledge base
    self.sensations = [[] for _ in range(self.size)]
    self.pits = [[] for _ in range(self.size)]
    self.wumpuss = [[] for _ in range(self.size)]
    self.golds = [[] for _ in range(self.size)]
    
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
    
    # TODO populate knowledge base with WumpusWorld rules

  # define rest of behaviour (part 3)
  # you may add helpers in WumpusWorlds if needed


# start script here
# agent = WumpusAgent()