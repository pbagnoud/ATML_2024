

from diceGame import ACTIONS, ACTION_BET_1, ACTION_BET_2, ACTION_BET_3, ACTION_ROLL_1, ACTION_ROLL_2
from diceGame import DiceGame

import numpy as np

# Use this value for theta, if nothing else is specified
DEFAULT_THETA = 1e-15

# Policy evaluation (following the code from seminars/lectures/Sutton&Barto)
def evaluatePolicy(policy, theta = DEFAULT_THETA):
    values = [0] * len(DiceGame.STATES)
    while True:
        delta = 0
        for state in DiceGame.STATES:
            oldValue = values[state]
            actionProbabilities = policy[state]
            # This function computes the double sum over a, s', r
            values[state] = evaluateRandomAction(state, values, actionProbabilities)
            delta = max(delta, abs(values[state] - oldValue))
        
        if delta <= theta:
            break
    
    return values

# Helper function to evaluate the expected reward and next state value of a random action
def evaluateRandomAction(state, currentValues, probs):
    if len(probs) != len(ACTIONS):
        raise Exception('Policy must have same length as ACTIONS')
    
    # Loop over actions with their probabilities to compute expectation
    expectedValue = 0
    for a, p in zip(ACTIONS, probs):
        expectedValue += p * evaluateAction(state, currentValues, a)

    return expectedValue

def evaluateAction(state, currentValues, action):
    # Return zero if the state is terminal
    if state == DiceGame.TERMINAL:
        return 0
    
    # Call corresponding functions for roll and bet actions
    if action == ACTION_ROLL_1:
        return evaluateRollOneAction(state, currentValues)
    if action == ACTION_ROLL_2:
        return evaluateRollTwoAction(state, currentValues)
    if action == ACTION_BET_1:
        return evaluateBetAction(state, 1)
    if action == ACTION_BET_2:
        return evaluateBetAction(state, 2)
    if action == ACTION_BET_3:
        return evaluateBetAction(state, 3)
    
    raise ValueError('Invalid action:', action)

def getDiceFaces(minEyes, maxEyes):
    # Helper function to get the numbers and probabilities of a dice
    possibleEyes = range(minEyes, maxEyes + 1)
    nFaces = len(possibleEyes)
    prob = 1/(nFaces + 1)
    probabilities = [prob] * nFaces
    probabilities[-1] *= 2
    return possibleEyes, probabilities

def evaluateRollOneAction(state, currentValues):
    # Get numbers and probabilites on dice
    possiblePlayerEyes, probabilities = getDiceFaces(DiceGame.MIN_EYES_PLAYER, DiceGame.MAX_EYES_PLAYER)

    # Rolling one costs ... regardless of outcome
    expectedValue = DiceGame.REWARD_ROLL

    # Loop over the possible outcomes of the dice, computing their contributions to the expectation
    for eyes, probability in zip(possiblePlayerEyes, probabilities):
        newState = state + eyes
        if newState >= DiceGame.TERMINAL:
            # new state is terminal, reward is "bust", next state value is 0
            expectedValue += probability * DiceGame.REWARD_BUST
        else:
            # new state has a value, but there is no reward
            expectedValue += probability * currentValues[newState]
    return expectedValue


def evaluateRollTwoAction(state, currentValues):
    # Get numbers and probabilites on dice
    possiblePlayerEyes, probabilities = getDiceFaces(DiceGame.MIN_EYES_PLAYER, DiceGame.MAX_EYES_PLAYER)

    # Rolling twice costs 2x... regardless of outcome
    expectedValue = 2 * DiceGame.REWARD_ROLL
    
    # Loop over all possible outcomes of the two dice
    for eyes1, p1 in zip(possiblePlayerEyes, probabilities):
        for eyes2, p2 in zip(possiblePlayerEyes, probabilities):
            newState = state + eyes1 + eyes2
            if eyes1 == eyes2:
                # give reward for double, regardless of further game
                expectedValue += p1 * p2 * DiceGame.REWARD_DOUBLE

            if newState >= DiceGame.TERMINAL:
                # new state is terminal, reward is "bust"
                expectedValue += p1 * p2 * DiceGame.REWARD_BUST
            else:
                # new state is not terminal -> has value, no reward
                expectedValue += p1 * p2 * currentValues[newState]
    return expectedValue

def evaluateBetAction(state, amount):
    # Bet actions always end the game, so we only compute the expected reward
    # and do not need to have the argumet `currentValues`
    
    # Get numbers and probabilities on dealer dice
    possibleDealerEyes, probabilities = getDiceFaces(DiceGame.MIN_EYES_DEALER, DiceGame.MAX_EYES_DEALER)
    
    # Loop over possible outcomes, computing their contribution to the expectation
    expectedReward = 0
    for eyes, probability in zip(possibleDealerEyes, probabilities):
        reward = (state - eyes) * amount
        expectedReward += reward * probability
    return expectedReward


def chooseGreedyPolicy(values):
    # Helper function to compute a greedy policy w.r.t. a value function
    allActions = ACTIONS
    policy = []
    
    # Loop over state, computing the best action for each
    for state in DiceGame.STATES:
        # Evaluate all actoins
        actionValues = [evaluateAction(state, values, action) for action in allActions]

        # Assign probability 1 to the best action, 0 to others
        bestActionIndex = np.argmax(actionValues)
        actionProbabilities = [0 for a in allActions]
        actionProbabilities[bestActionIndex] = 1

        policy.append(actionProbabilities)

    return policy


# Helper function to convert the probability-representation of a policy to a simple list of action indices
def randomToDeterministicPolicy(randomPolicy):
    detPolicy = [np.argmax(probs) for probs in randomPolicy]
    return detPolicy

