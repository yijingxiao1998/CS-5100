# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        # first we need to build iteration so that we could update during this iteration
        for i in range(self.iterations):
            # in each iteration, we need to calculate state value for current policy
            states = self.mdp.getStates()  # Return a list of all states in the MDP
            new = util.Counter()  # a dictionary with a default value of zero
            maxV = 0
            
            for state in states:
                # if current state is terminal then qValue = 0
                # otherwise, iterate all possible state and calculate qValue, save the max value as current value
                if not self.mdp.isTerminal(state):
                    maxV = -float('inf')
                    # check all possible actions in current state, and calculate Q value
                    for action in self.mdp.getPossibleActions(state):
                        qValue = self.computeQValueFromValues(state, action)  # the function returns the Q-value of the (state, action) pair
                        if qValue > maxV:  # get the max value
                            maxV = qValue
                # update qValue for next iteration
                new[state] = maxV
            self.values = new


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        qValue = 0
        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            # q(s, a) = q(s, a) + prob * [reward + discount * max_q(s', a')]
            qValue += prob * (self.mdp.getReward(state, action, nextState) + self.discount * self.getValue(nextState))
        return qValue
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # computes the best action according to the value function
        maxV, bestAction = -float('inf'), None
        for action in self.mdp.getPossibleActions(state):
            qValue = self.computeQValueFromValues(state, action)  # the function returns the Q-value of the (state, action) pair
            if qValue > maxV:  # get the max value
                maxV = qValue
                bestAction = action
        return bestAction
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()  # Return a list of all states in the MDP
        # first we need to build iteration so that we could update during this iteration
        for i in range(self.iterations):
            # get a state from states
            state = states[i % len(states)]  # make sure the index would not out of the range
            # then,same step with valueIteration
            maxV = 0
            # if the state picked for updating is terminal, nothing happens in that iteration
            # otherwise, iterate all possible state and calculate qValue, save the max value as current value
            if not self.mdp.isTerminal(state):
                maxV = -float('inf')
                # check all possible actions in current state, and calculate Q value
                for action in self.mdp.getPossibleActions(state):
                    qValue = self.computeQValueFromValues(state, action)  # the function returns the Q-value of the (state, action) pair
                    if qValue > maxV:  # get the max value
                        maxV = qValue
                # update only one state in each iteration
                self.values[state] = maxV

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        "Plus note:" # Even though we could skip question 5(PRIORITIZED SWEEPING), it's good for me to have a try just following the instruction
        # compute predecessors of all states, store them in a set to avoid duplicates
        predecessors = dict()
        for state in self.mdp.getStates():
            predecessors[state] = set()
        # initialize an empty priority queue
        priority_queue = util.PriorityQueue()
        # iterate over states in the order returned 
        for state in self.mdp.getStates():
            # rerminal state doesn't have predecessor, so for each non-terminal state s, do:
            if not self.mdp.isTerminal(state):
                # iterate every possible action and find the predecessor of state that have a nonzero probability of reaching state by taking some action
                for action in self.mdp.getPossibleActions(state):
                    for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                        predecessors[nextState].add(state)
        # iterate over non-terminal states
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                # find the absolute value of the difference between the current value of state in self.values and the highest Q-value across all possible actions from state
                qMax = max([self.getQValue(state, action) for action in self.mdp.getPossibleActions(state)])  # calculate highest Q-value
                # save the absolute value of the different to variable diff
                diff = abs(qMax - self.values[state])
                # push state into the priority queue with priority -diff, we use a negative because the priority queue is a min heap, but we want to prioritize updating states that have a higher error.
                priority_queue.update(state, -diff)
        # iterate in 0, 1, ..., self.iterations-1 over non-terminal states
        for i in range(self.iterations):
            # If the priority queue is empty, then terminate
            if priority_queue.isEmpty(): 
                break
            # pop a state s off the priority queue
            state = priority_queue.pop()
            if not self.mdp.isTerminal(state):
                self.values[state] = max([self.getQValue(state, action) for action in self.mdp.getPossibleActions(state)])
                # For each predecessor p of s, do:
                for pred in predecessors[state]:
                    # find the absolute value of the difference between the current value of p in self.values and the highest Q-value across all possible actions from p
                    qMax = max([self.getQValue(pred, action) for action in self.mdp.getPossibleActions(pred)]) # calculate highest Q-value
                    # save the absolute value of the different to variable diff
                    diff = abs(qMax - self.values[pred])
                    # if diff > theta, push p into the priority queue with priority -diff,  as long as it does not already exist in the priority queue with equal or lower priority
                    if diff > self.theta:
                        # as before, we use a negative because the priority queue is a min heap, but we want to prioritize updating states that have a higher error
                        priority_queue.update(pred, -diff)

