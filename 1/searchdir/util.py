## Author: Amal Zouaq
### azouaq@uottawa.ca
### Author: Hadi Abdi Ghavidel
###habdi.cnlp@gmail.com

from operator import attrgetter

#Queue - Implementation of the data structure Queue
class Queue:
    # initializes the current data structure
    def __init__(self):
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
    # TO COMPLETE

    # returns the elements of the current data structure
    def show(self):
    # TO COMPLETE

    # returns a boolean indicating whether the current data structure is empty or not
    def isEmpty(self):
    # TO COMPLETE

    # add the element item to the current data structure
    def push(self, item):
    # TO COMPLETE

    # removes an element from the current data structure
    def pop(self):
    # TO COMPLETE

    # returns the size of the current data structure (the number of elements)
    def size(self):
    # TO COMPLETE

    # returns a boolean value that indicates if the element item is contained in the current data structure
    def __contains__(self, item):
    # TO COMPLETE


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
