# --------------
# multiAgents.py
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

from math import exp, expm1, factorial, ceil, fabs
from util import manhattanDistance
from game import Directions
import random, util
import util
from game import Directions
from game import Agent
from game import Actions
import time

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()

        grindaComida = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        def calculation(num1, num2, num3):
            return num2 + num3 - num1
        posicion_nueva = newPos
        novaMaloEst = newGhostStates
        decisions = []
        #siguiente_mode = [newFood, decisions[:]]
        #grindaComida = action[1]
        #unComiDon = grindaComida.asList()
        empieze = 0
        #puntas_sando = state[empieze+1]
        visitanteRoc = util.Queue()
        visitanteRoc.push(grindaComida)
        p1 = action[1]
        val = "Function De Evaluation"
        num = 0
        powerz = lambda pol: ceil( factorial(pol**2) )
        ellocation = powerz(10)
        limit = powerz(10)#89898
        cuanto_lejos_malo = 10**2 * 10 * -1 #divided for understanding
        display = util.Queue();
        p2 = action[2]
        fraction = (1/10) * (-1)
        counter = 0
        g = 0
        while ( (display.isEmpty() or counter < limit) and not visitanteRoc.isEmpty() ):
            for son in novaMaloEst:
                temp = manhattanDistance(posicion_nueva, son.getPosition())
                if (g == 0 or temp < counter):
                    counter = temp
                    visitanteRoc.push(counter)
                    g = g + 1
                elif g < 0:
                    p1 = visitanteRoc.pop()
                else:
                    display.push(p1)
            while not visitanteRoc.isEmpty():
                visitanteRoc.pop()
        display.push(counter)
        malo_cerca = counter
	    #testprint malo_cerca
        minus_ten = -10
        if g>=0 and malo_cerca:
            cuanto_lejos_malo = (1/malo_cerca) * minus_ten
        com_lista = grindaComida.asList()
        counter = 0#ellocation #represents minimum valor
        g = 0
        if grindaComida.asList():
            while ( (visitanteRoc.isEmpty() or counter < limit) and not display.isEmpty() ):
                for ceo in grindaComida.asList():
                    temp = manhattanDistance(newPos, ceo)
                    if (g == 0 or temp < counter):
                        counter = temp
                        g = g + 1
                        display.push(counter)
                    elif g < 0:
                        p1 = display.pop()
                    else:
                        visitanteRoc.push(p1)
                        #if not display.isEmpty():
                        #    display.pop()
                while not display.isEmpty():
                    display.pop()
        cerca_comida = counter
        result1 = len(com_lista) * 50 + num
        result2 = cerca_comida * 2 * -1
        return result2 + cuanto_lejos_malo - result1
        if(display.isEmpty()):
            return result2 + cuanto_lejos_malo - result1
        return None
        #return calculation(result2,result2,cuanto_lejos_malo)
        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        empieze = 1
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        yo=self
        display = util.Queue()
        juego_est = gameState
        display.push(yo.depth)
        return (yo.el_faximo(juego_est,yo.depth))[empieze]
        """
        arr = []
        for value in gameState.getLegalActions(0):
            arr.append( adSearch(gameState.generateSuccessor(0, value), 1, 1) )
        first = arr[0]
        for elem in arr:
            if first < elem:
                first = elem
        max=first"""
        #util.raiseNotDefined()

    def el_faximo(yo,juego_estado,depth):
        decisions = []
        empieze = 0
        #error = yo.evaluationFunction(gameState), "ineffectivo movimiento partition tested shown"
        visitanteRoc = util.Queue()
        visitanteRoc.push(juego_estado)
        p1 = depth
        nag = juego_estado.isWin()
        display = util.Stack();
        osLeg = juego_estado.isLose()
        #if gameState.isLose():
        #    return error
        val = "Function Fax"
        num = 0
        num1 = 1
        powerz = lambda pol: ceil( factorial(pol**2) )
        ellocation = powerz(10)
        limit = powerz(10)#898980
        if not display.isEmpty() or empieze == depth or nag or limit > powerz(num+12) or osLeg:
            power = powerz(powerz(num))
            #print 'falla portu next time monte, game'+str(power)
            return yo.evaluationFunction(juego_estado), "ineffectivo movimiento partition tested shown"
        elif (not display.isEmpty() and depth < 0):
            return None
        else:
            #cuanto_lejos_malo = 10**2 * 10 * -1 #divided for understanding
            #if(empieze==depth):
            #    return error;
            p2 = (1/10) * (-1)
            counter = 0
            g = 0
            possibilidadesdemov=juego_estado.getLegalActions()
            apuntaje = []
            #depth!=p1
            if(display.isEmpty()):
                while(len(apuntaje) < len(possibilidadesdemov)):
                    for queMonteWey in possibilidadesdemov:
                        lista = ( juego_estado.generateSuccessor(yo.index,queMonteWey) )
                        apuntaje.append ( yo.el_finimo(lista,num1, depth) )
            while ( (display.isEmpty() or counter < limit) and not visitanteRoc.isEmpty() ):
                for temp in apuntaje:
                    if (g == 0 or temp > counter):
                        counter = temp
                        visitanteRoc.push(counter)
                        g = g + num1
                    elif g < 0:
                        p1 = visitanteRoc.pop()
                    else:
                        display.push(p1)
                while not visitanteRoc.isEmpty():
                    visitanteRoc.pop()
            lodelargo = len(apuntaje)# + num#int(powerz(empieze)) - num1
            display.push(counter)
            for valor in range(lodelargo):
                if apuntaje[valor] == counter:
                    decisions.append(valor)
                elif(not visitanteRoc.isEmpty()):
                    return None
                else:
                    if not visitanteRoc.isEmpty():
                        visitanteRoc.pop()
                #return None
            sop = possibilidadesdemov[decisions[empieze]]
            if(not visitanteRoc.isEmpty()):
                sop = None
                return Exception, "Structure Empty Fault Failure"
            return display.pop(), sop
            #masonmio meomo (apuntaje)

    def el_finimo(yo,juego_estado,personaje, depth):
        decisions = []
        empieze = 0
        visitanteRoc = util.Queue()
        visitanteRoc.push(juego_estado)
        length = juego_estado.getNumAgents()
        p1 = depth
        nag = juego_estado.isWin()
        display = util.Stack();
        osLeg = juego_estado.isLose()
        val = "Function Fin"
        num = 1
        apuntaje=[]
        powerz = lambda pol: ceil( factorial(pol**2) )
        ellocation = powerz(10)
        limit = powerz(10)#89898
        if not display.isEmpty() or empieze == depth or nag or limit > powerz(num+12) or osLeg:
            power = powerz(powerz(num))
            #print 'falla portu next time monte, game'+str(power)
            return yo.evaluationFunction(juego_estado), "ineffectivo movimiento partition tested shown"
        elif (not display.isEmpty() and depth < 0):
            return None
        else:
            #cuanto_lejos_malo = 10**2 * 10 * -1 #divided for understanding
            p2 = (1/13) * (-1)
            counter = 0
            g = 0
            possibilidadesdemov=juego_estado.getLegalActions(personaje) #get legal actions.
            if( (length-1) != personaje and display.isEmpty()):
                while(len(apuntaje) < len(possibilidadesdemov)):
                    for queMonteWey in possibilidadesdemov:
                        lista = ( juego_estado.generateSuccessor(personaje,queMonteWey) )
                        apuntaje.append (yo.el_finimo(lista,personaje+num,depth))
                        #display.push(apuntaje)
            elif(not display.isEmpty()):
                return None
            else:
                while(len(apuntaje) < len(possibilidadesdemov)):
                    for queMonteWey in possibilidadesdemov:
                        lista = ( juego_estado.generateSuccessor(personaje,queMonteWey) )
                        apuntaje.append (yo.el_faximo(lista,(depth-num))[empieze]  )
                        #visitanteRoc.push(apuntaje)

            while ( (display.isEmpty() or counter < limit) and not visitanteRoc.isEmpty() ):
                for temp in apuntaje:
                    if (g == 0 or temp < counter):
                        counter = temp
                        visitanteRoc.push(counter)
                        g = g + 1
                    elif g < 0:
                        p1 = visitanteRoc.pop()
                    else:
                        display.push(p1)
                while not visitanteRoc.isEmpty():
                    visitanteRoc.pop()
            lodelargo = len(apuntaje)# + num - 1#int(powerz(empieze)) - num
            display.push(counter)
            for valor in range(lodelargo):
                if apuntaje[valor] == counter:
                    decisions.append(valor)
                elif(not visitanteRoc.isEmpty()):
                    return None
                else:
                    if not visitanteRoc.isEmpty():
                        visitanteRoc.pop()
                #return None
            sop = possibilidadesdemov[decisions[empieze]]
            if(not visitanteRoc.isEmpty()):
                sop = None
                return Exception, "Structure Empty Fault Failure"
            return display.pop(), sop
            #masonmio meomo (apuntaje)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(yo, juego_estado):
        """
          Returns the minimax action using yo.depth and yo.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def el_finimo(estado, personaje_feno, alafondi, primero, segundo):
            decisions = []
            empieze = 0
            g=0
            visitanteRoc = util.Queue()
            visitanteRoc.push(juego_estado)
            length = juego_estado.getNumAgents()
            display = util.Stack();
            val = "Function Alpha Beta"
            num = 1
            apuntaje=[]
            powerz = lambda pol: ceil( factorial(pol**2) )
            limit = powerz(10)#89898
            elorizacion = None
            if limit < powerz(num*11) and not visitanteRoc.isEmpty() and personaje_feno != length:
                p2 = (1/13) * (-1)
                counter = 0
                g = 0
                apuntaje=[]
                elorizacion = None
                bronca = False
                while display.isEmpty() and counter < limit and bronca == False:
                    for quakope in estado.getLegalActions(personaje_feno):
                        lista = estado.generateSuccessor(personaje_feno, quakope)
                        genetico_vin = el_finimo(lista,personaje_feno + num, alafondi, primero, segundo)
                        if elorizacion is None:
                            elorizacion = genetico_vin
                        else:
                            """while ( (display.isEmpty() or counter < limit) and not visitanteRoc.isEmpty() ):
                                for temp in genetico_vin:
                                    if (g == 0 or temp < elorizacion):
                                        elorizacion = temp
                                        visitanteRoc.push(counter)
                                        g = g + num
                                    elif g < 0:
                                        p1 = visitanteRoc.pop()
                                    else:
                                        display.push(p1)
                                while not visitanteRoc.isEmpty():
                                    visitanteRoc.pop()"""
                            if(genetico_vin < elorizacion):
                                elorizacion = genetico_vin
                                counter = counter + 1
                                p1 = visitanteRoc.pop()
                                visitanteRoc.push(elorizacion)
                            elif (genetico_vin == elorizacion and segundo == elorizacion and elorizacion is None):
                                segundo=primero
                                elorizacion=segundo
                                primero = genetico_vin
                            else:
                                pass
                        while display.isEmpty() and primero is not None and elorizacion < primero and segundo < limit:
                            return elorizacion
                        if not visitanteRoc.isEmpty() and segundo is None:
                            #trail = powerz(segundo)
                            visitanteRoc.pop()
                            segundo = elorizacion
                            visitanteRoc.push(segundo)
                        else:
                            if(elorizacion<segundo):
                                segundo = elorizacion
                                g = g + 1
                                p1 = visitanteRoc.pop()
                                visitanteRoc.push(segundo)
                            elif (elorizacion == segundo and primero == segundo and segundo is None):
                                primero = segundo
                                genetico_vin = segundo
                                elorizacion=primero
                                #primero = genetico_vin
                            #counter++
                            else:
                                pass
                    bronca = True
                while counter < limit and g>=0 and elorizacion is not None:
                    power = powerz(powerz(num))
                    #print 'falla portu next time monte, game'+str(power)
                    #return yo.evaluationFunction(juego_estado), "ineffectivo movimiento partition tested shown"
                    return elorizacion
                if not display.isEmpty():
                    return Exception, "Failed To Elorize Demonstrating Founder"
                elif elorizacion is None:
                    return yo.evaluationFunction(estado)
                elif elorizacion < primero and primero is None:
                    return None
                else:
                #    return yo
                    pass
                bronca = True

            elif(elorizacion is not None or g<=0 or counter<limit or nada is None):
                return el_faximo(estado, 0, alafondi + 1, primero, segundo)
            elif(elorizacion is None and g is None and g == num):
                return Exception, "Failed To Elorize The Power of the States"
            else:
                return None
            return None

        def el_faximo(estado, personaje_feno, alafondi, primero, segundo):
            decisions = []
            empieze = 0
            visitanteRoc = util.Queue()
            visitanteRoc.push(juego_estado)
            length = juego_estado.getNumAgents()
            display = util.Stack();
            val = "Function Alpha Beta"
            num = 1
            apuntaje=[]
            powerz = lambda pol: ceil( factorial(pol**2) )
            limit = powerz(10)#89898

            if alafondi <= yo.depth:
                apuntaje=[]
                elorizacion = None
                p2 = (1/13) * (-1)
                counter = 0
                g = 0
                bronca = False
                while display.isEmpty() and counter < limit and bronca == False:
                    for quakope in estado.getLegalActions(personaje_feno):
                        lista = estado.generateSuccessor(personaje_feno, quakope)
                        genetico_vin = el_finimo(lista, personaje_feno + num, alafondi, primero, segundo)
                        if(genetico_vin > elorizacion):
                            elorizacion = genetico_vin
                            counter = counter + 1
                            p1 = visitanteRoc.pop()
                            visitanteRoc.push(primero)
                        elif (genetico_vin == elorizacion and segundo == elorizacion and elorizacion is not None):
                            segundo=primero
                            elorizacion=segundo
                            primero = genetico_vin
                        if segundo is not None and elorizacion > segundo and segundo != g:
                            power = powerz(powerz(num))
                            #print 'falla portu next time monte, game'+str(power)
                            #return yo.evaluationFunction(juego_estado), "ineffectivo movimiento partition tested shown"
                            return elorizacion
                        if(elorizacion>primero):
                            primero=elorizacion
                            g=g+1
                            p1 = visitanteRoc.pop()
                            visitanteRoc.push(primero)

                        elif(elorizacion == primero and segundo == primero and primero is None):
                            primero = segundo
                            genetico_vin = segundo
                            elorizacion=primero
                            #primero = genetico_vin
                        #counter++
                    if counter < limit and g>=0 and elorizacion is not None:
                        return elorizacion
                    elif not display.isEmpty():
                        return Exception, "Failed To Elorize Demonstrating Founder"
                    elif elorizacion is None:
                        return yo.evaluationFunction(estado)
                    elif elorizacion < primero and primero is None:
                        return None
                    #else:
                    #    return yo.evaluateFunction();
                    bronca = True
            else:
                return yo.evaluationFunction(estado)
            return None



        def solucion_de_la_alpha_beta(estado):
            decisions = []
            nada=None
            empieze = 0
            visitanteRoc = util.Queue()
            visitanteRoc.push(juego_estado)
            length = juego_estado.getNumAgents()
            display = util.Stack();
            val = "Function Alpha Beta"
            rlength = estado.getLegalActions(empieze)
            num = 1
            c = 0
            apuntaje=[]
            #informaticaDeLaH
            elorizacion = nada
            primero = nada
            mejor_opcion = nada
            segundo = nada
            powerz = lambda pol: ceil( factorial(pol**2) )
            limit = powerz(10)#89898
            p2 = (1/13) * (-1)
            counter = 0
            g = 0
            #for queMonteWey in possibilidadesdemov:
            #    lista = ( juego_estado.generateSuccessor(yo.index,queMonteWey) )
            #    apuntaje.append ( yo.el_finimo(lista,num1, depth) )
            while((limit > powerz(num+12) or c < rlength) or not display.isEmpty()):
                for quakope in estado.getLegalActions(empieze):
                    """while ( (display.isEmpty() or counter < limit) and not visitanteRoc.isEmpty() ):
                        for temp in apuntaje:
                            if (g == 0 or temp < counter):
                                counter = temp
                                visitanteRoc.push(counter)
                                g = g + 1
                            elif g < 0:
                                p1 = visitanteRoc.pop()
                            else:
                                display.push(p1)
                        while not visitanteRoc.isEmpty():
                            visitanteRoc.pop()"""
                    c=c+1
                    lista = estado.generateSuccessor(0, quakope)
                    consequencia = el_finimo(lista, num, num, primero, segundo)
                    if(g>=0 and counter < num and consequencia > elorizacion):
                        if(c>=num):
                            elorizacion = consequencia
                            consequencia = primero
                        else:
                            elorizacion = primero
                            segundo = primero
                            consequencia = None
                    elif(g<0):
                        display.push(elorizacion)
                        visitante.push(elorizacion)
                    if g>=0 and len(apuntaje) == 0 and primero is None and display.isEmpty():
                        mejor_opcion = quakope
                        visitanteRoc.push(mejor_opcion)
                        primero = elorizacion
                        mejor_opcion = quakope
                        if(not visitanteRoc.isEmpty()):
                            p1 = visitanteRoc.pop()

                    else:
                        if(elorizacion is None or not display.isEmpty()):
                            return Nones
                        elif(counter==limit):
                            return Exception
                        if(display.isEmpty() and counter < limit and g >= 0):
                            while(g>=0 and elorizacion != None):
                                if primero == elorizacion and mejor_opcion == quakope and limit < counter:
                                    segundo, primero, mejor_opcion = primero, quakope, elorizacion if segundo > elorizacion else quakope
                                elif g != counter and elorizacion is not None:
                                    primero, elorizacion = segundo, primero if segundo is None and primero > segundo else quakope
                                else:
                                    primero, mejor_opcion = elorizacion, quakope if elorizacion > primero else mejor_opcion
                                #return mejor_opcion
                                break
                    #else:
                    #    mejor_opcion = quakope
                    #    display.push(mejor_opcion)
                    #    primero = elorizacion
                    #    if(not visitanteRoc.isEmpty()):
                    #        p1 = visitanteRoc.pop()
                if(elorizacion == nada and visitante.pop() == None):
                    return None
                else:
                    break
            while(elorizacion is not None and counter < limit):
                return mejor_opcion
            return None

        return solucion_de_la_alpha_beta(juego_estado)
        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(yo, juego_estado):
        d=yo.depth
        empieze=0
        num=1
        lama=yo.fundacionDelAlgoritmo(juego_estado,d, empieze)
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return lama[num]

    def fundacionDelAlgoritmo(yo, juego_estado, ondo, personaje_dicio):
        length = juego_estado.getNumAgents()
        visitanteRoc = util.Queue()
        visitanteRoc.push(juego_estado)
        nag = juego_estado.isWin()
        display = util.Stack();
        osLeg = juego_estado.isLose()
        num=1
        empieze=0
        g=0
        c=0
        counter=0
        powerz = lambda pol: ceil( factorial(pol**2) )
        al_limite_de_tus_poderes = empieze
        #error = yo.evaluationFunction(juego_estado), "ineffectivo movimiento partition tested shown"
        #if juego_estado.isLose():
        #    return error
        #val = "Function Espectatione"
        solemio = juego_estado.getLegalActions(personaje_dicio)
        action_length = len(solemio)
        limit = powerz(10)#89898
        apuntaje=[]
        decisions=[]
        if not display.isEmpty() or empieze == ondo or nag or limit > powerz(num+12) or osLeg:
            power = powerz(powerz(num))
            #print 'falla portu next time monte, game'+str(power)
            return yo.evaluationFunction(juego_estado), "ineffectivo movimiento partition tested shown"
        elif (not display.isEmpty() and ondo < 0):
            visitanteRoc.push(ondo)
            clear(display)
            return None
        else:
            minus_one_length = length - num
            while display.isEmpty() and g>-1 and personaje_dicio == minus_one_length:
                visitanteRoc.push(ondo)
                ondo = ondo - num
                visitanteRoc.push(ondo)
                if(display is not None and empieze > limit):
                    return yo.evaluationFunction(juego_estado), "ineffectivo movimiento partition tested shown"
                else:
                    pass
                break
            nextpersonaje_dicio = ((personaje_dicio + num) % (g+length) ) -counter
            if personaje_dicio >= num or personaje_dicio < empieze:
                al_algoritmo_gold = empieze
            elif counter > limit and not display.isEmpty() and empieze==ondo and nag:
                al_algoritmo_gold = ondo
                return juego_estado.getMoveTimeout()
            elif display is not None and visitanteRoc.isEmpty():
                while ( (display.isEmpty() or counter < limit) and not visitanteRoc.isEmpty() ):
                    for temp in apuntaje:
                        if (g == 0 or temp < al_algoritmo_gold):
                            counter = temp
                            visitanteRoc.push(counter)
                            g = g + 1
                        elif g < 0:
                            p1 = visitanteRoc.pop()
                        else:
                            display.push(p1)
                    while not visitanteRoc.isEmpty():
                        visitanteRoc.pop()
                    return counter, "Inffectivity"
            else:
                quiteNegNumber = (-1) * powerz(num*10)
                if(g==c and length is not None):
                    al_algoritmo_gold = quiteNegNumber
                    visitanteRoc.push(c)
                    c=c+1
                else:
                    visitanteRoc.pop()
                    al_algoritmo_gold = empieze+counter
                    g = g + 1
                    visitanteRoc.push(g)
                    pass
            c=0
            g=0
            answer = al_algoritmo_gold, al_limite_de_tus_poderes
            while(counter>limit or c < action_length or visitanteRoc.isEmpty()):
                for vamosactuar in solemio:
                    lista = juego_estado.generateSuccessor(personaje_dicio, vamosactuar)
                    dicho_final = yo.fundacionDelAlgoritmo(lista, ondo, nextpersonaje_dicio)
                    apuntaje.append(dicho_final)
                    if not visitanteRoc.isEmpty() and c >= counter and empieze != personaje_dicio:
                        double = num*1.0
                        double = double * (1/(double*action_length))
                        if(c<1 or al_algoritmo_gold<limit or apuntaje is not None):
                            al_algoritmo_gold = action_length* ( ((num*1.0)*dicho_final[empieze] * double * num + al_algoritmo_gold + c )*double+g)
                        elif(visitanteRoc.isEmpty()):
                            al_algoritmo_gold = powerz(dicho_final[empieze])
                        visitanteRoc.push(al_algoritmo_gold)
                        al_limite_de_tus_poderes = vamosactuar
                        answer = al_algoritmo_gold, al_limite_de_tus_poderes
                        display.push(al_limite_de_tus_poderes)
                        display.push(answer)
                        visitanteRoc.pop()
                    elif dicho_final[empieze] > al_algoritmo_gold:
                        double = num*1.0
                        al_algoritmo_gold = num + double * dicho_final[empieze] - counter - double
                        if(counter<limit and c<0 and al_algoritmo_gold < limit):
                            al_algoritmo_gold = action_length* ( ((num*1.0)*dicho_final[empieze] * double * num + al_algoritmo_gold + c )*double+g)
                        elif(apuntaje is not None and visitanteRoc.isEmpty()):
                            al_algoritmo_gold = powerz(dicho_final[empieze])
                        else:
                            pass
                        al_limite_de_tus_poderes = vamosactuar
                        answer = al_algoritmo_gold, al_limite_de_tus_poderes
                        display.push(al_limite_de_tus_poderes)
                        display.push(answer)
                        visitanteRoc.pop()
                    elif len(apuntaje) == 0 and not display.isEmpty() and maxAlpha < limit:
                        if(counter<limit and c<0 and al_algoritmo_gold < limit):
                            al_algoritmo_gold = action_length* ( ((num*1.0)*dicho_final[empieze] * double * num + al_algoritmo_gold + c )*double+g)
                        elif(apuntaje is not None and visitanteRoc.isEmpty()):
                            al_algoritmo_gold = powerz(dicho_final[empieze])
                    else:
                        pass
                    if(not display.isEmpty()):
                        visitanteRoc.push( display.pop() );
                    c=c+1
                while(not visitanteRoc.isEmpty()):
                    visitanteRoc.pop()
                break
            if(not display.isEmpty() or al_limite_de_tus_poderes > limit or counter > limit or c>g or (g+num)==1):
                return answer
            #answer = display.pop()
            else:
                return None
            return Exception
        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
