import argparse
import random
from action import *
from solver import *


def initBoard(n):
    randomlist = random.sample(range(0, n), n)
    return tuple(randomlist)
def solvable(initialBoard):
    #do something here

    inBoard = list(initialBoard)
    inversions = 0
    # print(len(inBoard))
    for i in range(0,len(inBoard)):
        # print(inBoard[i])
        if inBoard[i]== 0:
            continue
        for j in range(i+1,len(inBoard)):
            # print(inBoard[j])
            if inBoard[j]==0:
                continue
            if (inBoard[i]>inBoard[j]):
                inversions +=1
    print(inversions)
    if inversions%2 == 1:
        return False
    else:
        return True
    
def run():
    parser = argparse.ArgumentParser(description = "n-Puzzle Game Search")
    # parser.add_argument('input_board', nargs='+', type=lambda x:x.split(','))
    #This line below just use for input the initial board for you to test in a specific input you want
    parser.add_argument('n', type=int)
    args = parser.parse_args()
    
    # print(args.n)
    # " args.input_board reads into a list of list, reformat to tuple"
    # board = args.input_board
    # board = tuple([int(i) for i in board[0]])
    if (args.n not in [2,3,4,5]):
        print('The number n is illegal, can not initial board and solve. It should be 2,3,4,5')
        return None
    n = args.n
    # you just need to input n, which is n*n matrix board. The function will auto init the initial state for you.
    board = initBoard(n*n)
    game = NPuzzle(board)

    print('\n* * * * * * * * * * * * * * * *\nInitial nPuzzle Board:\n', game)

    #Implement a solvable function in solver.py to check that the initial puzzle board input is solvable or not
    #because it turns out that there many cases of puzzle board that unsolvable.
    solvableInit = solvable(board) 
    if not solvableInit:
        print ('This puzzle board unsolvable')
        return None
    solution = Solver(game)
    
    running_time = time.time()
    # if args.method == ['bfs']:
    #     solution.bfs()

    solution.dfs()

    running_time = time.time() - running_time

    # " On screen print out solutions "
    print('\n - - solution - - \n')                            
    print('path_to_goal', solution.path_to_goal)    
    print('cost_of_path', solution.cost_of_path)
    print('nodes_expended:', solution.nodes_expanded)
    print('fringe_size:', solution.fringe_size)
    print('max_fringe_size:', solution.max_fringe_size)
    print('search_depth', solution.search_depth)
    print('max_search_depth', solution.max_search_depth)
    print('running_time:', running_time)

        
    
if __name__ == '__main__':
    run()