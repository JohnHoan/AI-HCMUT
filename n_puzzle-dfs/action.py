
import time
import sys
from math import sqrt
from collections import deque
from heapq import heappush, heappop, heapify



""" setting keys for a* heuristic comparisons """
action_dict = {'Up':1, 'Down':2, 'Left':3, 'Right':4}
    
class NPuzzle(object):
    
    """ Low-level physical configuration of N-Puzzle tiles. Board represented
    using tuple so its hashable."""
    
    def __init__(self, board):
        self.board = board
        
    def actions(self, state):
        """ Actions available in the current puzzle. Find the position of 
        zero first, and check if zero can be moved in up, down, left, right 
        directions. N-puzzle has edge and does not wrap around board. Returns 
        a list of available actions."""
        size = int(sqrt(len(state.board)))
        x = self.board.index(0)
        action_list = []
        
        if x > size-1:
            action_list.append('Up')
        if x < len(self.board)-size:
            action_list.append('Down')
        if x % size != 0:
            action_list.append('Left')
        if x % size != size-1:
            action_list.append('Right')
        return action_list
    
    def reverse_action(self,state):
        """ adding actions in reverse order. Used for depth first search as 
        speficied by project """
        size = int(sqrt(len(state.board)))
        x = self.board.index(0)
        action_list = []
        
        if x % size != size-1:
            action_list.append('Right')
        if x % size != 0:
            action_list.append('Left')
        if x < len(self.board)-size:
            action_list.append('Down')
        if x > size-1:
            action_list.append('Up')
        return action_list
    
    def result(self, state, action):
        """ Returns the NPuzzle board that result from executing the given
        given action on the given NPuzzle board. Have to change to list()
        because tuple() is immutable """
        size = int(sqrt(len(state.board)))
        new = list(state.board)
        x = state.board.index(0)
        if (action == 'Up'):
            new[x], new[x-size] = new[x-size], new[x]
            return NPuzzle(tuple(new))
        if (action == 'Down'):
            new[x], new[x+size] = new[x+size], new[x]
            return NPuzzle(tuple(new))
        if (action == 'Left'):
            new[x], new[x-1] = new[x-1], new[x]
            return NPuzzle(tuple(new))
        if (action == 'Right'):
            new[x], new[x+1] = new[x+1], new[x]
            return NPuzzle(tuple(new))

    def goal_test(self, state, goal):
        return state.board == goal
      
    def path_cost(self, c, state1, action, state2):
        return c + 1
    
    def __repr__(self):
        return str(self.board)
    
    def __eq__(self, other):
        return self.board == other.board and isinstance(other, NPuzzle)
    

class NPuzzleState(object):
    
    """ NPuzzleState represents a node in the NPuzzle game search tree. It
    contains an NPuzzle object, parent of the node, action taken to get to the
    node, and path_cost and search depth of the node. Hash value is based on
    the board within the NPuzzle object only to prevent adding duplicates nodes
    with different parents/actions during search."""
 
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1
        """ design decision to calculate manhattan distance heuristics at the 
        time of object creation to reduce repeated calculation for A* and 
        iterative depth A*. It slows down BFS/DFS by a few seconds but saves
        a lot of time for AST and IDA. 
        I copy this function from the Internet and modify to fit with the code and I see it works quite good even I'm not 
        really understand it. I will try harder. """
        self.f = self.path_cost + self.manhattan()
    
    def neighbors(self):
        # "List the nodes reachable in one step from this node in UDLR order."
        x = []
        for action in self.state.actions(self.state):
            x.append(NPuzzleState(self.state.result(self.state, action), 
                                  self, 
                                  action, 
                                  self.state.path_cost(self.path_cost, 
                                                       self.state,
                                                       action, 
                                                       next)))
        return x
    
    def reverse_neighbors(self):
        # "List the nodes reachable in one step from this node, in reverse UDLR"
        x = []
        for action in self.state.reverse_action(self.state):
            x.append(NPuzzleState(self.state.result(self.state, action), 
                                  self, 
                                  action, 
                                  self.state.path_cost(self.path_cost, 
                                                       self.state,
                                                       action, 
                                                       next)))
        return x
    
    def manhattan(self):
        # " Calculate the manhattan distance of the board, for heuristics "
        w = int(sqrt(len(self.state.board)))
        return sum((abs(i//w - self.state.board.index(i)//w) + 
                    abs(i%w - self.state.board.index(i)%w) 
                    for i in self.state.board if i != 0))
        
    def __eq__(self, other):
        return self.state.board == other.state.board and isinstance(other, NPuzzleState)

    def __hash__(self): 
        return hash(str(self.state.board))
        
    def __repr__(self):
        return str(self.state.board)
    
    def __lt__(self, other):
        """ For heapq comparisons. 1) compare f(n) = g(n) + h(n) with h(n) being
            the manhattan() distance, 2) compare directions in the order of
            UP, DOWN, LEFT, RIGHT. 3) To compensate for the same f(n) and same 
            action, I've choose to go wide in A* by choosing higher g(n)"""
        if self.f < other.f:
            return True
        elif self.f == other.f:
            if action_dict[self.action] < action_dict[other.action]:
                return True
            elif self.action == other.action:
                return self.depth > other.depth
            return False
        else:
            return False
        
              
