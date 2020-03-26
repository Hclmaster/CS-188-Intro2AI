def getStartState():
    """
    Returns the start state (in your state space, not the full Pacman state
    space)
    """
    "*** YOUR CODE HERE ***"
    # print("startingPosition: ", self.startingPosition)
    # util.raiseNotDefined()
    return (2, 2), False, False, False, False

print(getStartState())