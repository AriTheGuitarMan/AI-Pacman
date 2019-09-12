# bustersAgents.py
# ----------------
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


import util
from game import Agent
from game import Directions
from keyboardAgents import KeyboardAgent
import inference
import busters
from math import exp, expm1, factorial, ceil, fabs
from util import manhattanDistance
import itertools
import random, util
import busters
import game
from util import *
import time, os
import traceback
import sys

class NullGraphics:
    "Placeholder for graphics"
    def initialize(self, state, isBlue = False):
        pass
    def update(self, state):
        pass
    def pause(self):
        pass
    def draw(self, state):
        pass
    def updateDistributions(self, dist):
        pass
    def finish(self):
        pass

class KeyboardInference(inference.InferenceModule):
    """
    Basic inference module for use with the keyboard.
    """
    def initializeUniformly(self, gameState):
        "Begin with a uniform distribution over ghost positions."
        self.beliefs = util.Counter()
        for p in self.legalPositions: self.beliefs[p] = 1.0
        self.beliefs.normalize()

    def observe(self, observation, gameState):
        noisyDistance = observation
        emissionModel = busters.getObservationDistribution(noisyDistance)
        pacmanPosition = gameState.getPacmanPosition()
        allPossible = util.Counter()
        for p in self.legalPositions:
            trueDistance = util.manhattanDistance(p, pacmanPosition)
            if emissionModel[trueDistance] > 0:
                allPossible[p] = 1.0
        allPossible.normalize()
        self.beliefs = allPossible

    def elapseTime(self, gameState):
        pass

    def getBeliefDistribution(self):
        return self.beliefs


class BustersAgent:
    "An agent that tracks and displays its beliefs about ghost positions."

    def __init__( self, index = 0, inference = "ExactInference", ghostAgents = None, observeEnable = True, elapseTimeEnable = True):
        inferenceType = util.lookup(inference, globals())
        self.inferenceModules = [inferenceType(a) for a in ghostAgents]
        self.observeEnable = observeEnable
        self.elapseTimeEnable = elapseTimeEnable

    def registerInitialState(self, gameState):
        "Initializes beliefs and inference modules"
        import __main__
        self.display = __main__._display
        for inference in self.inferenceModules:
            inference.initialize(gameState)
        self.ghostBeliefs = [inf.getBeliefDistribution() for inf in self.inferenceModules]
        self.firstMove = True

    def observationFunction(self, gameState):
        "Removes the ghost states from the gameState"
        agents = gameState.data.agentStates
        gameState.data.agentStates = [agents[0]] + [None for i in range(1, len(agents))]
        return gameState

    def getAction(self, gameState):
        "Updates beliefs, then chooses an action based on updated beliefs."
        for index, inf in enumerate(self.inferenceModules):
            if not self.firstMove and self.elapseTimeEnable:
                inf.elapseTime(gameState)
            self.firstMove = False
            if self.observeEnable:
                inf.observeState(gameState)
            self.ghostBeliefs[index] = inf.getBeliefDistribution()
        self.display.updateDistributions(self.ghostBeliefs)
        return self.chooseAction(gameState)

    def chooseAction(self, gameState):
        "By default, a BustersAgent just stops.  This should be overridden."
        return Directions.STOP

class BustersKeyboardAgent(BustersAgent, KeyboardAgent):
    "An agent controlled by the keyboard that displays beliefs about ghost positions."

    def __init__(self, index = 0, inference = "KeyboardInference", ghostAgents = None):
        KeyboardAgent.__init__(self, index)
        BustersAgent.__init__(self, index, inference, ghostAgents)

    def getAction(self, gameState):
        return BustersAgent.getAction(self, gameState)

    def chooseAction(self, gameState):
        return KeyboardAgent.getAction(self, gameState)

from distanceCalculator import Distancer
from game import Actions
from game import Directions

class GreedyBustersAgent(BustersAgent):
    "An agent that charges the closest ghost."

    def registerInitialState(yo, estadoDelJuego):
        "Pre-computes the distance between every two points."
        BustersAgent.registerInitialState(yo, estadoDelJuego)
        yo.distancer = Distancer(estadoDelJuego.data.layout, False)

    def chooseAction(yo, estadoDelJuego):
        p2 = (1/13) * (-1)
        """
        First computes the most likely position of each ghost that has
        not yet been captured, then chooses an action that brings
        Pacman closer to the closest ghost (according to mazeDistance!).

        To find the mazeDistance between any two positions, use:
          self.distancer.getDistance(pos1, pos2)

        To find the successor position of a position after an action:
          successorPosition = Actions.getSuccessor(position, action)

        livingGhostPositionDistributions, defined below, is a list of
        util.Counter objects equal to the position belief
        distributions for each of the ghosts that are still alive.  It
        is defined based on (these are implementation details about
        which you need not be concerned):

          1) gameState.getLivingGhosts(), a list of booleans, one for each
             agent, indicating whether or not the agent is alive.  Note
             that pacman is always agent 0, so the ghosts are agents 1,
             onwards (just as before).

          2) self.ghostBeliefs, the list of belief distributions for each
             of the ghosts (including ghosts that are not alive).  The
             indices into this list should be 1 less than indices into the
             gameState.getLivingGhosts() list.
        """
        empieze = 0
        g = 2
        #idealCansaVerde = busters.getObservationDistribution(distMuyRuidoso)
        estacionDelJugador = estadoDelJuego.getPacmanPosition()
        visitanteRoc = util.Queue()
        counter = 0
        val = "Function De ChooseAction"
        locaNevnt = 0
        cuanto_lejos_malo = 10**2 * 10 * -1 #divided for understanding
        display = util.Queue()
        num = 0
        #util.raiseNotDefined()
        legal = [a for a in estadoDelJuego.getLegalPacmanActions()]
        livingGhosts = estadoDelJuego.getLivingGhosts()
        livingGhostPositionDistributions = \
            [beliefs for i, beliefs in enumerate(yo.ghostBeliefs)
             if livingGhosts[i+1]]
        livingGhostLen = len(livingGhostPositionDistributions)
        "*** YOUR CODE HERE ***"
        #Ariel

        #First computes the most likely position of each ghost that has
        #not yet been captured, then chooses an action that brings
        #Pacman closer to the closest ghost (according to mazeDistance!).

        decisions = []
        cercanoGrande = []
        legalMenteLen = len(legal)
        valor_won = 1.0
        tempLen = 0
        elPuntoTarget = None
        tempTempLen = valor_won

        while(tempLen < livingGhostLen):
            tempTempLen += tempLen
            s = livingGhostPositionDistributions[tempLen]
            aMe = s.argMax()
            display.push(aMe)
            cercanoGrande.append(aMe)
            if(len(cercanoGrande) < int(valor_won) - g):
                return None
            tempLen += 1

        visitanteRoc.push(legalMenteLen)
        powerz = lambda pol: ceil( factorial(pol**2) )
        ellocation = powerz(10)
        tempLen = 0
        laPossibleTarget = 0

        c = 0
        while(powerz(1) > cuanto_lejos_malo or tempTempLen >= legalMenteLen):
            while(locaNevnt < (len(cercanoGrande))):
                #locaNevnt = compararDeInteralo[tempTempLen]
                dictVal = cercanoGrande[locaNevnt]
                #cercanoGrande.pop()
                #print dictVal
                multiplyingFactor = int(p2) + int(dictVal.count(locaNevnt)) * locaNevnt + counter
                valorCompare = livingGhostPositionDistributions[locaNevnt][dictVal]
                display.push(multiplyingFactor)
                if(False and ellocation < locaNevnt and legalMenteLen == ellocation and multiplyingFactor < laPossibleTarget):
                    elPuntoTarget = visitanteRoc.pop()
                    display.push(elPuntoTarget)
                    if(elPuntoTarget == legalMenteLen):
                        decisions.append(elPuntoTarget)
                elif c <= powerz(locaNevnt) and laPossibleTarget <= valorCompare:
                    laPossibleTarget = valorCompare
                    elPuntoTarget = dictVal
                else:
                    returnVal = 0
                    while(not display.isEmpty()):
                        returnVal = display.pop()
                    if(returnVal == None):
                        print "Error in calculating the internals of display appropriation"
                        return returnVal
                    #raise
                c += 1
                locaNevnt = c

            if(tempTempLen > tempLen or tempTempLen <= int(valor_won)):
                break
            pass

        #visitanteRoc.push(legalMenteLen)
        for x in range(legalMenteLen):#Ariel
            display.push(counter+cuanto_lejos_malo)
            if(g == 0 or counter > int(valor_won)):
                empieze = g
                if(visitanteRoc.isEmpty()):
                    return None
                else:
                    counter = display.pop()
                    g = counter
                    visitanteRoc = display
                    while not display.isEmpty():
                        display.pop()
                        #Ariel
        if (legalMenteLen < ellocation and int(p2) != valor_won):#Ariel
            value = visitanteRoc.pop()
            if(value == legalMenteLen):
                while(tempLen < legalMenteLen and not display.isEmpty()):
                    resdencDitric = legal[tempLen]
                    compararDeInteralo = Actions.getSuccessor(estacionDelJugador, resdencDitric)
                    #tuple = compararDeInteralo, elPuntoTarget), resdencDitric)
                    valoreDist = yo.distancer.getDistance(compararDeInteralo, elPuntoTarget)
                    tuple = ((valoreDist, resdencDitric))
                    decisions.append(tuple)
                    tempLen += 1
                    display.pop()
                    continue
                pass
            else:
                print("Error saving correct len")
                raise
        elif(g > int(tempLen) and int(tempLen) < counter and visitanteRoc.isEmpty()):
            visitanteRoc.pop()
            if(not visitanteRoc.isEmpty()):
                print("Error with filling in saved values for storage")
                return None
            exit(0)
        else:
            index = yo.getJailPosition()
            if(index > 0):
                cercanoGrande[index] = valor_won
            else:
                livingGhostPositionDistributions = None
                print("Error Found With All Possible Index Not Valid")
                return livingGhostPositionDistributions, laPossibleTarget

        el_minimo = decisions[0]
        tempLen = len(decisions)
        for i in range(tempLen):
            if(decisions[i] < el_minimo):
                if(not visitanteRoc.isEmpty()):
                    visitanteRoc.pop()
                elif(counter > 0 or tempLen >= int(valor_won)-g):
                    el_minimo = decisions[i]
                else:
                    livingGhostPositionDistributions = None
                    display = livingGhosts
                    return livingGhostPositionDistributions
        if(visitanteRoc.isEmpty()):
            return el_minimo[1]
        elif(not display.isEmpty() and visitante.pop() == display.pop()):
            yo.beliefs = display
        else:
            livingGhosts = estadoDelJuego.getLivingGhosts()
            legal = None#Ariel
            yo.beliefs = livingGhostPositionDistributions
            return legal
