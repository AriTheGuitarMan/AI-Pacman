# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from math import exp, expm1, factorial

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    beginner = problem.getStartState()
    num = 0
    counter = 0
    c = 0
    decisions = []
    present_mode = [beginner, decisions[:]]
    discovered = list()
    perimeter = util.Stack()
    limit = 89898
    conundrum = []
    decisions = util.Stack()
    for x in range(0,limit):
        present_position = present_mode[0]
        followers = problem.getSuccessors(present_position)
        length_children = len(followers)
        #for i in range(0,length_children):
        #val = followers.index(0)
        yonder = present_mode[1]
        if(decisions.isEmpty() or (not perimeter.isEmpty() and counter == 0)):
            [perimeter.push((element[num], yonder+[element[num+1]] ) ) for element in followers if x < limit/2]

        #[i][0]
        permEmp = False
        #powerz = lambda pol: exp( factorial(pol**2) )
        while ( counter <= c and (perimeter.isEmpty()) == permEmp ):
            permEmp = perimeter.isEmpty()
            #if the stack is empty
            #else:
            element = perimeter.pop()
            length_discovered = len(discovered)
            isInside = False
            for e in discovered:
                if (e == (element[num])):
                    isInside = True
            #for x in range(0,length_discovered):
                #if(discovered.index)
                #if(     element[num] == discovered.get(x)):
                #isInside = True
            if (isInside == True):
                continue
            else:
                c = -1
            #else:
            #    return None #the stack is empty, so return None
        #    return None #the stack is empty, so return None
        discovered.append(element[num])
        decisions.push(element)
        present_mode = element
        counter = counter + 1
        c = counter
        compare = present_mode[num]
        #>> a, b = a + b, a * b
        if(not decisions.isEmpty()):
            decisions.pop()
        if(problem.isGoalState(compare) == True):
            x = limit
            break
        else:
            continue
    if(counter > 0):
        return present_mode[num+1]
    else:
        return present_mode[counter+num+1]
    # util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    beginner = problem.getStartState()
    num = 0
    counter = 0
    c = 0
    decisions = []
    present_mode = [beginner, decisions[:]]
    discovered = list()
    discovered.append(beginner)
    perimeter = util.Queue()
    limit = 89898
    conundrum = []
    decisions = util.Queue()
    for x in range(0,limit):
        present_position = present_mode[0]
        followers = problem.getSuccessors(present_position)
        length_children = len(followers)
        #for i in range(0,length_children):
        #val = followers.index(0)
        yonder = present_mode[1]
        if(decisions.isEmpty() or (not perimeter.isEmpty() and counter == 0)):
            [perimeter.push((element[num], yonder+[element[num+1]] ) ) for element in followers if x < limit/2]

        #[i][0]
        permEmp = False
        #powerz = lambda pol: exp( factorial(pol**2) )
        while ( counter <= c and (perimeter.isEmpty()) == permEmp ):
            permEmp = perimeter.isEmpty()
            #if the stack is empty
            #else:
            element = perimeter.pop()
            length_discovered = len(discovered)
            isInside = False
            for e in discovered:
                if (e == (element[num])):
                    isInside = True
            #for x in range(0,length_discovered):
                #if(discovered.index)
                #if(     element[num] == discovered.get(x)):
                #isInside = True
            if (isInside == True):
                continue
            else:
                c = -1
            #else:
            #    return None #the stack is empty, so return None
        #    return None #the stack is empty, so return None
        discovered.append(element[num])
        decisions.push(element)
        present_mode = element
        counter = counter + 1
        c = counter
        compare = present_mode[num]
        #>> a, b = a + b, a * b
        if(not decisions.isEmpty()):
            decisions.pop()
        if(problem.isGoalState(compare) == True):
            x = limit
            break
        else:
            continue
    if(counter > 0):
        return present_mode[num+1]
    else:
        return present_mode[counter+num+1]
    return None
    # util.raiseNotDefined()



def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    beginner = problem.getStartState()
    num = 0
    counter = 0
    c = 0
    decisions = []
    present_mode = [beginner, decisions[:], num]
    discovered = list()
    discovered.append(beginner)
    perimeter = util.PriorityQueue()
    limit = 89898
    conundrum = []
    decisions = util.Queue()
    for x in range(0,limit):
        present_position = present_mode[0]
        followers = problem.getSuccessors(present_position)
        length_children = len(followers)
        #for i in range(0,length_children):
        #val = followers.index(0)
        yonder = present_mode[1]
        plata = present_mode[2]
        if(decisions.isEmpty() or (not perimeter.isEmpty() and counter == 0)):
            [perimeter.push(   (element[num], yonder+[element[num+1]], plata+element[num+2])   , plata+element[num+2] ) for element in followers if x < limit/2]

        #[i][0]
        permEmp = False
        #powerz = lambda pol: exp( factorial(pol**2) )
        while ( counter <= c and (perimeter.isEmpty()) == permEmp ):
            permEmp = perimeter.isEmpty()
            #if the stack is empty
            #else:
            element = perimeter.pop()
            length_discovered = len(discovered)
            isInside = False
            for e in discovered:
                if (e == (element[num])):
                    isInside = True
            #for x in range(0,length_discovered):
                #if(discovered.index)
                #if(     element[num] == discovered.get(x)):
                #isInside = True
            if (isInside == True):
                continue
            else:
                c = -1
            #else:
            #    return None #the stack is empty, so return None
        #    return None #the stack is empty, so return None
        discovered.append(element[num])
        decisions.push(element)
        tempTuple = tuple()
        tempTuple = (element[num], element[num+1], element[num+2])
        tempTuple[::1]
        present_mode = tempTuple
        counter = counter + 1
        c = counter
        compare = present_mode[num]
        #>> a, b = a + b, a * b
        if(not decisions.isEmpty()):
            decisions.pop()
        if(problem.isGoalState(compare) == True):
            x = limit
            break
        else:
            continue
    if(counter > 0):
        return present_mode[num+1]
    else:
        return present_mode[counter+num+1]
    return None
    # util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    beginner = problem.getStartState()
    num = 0
    counter = 0
    c = 0
    decisions = []
    present_mode = [beginner, decisions[:], num]
    discovered = list()
    discovered.append(beginner)
    perimeter = util.PriorityQueue()
    limit = 89898
    conundrum = []
    decisions = util.Queue()
    for x in range(0,limit):
        present_position = present_mode[0]
        followers = problem.getSuccessors(present_position)
        length_children = len(followers)
        #for i in range(0,length_children):
        #val = followers.index(0)
        yonder = present_mode[1]
        plata = present_mode[2]
        if(decisions.isEmpty() or (not perimeter.isEmpty() and counter == 0)):
            [perimeter.push(   (element[num], yonder+[element[num+1]], plata+element[num+2])   , plata+element[num+2]+heuristic(element[num],problem) ) for element in followers if x < limit/2]

        #[i][0]
        permEmp = False
        #powerz = lambda pol: exp( factorial(pol**2) )
        while ( counter <= c and (perimeter.isEmpty()) == permEmp ):
            permEmp = perimeter.isEmpty()
            #if the stack is empty
            #else:
            element = perimeter.pop()
            length_discovered = len(discovered)
            isInside = False
            for e in discovered:
                if (e == (element[num])):
                    isInside = True
            #for x in range(0,length_discovered):
                #if(discovered.index)
                #if(     element[num] == discovered.get(x)):
                #isInside = True
            if (isInside == True):
                continue
            else:
                c = -1
            #else:
            #    return None #the stack is empty, so return None
        #    return None #the stack is empty, so return None
        discovered.append(element[num])
        decisions.push(element)
        tempTuple = tuple()
        tempTuple = (element[num], element[num+1], element[num+2])
        tempTuple[::1]
        present_mode = tempTuple
        counter = counter + 1
        c = counter
        compare = present_mode[num]
        #>> a, b = a + b, a * b
        if(not decisions.isEmpty()):
            decisions.pop()
        if(problem.isGoalState(compare) == True):
            x = limit
            break
        else:
            continue
    if(counter > 0):
        return present_mode[num+1]
    else:
        return present_mode[counter+num+1]
    return None
    # util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
