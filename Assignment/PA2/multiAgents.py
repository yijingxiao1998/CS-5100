# multiAgents.py
# --------------
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


from cmath import inf
from util import manhattanDistance
from game import Directions
import random, util

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()  # direct for next step, {NORTH, SOUTH, WEST, EAST, STOP}

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]  # get next stp weight score by evaluate function 
        bestScore = max(scores)  # pick the best score
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]  # choose action step according to best score
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
        successorGameState = currentGameState.generatePacmanSuccessor(action) # get current game state (G is Ghost, % is wall, and ^ is pacman)
        newPos = successorGameState.getPacmanPosition() # get new position for each move
        newFood = successorGameState.getFood() # get the food distribution in game graph (T for having food, F for not)
        newGhostStates = successorGameState.getGhostStates() # get the Ghost position
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] # rest of scared time after pacman ate power pellet

        "*** YOUR CODE HERE ***"
        foods = newFood.asList()  # get all food's position

        curr_score = 0  # define a evaluate score
        # if current state could make ghost scared, then add it to score
        for scaredTime in newScaredTimes:
            curr_score += scaredTime
        
        # get distance between current position and ghost position
        ghostDis = float(inf)
        for ghostPos in newGhostStates:
           dis = util.manhattanDistance(newPos, ghostPos.getPosition())
           ghostDis = min(dis, ghostDis)
        #get distance between current position and food position
        foodDis = float(inf)
        for foodPos in foods:
            dis = util.manhattanDistance(newPos, foodPos)
            foodDis = min(dis, foodDis)
        # As features, try the reciprocal of important values (such as distance to food) rather than just the values themselves
        curr_score += 10 / foodDis
        if ghostDis != 0: # didn't meet ghost
            curr_score += -1/ghostDis
        else:
            curr_score += -100
        
        # get current system score since we may eat pellet to get high score
        curr_score += successorGameState.getScore()
        return curr_score

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
    def minimaxDecision(self, gameState): # return an action
        depth = 0
        # check next possible action for pacman
        pacActions = gameState.getLegalActions(0) # Returns a list of legal actions for an agent (agentIndex=0 means Pacman, ghosts are >= 1)
        
        maximum, action = float('-inf'), ''
        # for next possible action, pick one move which has highest win probability
        for pacAct in pacActions:
            # and this move also has lowest win probability for ghost
            curr_max = self.min_value(gameState.generateSuccessor(0, pacAct), depth, 1)
            if curr_max > maximum:
                maximum = curr_max
                action = pacAct
        return action
    
    def max_value(self, gameState, depth):
        depth += 1
        # check state first, if win or lose or reach the self.depth, then return evaluateFun
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        v = float('-inf') # initialized v
        # get max for each min branch
        for pacAct in gameState.getLegalActions(0):
            v = max(v, self.min_value(gameState.generateSuccessor(0, pacAct), depth, 1))
        return v

    def min_value(self, gameState, depth, ghosts):
        # check state first, if win or lose, then return evaluateFun
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        v = float('inf') # initialized v
        # get min for each max, we have a lot ghost branchs since there are many ghosts
        # minimax tree will have multiple min layers (one for each ghost) for every max layer.
        for action in gameState.getLegalActions(ghosts):
            if ghosts == gameState.getNumAgents() - 1: # since agentIndex of ghosts are >= 1, if ghosts's number is equal to agents number minus 1,
                # it means that we've already found all of ghosts min, we shall begin to find next max
                v = min(v, self.max_value(gameState.generateSuccessor(ghosts, action), depth))
            else:
                # keep going for next ghost
                v = min(v, self.min_value(gameState.generateSuccessor(ghosts, action), depth, ghosts+1))
        return v

    def getAction(self, gameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.minimaxDecision(gameState)
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def alphaBetaSearch(self, gameState):
        # check next possible action for pacman
        pacActions = gameState.getLegalActions(0) # Returns a list of legal actions for an agent (agentIndex=0 means Pacman, ghosts are >= 1)
        
        maximum, alpha, beta= float('-inf'), float('-inf'), float('inf')
        action = ''
        # for next possible action, pick one move which has highest win probability
        for pacAct in pacActions:
            depth = 0
            # and this move also has lowest win probability for ghost
            curr_max = self.min_value(gameState.generateSuccessor(0, pacAct), depth, 1, alpha, beta)
            if curr_max > maximum:
                maximum = curr_max
                action = pacAct
            
            alpha = max(alpha, curr_max)
        return action

    def max_value(self, gameState, depth, alpha, beta):
        depth += 1
        # check state first, if win or lose or reach the self.depth, then return evaluateFun
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        v = float('-inf') # initialized v
        # get max for each min branch
        for pacAct in gameState.getLegalActions(0):
            v = max(v, self.min_value(gameState.generateSuccessor(0, pacAct), depth, 1, alpha, beta))
            if v > beta:  # if v have already bigger than beta, we don't have to keep comparing
                return v
            alpha = max(alpha, v)  # update value of alpha
        return v

    def min_value(self, gameState, depth, ghosts, alpha, beta):
        # check state first, if win or lose, then return evaluateFun
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        v = float('inf') # initialized v
        # get min for each max, we have a lot ghost branchs since there are many ghosts
        # minimax tree will have multiple min layers (one for each ghost) for every max layer.
        for action in gameState.getLegalActions(ghosts):
            if ghosts == gameState.getNumAgents() - 1: # since agentIndex of ghosts are >= 1, if ghosts's number is equal to agents number minus 1,
                # it means that we've already found all of ghosts min, we shall begin to find next max
                v = min(v, self.max_value(gameState.generateSuccessor(ghosts, action), depth, alpha, beta))
            else:
                # keep going for next ghost
                v = min(v, self.min_value(gameState.generateSuccessor(ghosts, action), depth, ghosts+1, alpha, beta))
            
            if v < alpha: # if v have already bigger than alpha, we don't have to keep comparing
                return v
            beta = min(beta, v) # update value of beta
        return v

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.alphaBetaSearch(gameState)
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expectMax(self, gameState, depth):
        # check next possible action for pacman
        pacActions = gameState.getLegalActions(0) # Returns a list of legal actions for an agent (agentIndex=0 means Pacman, ghosts are >= 1)
        
        maximum, action = float('-inf'), ''
        # for next possible action, pick one move which has highest win probability
        for pacAct in pacActions:
            # and this move also has lowest win probability for ghost
            curr_max = self.exp_value(gameState.generateSuccessor(0, pacAct), depth, 1)
            if curr_max > maximum:
                maximum = curr_max
                action = pacAct
        return action
    
    def max_value(self, gameState, depth):
        depth += 1
        # check state first, if win or lose or reach the self.depth, then return evaluateFun
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        v = float('-inf') # initialized v
        # get max for each exp branch
        for pacAct in gameState.getLegalActions(0):
            v = max(v, self.exp_value(gameState.generateSuccessor(0, pacAct), depth, 1))
        return v

    def exp_value(self, gameState, depth, ghosts):
        # check state first, if win or lose, then return evaluateFun
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        v = 0
        prob = 1 / len(gameState.getLegalActions(ghosts))
        # get exp for each max, we have a lot ghost branchs since there are many ghosts
        for action in gameState.getLegalActions(ghosts):
            if ghosts == gameState.getNumAgents() - 1: # since agentIndex of ghosts are >= 1, if ghosts's number is equal to agents number minus 1,
                # it means that we've already get all of ghosts, we shall begin to find next max
                v += prob * self.max_value(gameState.generateSuccessor(ghosts, action), depth)
            else:
                # keep going for next ghost
                v += prob * self.exp_value(gameState.generateSuccessor(ghosts, action), depth, ghosts+1)
        return v

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectMax(gameState, 0)
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    The goal of Pacman is eat all food as soon as possible, hence we could weight the food similar with Reflex Agent
    If the pacman just ate food, then he could get "reward" so that he will keep finding food
    However, if Pacman almost meet ghost, then he will get "penalty" so that he know he could not go that way
    Besides, after ate power pellet the Pacman will not fear ghost any more, he even could go to scare ghosts
    Overall, we could set food weight to positive and ghost weight to negative
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
    newPos = currentGameState.getPacmanPosition() # get new position for each move
    newFood = currentGameState.getFood() # get the food distribution in game graph (T for having food, F for not)
    newGhostStates = currentGameState.getGhostStates() # get the Ghost position
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] # rest of scared time after pacman ate power pellet
    
    curr_score = 0  # define a evaluate score

    foods = newFood.asList()  # get all food's position
    # get distances between current position and food position
    foodDis = float(inf)
    for foodPos in foods:
        dis = util.manhattanDistance(newPos, foodPos)
        foodDis = min(dis, foodDis)

    # Closer food, more reward 
    curr_score += 10 / foodDis

    # if current state could make ghost scared, then add it to score
    for scaredTime in newScaredTimes:
        curr_score += scaredTime
        
    # get distance between current position and ghost position
    ghostDis = float(inf)
    for ghostPos in newGhostStates:
        dis = util.manhattanDistance(newPos, ghostPos.getPosition())
        ghostDis = min(dis, ghostDis)
    if ghostDis != 0: # didn't meet ghost
        curr_score += -1 / ghostDis
        
    # get current system score since we may eat pellet to get high score
    curr_score += currentGameState.getScore()
    return curr_score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
