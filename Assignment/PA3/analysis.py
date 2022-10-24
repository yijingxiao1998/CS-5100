# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    answerDiscount = 0.9
    answerNoise = 0
    return answerDiscount, answerNoise

def question3a():
    # 1. Prefer the close exit (+1), risking the cliff (-10)
    answerDiscount = 0.1      # lower value means big reward has lower attractive to current state
    answerNoise = 0           # some probability for other actions
    answerLivingReward = 0    # lower value agent more likely take adventure
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    # 2. Prefer the close exit (+1), but avoiding the cliff (-10)
    answerDiscount = 0.1      # lower value means big reward has lower attractive to current state
    answerNoise = 0.1         # the probability of falling cliff is increased, so agent will try to avoid the cliff
    answerLivingReward = 0.1  # lower value agent more likely take adventure
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    # 3. Prefer the distant exit (+10), risking the cliff (-10)
    answerDiscount = 0.9      # right side reward is attractive, so agent would like following the cliff
    answerNoise = 0.002       # some probability for other actions
    answerLivingReward = 0    # lower value agent more likely take adventure
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    # 4. Prefer the distant exit (+10), avoiding the cliff (-10)
    answerDiscount = 0.9      # right side reward is attractive, so agent would like following the cliff
    answerNoise = 0.1         # the probability of falling cliff is increased, so agent will try to avoid the cliff
    answerLivingReward = 0.1  # lower value agent more likely take adventure
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    # 5. Avoid both exits and the cliff (so an episode should never terminate)
    answerDiscount = 0        # big reward doesn't attractive any more
    answerNoise = 0.1         # the probability of falling cliff is increased, so agent will try to avoid the cliff
    answerLivingReward = 0.9  # living reward is big so that agent too fear to go
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question8():
    answerEpsilon = 0
    answerLearningRate = 0.1
    return 'NOT POSSIBLE'
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
