

import random

# The five available actions
ACTION_ROLL_1 = 'roll'
ACTION_ROLL_2 = 'rollTwo'
ACTION_BET_1 = 'betOne'
ACTION_BET_2 = 'betTwo'
ACTION_BET_3 = 'betThree'

ACTIONS = [
    ACTION_ROLL_1,
    ACTION_ROLL_2,
    ACTION_BET_1,
    ACTION_BET_2,
    ACTION_BET_3
]

# Names to be used in plots etc.
ACTION_NAMES = [
    'Roll 1',
    'Roll 2',
    'Bet 1',
    'Bet 2',
    'Bet 3'
]


class DiceGame:
    # All dice are weighted: highest number has double probability!
    # Min and max eyes on the dealer dice
    MAX_EYES_DEALER = 30
    MIN_EYES_DEALER = 25
    
    # Min and max eyes on the player dice
    MIN_EYES_PLAYER = 1
    MAX_EYES_PLAYER = 6
    
    # Rewards for rolling, rolling doubles, and going bust
    REWARD_DOUBLE = 10
    REWARD_ROLL = -1
    REWARD_BUST = -10
    
    # Terminal state
    TERMINAL = MAX_EYES_DEALER + 1
    
    # List of states
    STATES = range(MAX_EYES_DEALER + 2)
    
    def __init__(self, verbose = False):
        self.state = 0

        # The verbose toggle is used to print output in interactive mode, but not during MC
        self.verbose = verbose
    
    def reset(self, state0 = 0):
        self.state = state0
        return self.state
        
    def _log(self, *args, sep = ' ', end = '\n'):
        if self.verbose:
            print(*args, sep = sep, end = end)
        
    def _rollPlayerDice(self):
        # We sample the highest number with double probability
        # by sampling up to self.MAX_EYES_PLAYER+1 (inclusive!)
        # and capping the result at self.MAX_EYES_PLAYER.
        # A more flexible approach could be to use random.choices with weights.
        dice = random.randint(self.MIN_EYES_PLAYER, self.MAX_EYES_PLAYER + 1)
        dice = min(dice, self.MAX_EYES_PLAYER)
        return dice
    
    def _rollDealerDice(self):
        dice = random.randint(self.MIN_EYES_DEALER, self.MAX_EYES_DEALER + 1)
        dice = min(dice, self.MAX_EYES_DEALER)
        return dice

    def _stepRoll(self, rollTwo = False):
        # sub-method to handle a step with a roll action
        reward = 0
        
        # roll the first dice
        dice = self._rollPlayerDice()
        reward += self.REWARD_ROLL
        self._log(f'Dice: {dice}')
        self.state += dice

        # (maybe) roll the second dice
        if rollTwo:
            dice2 = self._rollPlayerDice()
            reward += self.REWARD_ROLL
            self._log(f'Dice 2: {dice2}')
            self.state += dice2
            if dice == dice2:
                reward += self.REWARD_DOUBLE

        # handle the bust case
        if self.state >= self.TERMINAL:
            self.state = self.TERMINAL
            reward += self.REWARD_BUST
        
        # return reward and new state
        self._log(f'Reward: {reward} --- State: {self.state}')
        return reward, self.state
    
    def _stepBet(self, amount):
        # sub-method to handle a step with a bet action
        dealerEyes = self._rollDealerDice()
        self._log(f'Dealer eyes {dealerEyes}')
        reward = (self.state - dealerEyes) * amount
        self.state = self.TERMINAL
        self._log(f'Reward: {reward} --- State: {self.state}')
        return reward, self.state
    
    def step(self, action):
        self._log(f'Action: {action}')
        # Check that the action is valid and call the corresponding sub-method
        if self.state == self.TERMINAL:
            # Here we could also return the terminal state and a reward of 0
            raise Exception('Game is in terminal state. Call .reset() to play again.')
        if action == ACTION_ROLL_1:
            return self._stepRoll(False)
        if action == ACTION_ROLL_2:
            return self._stepRoll(True)
        if action == ACTION_BET_1:
            return self._stepBet(1)
        if action == ACTION_BET_2:
            return self._stepBet(2)
        if action == ACTION_BET_3:
            return self._stepBet(3)
        raise ValueError('Invalid action:', action)
    
    def play(self):
        # Optional method to play the game interactively

        # Force self.verbose to print output
        oldVerbosity = self.verbose
        self.verbose = True
        
        # Keep track of the reward
        totalReward = 0
        
        # Print instructions
        print(f'\nEnter "{ACTION_ROLL_1}" to roll once, "{ACTION_ROLL_2}" to roll twice.')
        print(f'Enter "{ACTION_BET_1}", "{ACTION_BET_2}", or "{ACTION_BET_3}" to bet.')
        print('Anything else to quite.')
        print('You start with a count of 0.')
        
        # Play
        while self.state != self.TERMINAL:
            action = input('> ')
            if not action in ACTIONS:
                print('Unknown action -> quitting...')
                break
            reward, state = self.step(action)
            totalReward += reward
        
        print(f'Total rewards: {totalReward}')
        print(f'Final state: {self.state}')
        
        # Restore previous verbosity
        self.verbose = oldVerbosity

# If the module is sourced directly, we test the class by playing a game
if __name__ == '__main__':
    dj = DiceGame()
    dj.play()



