## Author: Amal Zouaq
### azouaq@uottawa.ca
### Author: Hadi Abdi Ghavidel
###habdi.cnlp@gmail.com

from operator import attrgetter
from collections import deque
import heapq

#Queue - Implementation of the data structure Queue
class Queue:
    # initializes the current data structure
    def __init__(self):
        self.__elems = deque()

    # returns the elements of the current data structure
    def show(self):
        return self.__elems

    # returns a boolean indicating whether the current data structure is empty or not
    def isEmpty(self):
        return not self.__elems

    # add the element item to the current data structure
    def enqueue(self, item):
        self.__elems.append(item)

    # removes an element from the current data structure
    def dequeue(self):
        if self.isEmpty():
            return None

        return self.__elems.popleft()

    # returns the size of the current data structure (the number of elements)
    def size(self):
        return len(self.__elems)

    # returns a boolean value that indicates if the element item is contained in the current data structure
    def __contains__(self, item):
        return item in self.__elems


#Priority Queue Implementation of the data structure PriorityQueue
class PriorityQueue:
    # initializes the data structure
    def __init__(self, fct):
        self.__heap = []
        self.__priority = fct

    # returns the elements of the current data structure
    def show(self):
        return self.__heap

    # returns a boolean indicating whether the current data structure is empty or not
    def isEmpty(self):
        return not self.__heap

    # add the element item to the current data structure
    def enqueue(self, item):
        heapq.heappush(self.__heap, (self.__priority(item), item))

    # removes an element from the current data structure
    def dequeue(self):
        if self.isEmpty():
            return None
        return heapq.heappop(self.__heap)

    # returns the size of the current data structure (the number of elements)
    def size(self):
        return len(self.__heap)

    # returns a boolean value that indicates if the element item is contained in the current data structure
    def __contains__(self, item):
        return item in self.__heap

#Stack - Implementation of the data structure Stack
class Stack:
    # initializes the data structure
    def __init__(self):
        self.__list = []

    # returns the elements of the current data structure
    def show(self):
        return self.__list

    # returns a boolean indicating whether the current data structure is empty or not
    def isEmpty(self):
        return not self.__list

    # add the element item to the current data structure
    def push(self, item):
        self.__list.append(item)

    # removes an element from the current data structure
    def pop(self):
        if self.isEmpty():
            return None

        return self.__list.pop()

    # returns the size of the current data structure (the number of elements)
    def size(self):
        return len(self.__list)

    # returns a boolean value that indicates if the element item is contained in the current data structure
    def __contains__(self, item):
       return item in self.__list


#Prints results for search alorithms
def printResults(alg, solution, start, stop, nbvisited):
    try:
        result, depth = solution.extractSolutionAndDepth()
        if result != []:
            print("The Solution is  ", (result))
            print("The Solution is at depth ", depth)
            print("The path cost is ", solution.getcost())
            print('Number of visited nodes:', nbvisited)
            time = stop - start
            print("The execution time is ", time, "seconds.")
            print("Done!")
    except AttributeError:
        print("No solution")
    except MemoryError:
        print("Memory Error!")
