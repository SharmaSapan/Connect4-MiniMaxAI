import numpy as np
import random
import math

TOTAL_ROWS = 6
TOTAL_COLUMNS = 7
PLAYER = 0
PLAYER2 = 1
AI = 1

def initializeBoard(): # numpy configs are in the assignment package
    board = np.zeros((TOTAL_ROWS, TOTAL_COLUMNS), int) # numpy is used only to initalize board
    return board


# to check if last row of given column is not full
def validPosition(board, col):
    return board[TOTAL_ROWS - 1][col] == 0


# give the next valid position for the turn in a column
def nextValidPosition(board, col):
    for r in range(TOTAL_ROWS):
        if board[r][col] == 0:
            return r


# function to initalize the turn
def nextTurn(board, row, col, value):
    board[row][col] = value


# print the current state of the board
def printState(board):
    a = []
    for r in reversed(range(TOTAL_ROWS)):
        for c in reversed(range(TOTAL_COLUMNS)):
            a.append(board[r][c])
        a.reverse()
        print(a)
        a.clear()


# to check the winning move acc to rules, it takes the value of player's move
def isWinningMove(board, value):
    # to check if horizontal connect 4 is complete
    for c in range(TOTAL_COLUMNS - 3):
        for r in range(TOTAL_ROWS):
            if board[r][c] == value and board[r][c + 1] == value and board[r][c + 2] == value and board[r][
                c + 3] == value:
                return True

    # to check if vertical connect 4 is complete
    for c in range(TOTAL_COLUMNS):
        for r in range(TOTAL_ROWS-3):
            if board[r][c] == value and board[r + 1][c] == value and board[r + 2][c] == value and board[r + 3][
                c] == value:
                return True

        # to check if downward diagonal connect 4 is complete
    for c in range(TOTAL_COLUMNS - 3):
        for r in range(3, TOTAL_ROWS):
            if board[r][c] == value and board[r - 1][c + 1] == value and board[r - 2][c + 2] == value and board[r - 3][
                c + 3] == value:
                return True

    # to check if upward diagonal connect 4 is complete
    for c in range(TOTAL_COLUMNS - 3):
        for r in range(TOTAL_ROWS - 3):
            if board[r][c] == value and board[r + 1][c + 1] == value and board[r + 2][c + 2] == value and board[r + 3][
                c + 3] == value:
                return True


# AI's turn or action is passed into utility function
def utilityFunction(board, action):
    hScore = 0
    # heuristic score for action at center column
    centerColumn = [int(i) for i in list(board[:, TOTAL_COLUMNS//2])]
    centerCount = centerColumn.count(action)
    hScore += centerCount * 3

    # heurisitc score for next horizontal move
    for r in range(TOTAL_ROWS):
        rowArray = [int(i) for i in list(board[r,:])]  # every column for specific row
        for c in range(TOTAL_COLUMNS - 3):
            toCheck = rowArray[c:c + 4] # checking each row starting from c to next 4
            hScore += staticEvaluation(toCheck, action)

    # heurisitc score for next vertical move
    for c in range(TOTAL_COLUMNS):
        colArray = [int(i) for i in list(board[:,c])]  # every row for specific column
        for r in range(TOTAL_ROWS - 3):
            toCheck = colArray[r:r + 4] # checking each column starting from r to next 4
            hScore += staticEvaluation(toCheck, action)

    # heurisitc score for next downward diagaonal move
    for r in range(TOTAL_ROWS - 3):
        for c in range(TOTAL_COLUMNS - 3):
            toCheck = [board[r + 3 - i][c + i] for i in range(4)] # checking each diagonal starting from r to next 4
            hScore += staticEvaluation(toCheck, action)

    # heurisitc score for next upward diagonal move
    for r in range(TOTAL_ROWS - 3):
        for c in range(TOTAL_COLUMNS - 3):
            toCheck = [board[r + i][c + i] for i in range(4)]
            hScore += staticEvaluation(toCheck, action)

    return hScore


# helps to calculate heurisitic score by taking how many empty or filled(toCheck) action
def staticEvaluation(toCheck, action):
    score = 0
    opponent = 1
    if action == 1:
        opponent = 2

    if toCheck.count(opponent) == 3 and toCheck.count(0) == 1:
        score -= 4 # if there is an opportunity for opp to make 3 then assign -4

    elif toCheck.count(action) == 3 and toCheck.count(0) == 1:
        score += 5 # if there is an opportunity to make 3 then assign 5

    elif toCheck.count(action) == 2 and toCheck.count(0) == 2:
        score += 2  # if there is an opportunity to make 2 then assign 2

    elif toCheck.count(action) == 4:
        score += 100 # if there is an opportunity to make 4 then assign 100

    if toCheck.count(opponent) == 2 and toCheck.count(0) == 1:
        score -= 2 # if there is an opportunity for opp to make 3 then assign -2

    return score


def validMoves(board):
    moves = []
    for col in range(TOTAL_COLUMNS):
        if validPosition(board, col):
            moves.append(col)
    return moves


def terminalTest(board):
    return len(validMoves(board)) == 0 or isWinningMove(board, 1) or isWinningMove(board, 2)


def minimax(board, depth, maximizer):
    successor = validMoves(board)
    lastNode = terminalTest(board)
    if lastNode:
        if isWinningMove(board, 2):
            return (None, math.inf)
        elif isWinningMove(board, 1):
            return (None, -math.inf)
        else:
            return (None, 0)
    elif depth == 0:
        return (None, utilityFunction(board, 2))

    if maximizer:
        v = -math.inf
        column = random.choice(successor)
        for col in successor:
            row = nextValidPosition(board, col)
            # a copy is made so the maximizer can test the outcome while doing recursively
            b = board.copy()
            nextTurn(b, row, col, 2)
            updateStatEval = minimax(b, depth - 1, False)[1]
            if updateStatEval > v:
                v = updateStatEval
                column = col
        return column, v
    # minimizer
    else:
        v = math.inf
        column = random.choice(successor)
        for col in successor:
            row = nextValidPosition(board, col)
            # a copy is made so the minimizer can test the outcome
            b = board.copy()
            nextTurn(b, row, col, 1)
            updateStatEval = minimax(b, depth - 1, True)[1]
            if updateStatEval < v:
                v = updateStatEval
                column = col
        return column, v


a = int(input("Press 1 for HUMAN or Press 2 for AI: "))
print("")
board = initializeBoard()
printState(board)
gameOver = False
if a == 1:
    turn = random.randint(PLAYER, PLAYER2)  # to start with random turn
    print("Begin Game!!!!!!")

    while (gameOver == False):

        if turn == PLAYER:
            col = int(input("First Player's turn (enter between 0-6): "))
            if validPosition(board, col):
                row = nextValidPosition(board, col)
                nextTurn(board, row, col, 1)

                if isWinningMove(board, 1):
                    print("Player 1 Wins!")
                    gameOver = True

                printState(board)
                turn += 1
                turn = turn % 2  # to keep the value between 0 & 1

        if turn == PLAYER2 and gameOver == False:
            col = int(input("Second Player's turn (enter between 0-6): "))
            if validPosition(board, col):
                row = nextValidPosition(board, col)
                nextTurn(board, row, col, 2)

                if isWinningMove(board, 2):
                    print("Player 2 Wins!")
                    gameOver = True

                printState(board)
                turn += 1
                turn = turn % 2  # to keep the value between 0 & 1
    print("Game Over!!!!!")

if a == 2:
    turn = random.randint(PLAYER, AI)  # to start with random turn
    print("Begin Game with AI")
    d = int(input("Enter Depth for AI (4 = less than a sec, 5 = 5 sec, 6 = 40 sec, 7 = 3 min+):  "))

    while (gameOver == False):

        if turn == PLAYER:
            col = int(input("First Player's turn (enter between 0-6): "))
            if validPosition(board, col):
                row = nextValidPosition(board, col)
                nextTurn(board, row, col, 1)

                if isWinningMove(board, 1):
                    print("Player 1 Wins!")
                    gameOver = True

                printState(board)
                turn += 1
                turn = turn % 2  # to keep the value between 0 & 1

        elif turn == AI and gameOver == False:

            col, minimaxScore = minimax(board, d, True)
            print("AI's Turn")
            if validPosition(board, col):
                row = nextValidPosition(board, col)
                nextTurn(board, row, col, 2)

                if isWinningMove(board, 2):
                    print("AI Wins!")
                    gameOver = True

                printState(board)
                turn += 1
                turn = turn % 2  # to keep the value between 0 & 1
    print("Game Over!!!!!")

else:
    print("Wrong Choice! Run again.")
