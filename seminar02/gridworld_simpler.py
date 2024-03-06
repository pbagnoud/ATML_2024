


# A list of possible moves
MOVES = [
    (-1, 0), # Up
    (0, 1),  # Right
    (1, 0),  # Down
    (0, -1)  # Left
]

class GridWorld:
    def __init__(self, height = 5, width = 5, rewardDict = dict(), invalidActionReward = 0):
        # Store given dimensions and rewards in attributes
        self.height = height
        self.width = width
        self.rewardDict = rewardDict
        self.invalidActionReward = invalidActionReward

        # Set the initial position to (0, 0)
        self.pos = (0, 0)

    def step(self, action):
        """
        Perform an action.
        The argument `action` must be an integer (0, 1, 2, or 3),
        indicating one of the moves from `MOVES`.
        """
        
        # Get the move (tuple) corresponding to the given action (integer)
        move = MOVES[action]
        
        # Compute the new position
        newPos = (self.pos[0] + move[0], self.pos[1] + move[1])
        
        # Check if the new position is out of bounds
        if newPos[0] < 0 or newPos[0] >= self.height or newPos[1] < 0 or newPos[1] >= self.width:
            # If so, don't move, and return the invalid action reward
            return self.pos, self.invalidActionReward
        
        # Loop up the reward for landing here
        reward = self.rewardDict.get(newPos, 0)
        
        # Update the state of the world
        self.pos = newPos

        # Return the new position and the reward
        return newPos, reward
    
    def reset(self):
        self.pos = (0, 0)
        return self.pos
    
    def drawWorld(self):
        # Loop over all rows/columns
        for i in range(self.height):
            for j in range(self.width):
                # Print an "X" if we're at the current position
                # Otherwise, print a "."
                if (i, j) == self.pos:
                    print("X", end=" ")
                else:
                    print(".", end=" ")
            # Print a newline at the end of each row
            print()
    
    def play(self):
        print('Enter an integer to make a move (0, 1, 2, or 3).')
        print('Enter anything else to quit.\n')
        self.drawWorld()
        while True:
            x = input('> ')
            try:
                action = int(x)
            except:
                break
            (newPos, reward) = self.step(action)
            print('New position:', newPos)
            print('Reward:', reward, '\n')
            self.drawWorld()



if __name__ == '__main__':
    # Create a dictionary of rewards
    rewardDict = {
        (0, 3): 10,
        (1, 3): -10,
    }
    
    # Initialize the world
    gw = GridWorld(6, 7, rewardDict, -2)
    
    # Draw the world
    gw.drawWorld()
    
    # Take some steps
    print('\nMaking some moves...\n')
    gw.step(1)
    gw.step(1)
    gw.step(1)
    gw.step(2)
    gw.step(2)
    
    # Draw the world again
    gw.drawWorld()

    # Interactively play in the world
    gw.play()


