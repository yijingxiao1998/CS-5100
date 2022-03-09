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

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    initial_node = (problem.getStartState(), []) # initialize the initial-state node
    frontier = util.Stack() # use LIFO stack
    frontier.push(initial_node) # initialize the frontier
    explored = list() # initialize the explored set
    while not frontier.isEmpty():
        curr_node = frontier.pop() # last node in frontier
        curr_state, curr_path = curr_node[0], curr_node[1]
        if curr_state not in explored:
            explored.append(curr_state) # add curr_node state to explored
            if problem.isGoalState(curr_state):
                return curr_path
            for successor in problem.getSuccessors(curr_state):
                next_state, action = successor[0], successor[1]
                frontier.push((next_state, curr_path+[action]))
    return []
    util.raiseNotDefined()

    """
    Question 1: Is the exploration order what you would have expected? 
    Does Pacman actually go to all the explored squares on his way to the goal?
    Answer: We use DFS and it explores all possible paths to the maximum depth
    but it cannot guarantee the solution is optimal, thus the exploration order
    is not we would have expected. Moreover, the Pacman dose not actually go to 
    all the explored squares on his way to the goal.
    """

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    initial_node = (problem.getStartState(), []) # initialize the initial-state node
    frontier = util.Queue() # use FIFO queue
    frontier.push(initial_node) # initialize the frontier
    explored = list() # initialize the explored set
    while not frontier.isEmpty():
        curr_node = frontier.pop() # first node in frontier
        curr_state, curr_path = curr_node[0], curr_node[1]
        if curr_state not in explored:
            explored.append(curr_state) # add curr_node state to explored
            if problem.isGoalState(curr_state):
                return curr_path
            for successor in problem.getSuccessors(curr_state):
                next_state, action = successor[0], successor[1]
                frontier.push((next_state, curr_path+[action]))
    return []
    util.raiseNotDefined()

    """
    Question 2: Does BFS find a least cost solution? If not, check your implementation.
    Answer: Yes, it find a solution. 
    """

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    initial_node = (problem.getStartState(), []) # initialize the initial-state node
    frontier = util.PriorityQueue() # use priority queue
    frontier.push(initial_node, 0) # initialize the frontier
    explored = list() # initialize the explored set
    while not frontier.isEmpty():
        curr_node = frontier.pop() # minimum-cost node in frontier
        curr_state, curr_path = curr_node[0], curr_node[1]
        if curr_state not in explored:
            explored.append(curr_state) # add curr_node state to explored
            if problem.isGoalState(curr_state):
                return curr_path
            for successor in problem.getSuccessors(curr_state):
                next_state, action = successor[0], successor[1]
                next_node = (next_state, curr_path+[action])
                frontier.update(next_node, problem.getCostOfActions(curr_path+[action]))
    return []
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    initial_node = (problem.getStartState(), []) # initialize the initial-state node
    frontier = util.PriorityQueue() # use priority queue
    frontier.push(initial_node, heuristic(problem.getStartState(), problem)) # initialize the frontier
    explored = list() # initialize the explored set
    while not frontier.isEmpty():
        curr_node = frontier.pop() # minimum-cost node in frontier
        curr_state, curr_path = curr_node[0], curr_node[1]
        if curr_state not in explored:
            explored.append(curr_state) # add curr_node state to explored
            if problem.isGoalState(curr_state):
                return curr_path
            for successor in problem.getSuccessors(curr_state):
                next_state, action = successor[0], successor[1]
                if next_state not in explored:
                    next_node = (next_state, curr_path+[action])
                    frontier.update(next_node, problem.getCostOfActions(curr_path+[action]) + heuristic(next_state, problem))
    return [] #curr_path
    util.raiseNotDefined()

    """
    Question 4: What happens on openMaze for the various search strategies?
    Answer: For DFS strategy, it explored all possible paths to the maximum 
    depth but cannot guarantee optimal. BFS is better than DFS. A* use Manhatten
    heuristic so that perform better than UCS.
    """

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
