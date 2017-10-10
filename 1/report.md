# CSI4106 - Assignment 1
## by Oliver Fei and Jonathan Guillotte-Blouin

### 1.

### 2.

### 3. Heuristics
**a. Description of the two heuristics used by A***

**Heuristics 1** simply computes the number of misplaced numbers. Let's say we have:

| 2 | 3 | 0 |
|---|---|---|
| 1 | 4 | 5 |
| 6 | 7 | 8 |

"2", "3", "0", and "1" are misplaced; we get a cost of 4. However, we substract 1 to this in the end (unless we have a cost of 0, then we return 0); we'll discuss why in part b.


**Heuristics 2** computes the sum of the Manhattan distance of all numbers to their goal position. The Manhattan distance itself is the sum of the distance horizontally and of the distance vertically between two points. Let's say we have:

| 2 | 3 | 8 |
|---|---|---|
| 1 | 4 | 5 |
| 6 | 7 | 0 |

* "2" is at distance 2 (2 horizontally)
* "3" is at distance 2 (1 horizontally - 1 vertically)
* "8" is at distance 2 (2 vertically)
* "1" is at distance 2 (1 horizontally - 1 vertically)
* "0" is at distance 4 (2 horizontally - 2 vertically)

The cost would therefore be 2 + 2 + 2 + 2 + 4 = 12. However, we divide this result by 2 in the end; we'll discuss why in part b.

**b. Explanation of their admissibility**

Both heuristics are admissible, as their estimated costs are always smaller or equal to the real cost.

The real cost in our case is a cost of 1 per move (3 swaps = cost of 3, etc.)

**Heuristics 1**: With a real cost of *x*, we know that we must do exactly *x* moves to get to the goal state. With 1 move, 2 numbers have moved from their original position (0 and a neighbour); with a second move, another number can be displaced (we don't include 0 as it is already displaced), and so on. So, with *x* moves (read "real cost of *x*"), we can displace **at least** *x+1* numbers. Knowing that, if we compute that *y* numbers are misplaced | y > 0, we know we can move these *y* numbers in **at least** *y-1* moves, so has a minimum real cost of *y-1*. Therefore, **Heuristics 1** is admissible as it is certain to never overcome the minimum real cost at one state.

**Heuristics 2**:


**c. Does one heuristic dominate the other?**

No, as none of the heuristics always have a higher score than the other. Here's a proof:

| 1 | 5 | 6 |
|---|---|---|
| 3 | 4 | 2 |
| 7 | 0 | 8 |

Heuristics 1: 5 <br>
Heuristics 2: 6

| 1 | 4 | 2 |
|---|---|---|
| 0 | 8 | 5 |
| 3 | 7 | 6 |

Heuristics 1: 5 <br>
Heuristics 2: 4


In the first case, **heuristics 2** dominates **heuristics 1**; in the second case, **heuristics 1** dominates **heuristics 2**. Therefore, none of them are dominant.

### 4. Conclusion