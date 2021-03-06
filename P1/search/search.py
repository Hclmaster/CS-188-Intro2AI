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
    return [s, s, w, s, w, w, s, w]


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

    stack = util.Stack()
    prev_stacks = util.Stack()
    closed_set = set()
    closed_set.add(problem.getStartState())

    for successor in problem.getSuccessors(problem.getStartState()):
        stack.push(successor)
        prev_stacks.push(successor)

    actions = []

    while not stack.isEmpty():
        state = stack.pop()
        prev_top = prev_stacks.pop()
        if prev_top[0] == state[0]:
            prev_stacks.push(prev_top)
        else:
            while prev_top[0] != state[0]:
                prev_top = prev_stacks.pop()
                actions.pop()
            prev_stacks.push(state[0])

        # if not visited before, then visit, otherwise continue
        if state[0] in closed_set:
            continue
        if state[0] not in closed_set:
            actions.append(state[1])
            closed_set.add(state[0])
        if problem.isGoalState(state[0]):
            break

        successors = problem.getSuccessors(state[0])
        flag = False
        for successor in successors:
            if successor[0] in closed_set:
                continue
            stack.push(successor)
            prev_stacks.push(successor)
            flag = True
        if not flag:
            actions.pop()
            prev_stacks.pop()

    return actions


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    closed_set = set()
    closed_set.add(problem.getStartState())
    prev_nodes = {problem.getStartState(): None}

    # be careful about the definition of closed set here
    # it should judge whether this node is current inside queue or not
    # not judge whether this node is expanded or not
    # because the way bfs works - is start from shallow and then deeper
    # so if this node is being visited in shallow before, then we no need
    # to expand this node, thus we can mark it already being inside queue.
    for successor in problem.getSuccessors(problem.getStartState()):
        queue.push(successor)
        prev_nodes[successor[0]] = problem.getStartState()
        closed_set.add(successor[0])

    goal_node = None
    actions = []

    while not queue.isEmpty():
        state = queue.pop()

        if problem.isGoalState(state[0]):
            goal_node = state[0]
            actions.append(state[1])
            break

        for successor in problem.getSuccessors(state[0]):
            if successor[0] not in closed_set:
                prev_nodes[successor[0]] = state
                queue.push(successor)
                closed_set.add(successor[0])

    while goal_node:
        if goal_node not in prev_nodes:
            print("******This state doesn't store in dictionary!******")
            break
        state = prev_nodes[goal_node]
        if type(problem.getStartState()) == type(state) and state == problem.getStartState():
            break
        if state is not None:
            actions.append(state[1])
            goal_node = state[0]
        else:
            goal_node = state

    actions.reverse()
    return actions


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    pq = util.PriorityQueue()
    closed_set = set()
    closed_set.add(problem.getStartState())

    for successor in problem.getSuccessors(problem.getStartState()):
        item = [successor, [successor[1]]]
        pq.push(item, problem.getCostOfActions(item[1]))

    actions = None
    while not pq.isEmpty():
        pq_item = pq.pop()
        state = pq_item[0]
        actions = pq_item[1]

        if problem.isGoalState(state[0]):
            break
        if state[0] in closed_set:      # if we already expanded this node, then continue (don't forget!!!)
            continue
        if state[0] not in closed_set:
            closed_set.add(state[0])

        for successor in problem.getSuccessors(state[0]):
            if successor[0] in closed_set:
                continue
            item = [successor, actions + [successor[1]]]
            pq.push(item, problem.getCostOfActions(item[1]))

    return actions


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    """
    Questions:
    1. why this heuristic is admissible and ensure consistency?
    2. how to define our own heuristic function?
    """
    pq = util.PriorityQueue()
    closed_set = set()
    closed_set.add(problem.getStartState())

    for successor in problem.getSuccessors(problem.getStartState()):
        item = [successor, [successor[1]]]
        pq.push(item, problem.getCostOfActions(item[1]) + heuristic(successor[0], problem))

    actions = None
    while not pq.isEmpty():
        pq_item = pq.pop()
        state = pq_item[0]
        actions = pq_item[1]

        if problem.isGoalState(state[0]):
            break
        if state[0] in closed_set:
            continue
        if state[0] not in closed_set:
            closed_set.add(state[0])

        for successor in problem.getSuccessors(state[0]):
            if successor[0] in closed_set:
                continue
            item = [successor, actions + [successor[1]]]
            pq.push(item, problem.getCostOfActions(item[1]) + heuristic(successor[0], problem))

    return actions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
