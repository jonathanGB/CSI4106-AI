# CSI 4106 - Assignment 2

## by Oliver Fei (7624001) and Jonathan Guillotte-Blouin (7900293)

*NB*: `utils.py` and `logic.py` are taken from **aima-python**.

We assume pits **cannot** appear on the gold **and** wumpus tiles.

We don't start at [1,1], in reality at [0,0]; simpler to reason with, as python is a 0-based index. The map looks like this:

|      |       |       |      |
|:----:|:-----:|:-----:|:----:|
|(3,0) | (3,1) | (3,2) | (3,3)|
|(2,0) | (2,1) | (2,2) | (2,3)|
|(1,0) | (1,1) | (1,2) | (1,3)|
|(0,0) | (0,1) | (0,2) | (0,3)|
