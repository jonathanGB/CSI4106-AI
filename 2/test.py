from utils import *
from logic import *

(x, y, P, Q, f) = symbols('x, y, P, Q, f')

sentence = P & ~Q
Pxy = P(x, y)
kek = ~(P & Q)  |'==>'|  (~P | ~Q)
print(kek)


wumpus_kb = PropKB()

P11, P12, P21, P22, P31, B11, B21 = expr('P11, P12, P21, P22, P31, B11, B21')
wumpus_kb.tell(~P11)
wumpus_kb.tell(B11 | '<=>' | ((P12 | P21)))
wumpus_kb.tell(B21 | '<=>' | ((P11 | P22 | P31)))
wumpus_kb.tell(~B11)
wumpus_kb.tell(B21)
print(wumpus_kb.clauses)
print(pl_resolution(wumpus_kb, ~P11), pl_resolution(wumpus_kb, P11))