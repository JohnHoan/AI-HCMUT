from run import *
from action import *

class Solver:

    def __init__(self, initialBoard):
        self.nPuzzleState = NPuzzleState(initialBoard)
        self.path_to_goal = []
        self.cost_of_path = 0
        self.nodes_expanded = 0
        self.fringe_size = 0
        self.max_fringe_size = 0
        self.search_depth = 0
        self.max_search_depth = 0
        self.goal = tuple(range(0,len(initialBoard.board)))
        print('The goal state: ' + str(self.goal))

    def __success(self, node):
        self.cost_of_path = node.path_cost
        self.search_depth = node.depth
        # " work backwards from answer node to get the path solution " 
        while node.parent is not None:
            self.path_to_goal.insert(0, node.action)
            node = node.parent       
        return None
        
    def __failure(self):
        print('Cannot find solution')
        return None

    
    def dfs(self):
        """ using deque() as LIFO stack, right side in/out"""
        frontier = deque()
        frontier.append(self.nPuzzleState)
        self.fringe_size += 1
        """ using a set() to track both frontier and explored nodes"""
        frontier_U_explored = set()
        frontier_U_explored.add(self.nPuzzleState)
        
        while frontier:
            node = frontier.pop()
            self.fringe_size -= 1
            
            if node.state.goal_test(node.state, self.goal):
                return self.__success(node)
            self.nodes_expanded += 1            
            
            for neighbor in node.reverse_neighbors():
                if neighbor not in frontier_U_explored:
                    """ enqueue in *reverse* UDLR order, the order of how 
                    actions are checked at Class NPuzzle. """
                    #reverse_frontier.appendleft(neighbor)
                    frontier.append(neighbor)
                    frontier_U_explored.add(neighbor)
                    self.fringe_size += 1
                    if neighbor.depth > self.max_search_depth:
                        self.max_search_depth = neighbor.depth
                        
            if self.fringe_size > self.max_fringe_size:
                self.max_fringe_size = self.fringe_size
                
        return self.__failure   
    