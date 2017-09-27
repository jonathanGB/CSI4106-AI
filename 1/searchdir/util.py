## Author: Amal Zouaq
### azouaq@uottawa.ca
### Author: Hadi Abdi Ghavidel
###habdi.cnlp@gmail.com

from operator import attrgetter
from collections import deque

#Queue - Implementation of the data structure Queue
class Queue:
    # initializes the current data structure
    def __init__(self):
        self.elems = deque()

    # returns the elements of the current data structure
    def show(self):
        return self.elems

    # returns a boolean indicating whether the current data structure is empty or not
    def isEmpty(self):
        return not self.elems

    # add the element item to the current data structure
    def enqueue(self, item):
        self.elems.append(item)

    # removes an element from the current data structure
    def dequeue(self):
        return self.elems.popleft()

    # returns the size of the current data structure (the number of elements)
    def size(self):
        return len(self.elems)

    # returns a boolean value that indicates if the element item is contained in the current data structure
    def __contains__(self, item):
        return item in self.elems


#Priority Queue Implementation of the data structure PriorityQueue
class PriorityQueue:
    # initializes the data structure
    def __init__(self, fct):
    # TO COMPLETE

    # returns the elements of the current data structure
    def show(self):
    # TO COMPLETE

    # returns a boolean indicating whether the current data structure is empty or not
    def isEmpty(self):
    # TO COMPLETE

    # add the element item to the current data structure
    def enqueue(self, item):
    # TO COMPLETE

    # removes an element from the current data structure
    def dequeue(self):
    # TO COMPLETE

    # returns the size of the current data structure (the number of elements)
    def size(self):
    # TO COMPLETE

    # returns a boolean value that indicates if the element item is contained in the current data structure
    def __contains__(self, item):
    # TO COMPLETE

#Stack - Implementation of the data structure Stack
class Stack:
    # initializes the data structure
    def __init__(self):
        self.__list = []
        self.__length = 0

    # returns the elements of the current data structure
    def show(self):
        return self.__list

    # returns a boolean indicating whether the current data structure is empty or not
    def isEmpty(self):
        return self.__length == 0

    # add the element item to the current data structure
    def push(self, item):
        self.__list.append(item)
        self.__length += 1

    # removes an element from the current data structure
    def pop(self):
        if self.isEmpty():
            return None

        self.__length -= 1
        return self.__list.pop()

    # returns the size of the current data structure (the number of elements)
    def size(self):
        return self.__length

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
