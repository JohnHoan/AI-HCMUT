import random
import time
import copy

def getAllPossibleMoves(board, player):
    board = board.copy()
    moves = list()
    for i in range(25):
        if board[i] == player:
            lst = list()
            if i%2 == 0:
                lst = [i-6, i-5, i-4, i-1, i+1, i+4, i+5, i+6]
            else:
                lst = [i-5, i-1, i+1, i+5]
            for x in lst:
                if moveCondition(board, i, x):
                    moves.append((i, x))
    return moves

def getAvailableMoves(board, player, preBoard):
    availableMove = list()
    listBayAvailable = list()
    isBay = False
    for i in range(25):
        if board[i] == player:
            lst = list()
            if i%2 == 0:
                lst = [i-6, i-5, i-4, i-1, i+1, i+4, i+5, i+6]
            else:
                lst = [i-5, i-1, i+1, i+5]
            bay1 = False
            for x in lst:
                if moveCondition(board,i, x):
                    # Bay
                    lst1 = list()
                    if x % 2 == 0:
                        lst1 = [(x - 6, x + 6), (x - 5, x + 5), (x - 4, x + 4), (x - 1, x + 1)]
                    else:
                        lst1 = [(x - 5, x + 5), (x - 1, x + 1)]
                    for x1 in lst1:
                        if x1[0] >= 0 and x1[0] <= 24 and x1[0] % 5 - x % 5 in [-1, 0, 1] and x1[1] >= 0 and x1[1] <= 24 and x1[1] % 5 - x % 5 in [-1, 0, 1]:
                            if not board[x1[0]] in [board[i], 0] and not board[x1[1]] in [board[i], 0]:
                                if preBoard[x1[0]] in [preBoard[i], 0]:
                                    bay1 = True
                                    listBayAvailable.append((i, x))
                                    break
                                elif preBoard[x1[1]] in [preBoard[i], 0]:
                                    bay1 = True
                                    listBayAvailable.append((i, x))
                                    break
                                elif preBoard[x] != 0:
                                    bay1 = True
                                    listBayAvailable.append((i, x))
                                    break
                    # them i, x vao danh sach nhung nuoc co the di
                    availableMove.append((i, x))
            if bay1 is True:
                isBay = True
    if isBay:
        return listBayAvailable
    return availableMove

def moveCondition(board, start, end):
    if end <= 0 or end >= 24 or not end % 5 - start % 5 in [-1, 0, 1]:
        return False
    if board[end] != 0:
        return False
    return True

def flatten(board):
    if board == []:
        return []
    return board[0] + flatten(board[1:])

def makeMove(board, move):
    boardNew = board.copy()
    if boardNew[move[0]] == 0:
        return None
    if boardNew[move[1]] != 0:
        return None

    boardNew[move[1]] = boardNew[move[0]]
    boardNew[move[0]] = 0
    # ganh
    lst = list()
    if move[1] % 2 == 0:
        lst = [(move[1] - 6, move[1] + 6), (move[1] - 5, move[1] + 5), (move[1] - 4, move[1] + 4), (move[1] - 1, move[1] + 1)]
    else:
        lst = [(move[1] - 5, move[1] + 5), (move[1] - 1, move[1] + 1)]
    for x in lst:
        if x[0] >= 0 and x[0] <= 24 and x[0] % 5 - move[1] % 5 in [-1, 0, 1] and x[1] >= 0 and x[1] <= 24 and x[1] % 5 - move[1] % 5 in [-1, 0, 1]:
            if not boardNew[x[0]] in [boardNew[move[1]], 0] and not boardNew[x[1]] in [boardNew[move[1]], 0]:
                boardNew[x[0]] = boardNew[move[1]]
                boardNew[x[1]] = boardNew[move[1]]

    # vay
    opp = -boardNew[move[1]]
    alain = list()
    
    for i in range(25):
            if boardNew[i]==opp:
                opptrans = list()
                visited = [False]*25
                opptrans.append(i)
                visited[i] = True
                way = 0
                if i % 2 == 0:
                    lst = [i - 6, i - 5, i - 4, i - 1, i + 1, i + 4, i + 5, i + 6]
                else:
                    lst = [i - 5, i - 1, i + 1, i + 5]
                for x in lst:
                    if x <= 0 or x >= 24 or not x % 5 - i % 5 in [-1, 0, 1]:
                        continue
                    if boardNew[x] == 0:
                        way = way + 1
                    if boardNew[x] == opp and visited[x] == False:
                        alain.append(x)
                        visited[x]=True
                if way != 0:
                    continue
                else:
                    vay = True
                    while alain:
                        u = alain.pop()
                        opptrans.append(u)
                        way = 0
                        if u % 2 == 0:
                            lst = [u - 6, u - 5, u - 4, u - 1, u + 1, u + 4, u + 5, u + 6]
                        else:
                            lst = [u - 5, u - 1, u + 1, u + 5]
                        for x in lst:
                            if x <= 0 or x >= 24 or not x % 5 - u % 5 in [-1, 0, 1]:
                                continue
                            if boardNew[x] == 0:
                                way = way + 1
                            if boardNew[x] == opp and visited[x] == False:
                                alain.append(x)
                                visited[x] = True
                        if way != 0:
                            vay = False
                            break
                        else:
                            vay = True
                    if vay:
                        for x in opptrans:
                            boardNew[x]=boardNew[move[1]]

    return boardNew

def alpha_beta_search(board, player):
    timeStart = time.time()
    best_value = -1000
    beta = 1000
    moves = getAllPossibleMoves(board, player)
    if len(moves) == 0:
        return None
    if len(moves) == 1:
        return moves[0]
    best_move = list()
    depth = 6
    for i in range(len(moves)):
        # print(moves[i])
        new_board = makeMove(board, moves[i])
        value = min_value(new_board, -player, best_value, beta , moves[i], depth - 1, board, timeStart)
        if value >= best_value:
            best_value = value
            best_move.append((moves[i], best_value))
        if timeOut(timeStart):
            break
    lst = list()
    # print(best_move)
    for x in best_move:
        if x[1] == best_value:
            lst.append(x[0])
    if len(lst) == 1:
        return lst[0]
    else:
        return lst[random.randint(0, len(lst) - 1)]

def min_value(board, player, alpha, beta, moves, depth, preBoard, timeStart):
    if depth == 0 or timeOut(timeStart):
        return staticEval(board,-player)
    value = 1000
    moves = getAvailableMoves(board, player, preBoard)
    for i in range(len(moves)):
        new_board = makeMove(board, moves[i])
        value = min(value, max_value(new_board, -player, alpha, beta , moves[i], depth - 1, board, timeStart))
        if value <= alpha:
            return value
        beta = min(beta, value)
        if timeOut(timeStart):
            break
    return value

def max_value(board, player, alpha, beta, moves, depth, preBoard, timeStart):
    if depth == 0 or timeOut(timeStart):
        return staticEval(board, -player)
    value = -1000
    moves = getAvailableMoves(board, player, preBoard)
    for i in range(len(moves)):
        new_board = makeMove(board, moves[i])
        value = max(value, min_value(new_board, -player, alpha, beta , moves[i], depth - 1, board, timeStart))
        if value >= beta:
            return value
        beta = max(beta, value)
        if timeOut(timeStart):
            break
    return value

def timeOut(timeStart):
    if time.time() - timeStart >= 1.5:
        return True
    return False

def staticEval(board, player):
    num1 = 0
    num2 = 0
    for i in range(25):
        if board[i]==-1:
            num1 +=1
        elif board[i]==1:
            num2 +=1 
    if player == -1:
        if num1 == 0:
            return -1000
        if num2 == 0:
            return 1000
        return num1 - num2
    elif player == 1:
        if num1 == 0:
            return 1000
        if num2 == 0:
            return -1000
        return num2 - num1
    else:
        return None

# greedy algorithm
def findGoodMove(board, moves, player):
    bestScore = -1000
    bestMove = None
    for move in moves:
        boardNew = makeMove(board, move)
        score = scoreBoard(boardNew)
        if score > bestScore:
            bestScore = score
            bestMove = move 
    return bestMove

def move(board, player, remain_time):
    # startTime = time.time()
    board = flatten(board)
    if remain_time <= 10:
        moves = getAllPossibleMoves(board, player)
        if len(moves) == 0:
            return None
        bestMove = findGoodMove(board, moves, player)         
        if bestMove == None and len(moves)!=0:
            rand = random.randint(0, len(moves)-1)
            bestMove = moves[rand]
            result = ((int(bestMove[0]/5), bestMove[0] % 5), (int(bestMove[1]/5), bestMove[1]%5))
        else:
            result = ((int(bestMove[0]/5), bestMove[0] % 5), (int(bestMove[1]/5), bestMove[1]%5))
        return result  
    else:
        bestMove = alpha_beta_search(board, player)
        if bestMove == None and len(moves)!=0:
            rand = random.randint(0, len(moves)-1)
            bestMove = moves[rand]
            result = ((int(bestMove[0]/5), bestMove[0] % 5), (int(bestMove[1]/5), bestMove[1]%5))
        else:
            result = ((int(bestMove[0]/5), bestMove[0] % 5), (int(bestMove[1]/5), bestMove[1]%5))
        # endTime = time.time()
        # print('Time running: ',endTime-startTime)
        return result


# board = [[-1,0,1,0,1],
# [1,-1,0,-1,0],
# [1,-1,0,0,0],
# [1,-1,-1,-1,0],
# [1,1,1,0,-1]]

# print(move(board,1, 90))

# preBoard = flatten([[0,0,1,0,1],
# [-1,-1,0,0,1],
# [-1,-1,1,0,0],
# [-1,-1,1,1,1],
# [-1,1,0,0,1]])

# board = flatten([[0,0,1,0,1],
# [-1,-1,0,0,1],
# [-1,-1,1,0,0],
# [-1,-1,0,1,1],
# [-1,1,1,0,1]])

# print(getAvailableMoves(board,1, preBoard))
