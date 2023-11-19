import random
import numpy as np
import time
from itertools import product


ROW_LENGTH = 4
STARTING_NUMBERS = 2
CHANCE_OF_TWO = 90
PLAYER_SCORE = 0
TOTAL_MOVES = 0
NUMBER_OF_RUNS = 6
DEPTH = 4
BEST_SCORE = 0

POSSIBLE_MOVES = ["up", "right", "down", "left"]
POSSIBLE_ARRANGEMENTS = product(POSSIBLE_MOVES, repeat=DEPTH)
TEMPLATE = [[0.135, 0.121, 0.102, 0.0999],
            [0.0997, 0.088, 0.076, 0.0724],
            [0.0606, 0.0562, 0.0371, 0.0161],
            [0.0125, 0.0099, 0.0057, 0.0033]]

def generateTile():
    RANDOM_NUM = random.randint(1, 100)
    if RANDOM_NUM < CHANCE_OF_TWO:
        number = 2
    else:
        number = 4
    return number


def createGrid(dimensions):
    grid = [[0 for i in range(dimensions)] for j in range(dimensions)]
    for i in range(STARTING_NUMBERS):
        number = generateTile()
        grid[random.randint(0, ROW_LENGTH - 1)][random.randint(0, ROW_LENGTH - 1)] = number
    displayGrid(grid)
    return grid


def displayGrid(*grids):
    for grid in grids:
        print(np.array(grid))


def evalgrid(grid):
    return np.sum(np.array(grid) * TEMPLATE)


def move(direction, grid, score):
    if direction == "left" or direction == "right":
        for i in range(ROW_LENGTH):
            if direction == "right": grid[i] = grid[i][::-1]
            for j in range(grid[i].count(0)):
                grid[i].append(grid[i].pop(grid[i].index(0)))

            for element in range(0, ROW_LENGTH - 1):
                if grid[i][element] == grid[i][element + 1]:
                    score += grid[i][element] * 2
                    grid[i][element] = grid[i][element] * 2
                    grid[i].remove(grid[i][element + 1])
                    grid[i].append(0)
            if direction == "right": grid[i] = grid[i][::-1]

        return grid, score

    else:
        collection = [grid[j][i] for i in range(0, ROW_LENGTH) for j in range(0, ROW_LENGTH)]
        vGrid = [collection[i * ROW_LENGTH:((i + 1) * ROW_LENGTH)] for i in range(ROW_LENGTH)]

        for i in range(ROW_LENGTH):
            if direction == "down": vGrid[i] = vGrid[i][::-1]
            for j in range(vGrid[i].count(0)):
                vGrid[i].append(vGrid[i].pop(vGrid[i].index(0)))
            for element in range(0, ROW_LENGTH - 1):
                if vGrid[i][element] == vGrid[i][element + 1]:
                    score += grid[i][element] * 2
                    vGrid[i][element] = vGrid[i][element] * 2
                    vGrid[i].remove(vGrid[i][element + 1])
                    vGrid[i].append(0)
            if direction == "down": vGrid[i] = vGrid[i][::-1]

        for row in range(ROW_LENGTH):
            for column in range(ROW_LENGTH):
                grid[row][column] = vGrid[column][row]

        return grid, score


def check(grid):
    gridArr = []

    for direction in POSSIBLE_MOVES:
        temp = [x[:] for x in grid]
        gridArr.append(move(direction, temp, PLAYER_SCORE))

    for potentialGrid in gridArr:
        if grid != potentialGrid[0]:
            return False
    return True


def updateGrid(grid, state):
    count = 0
    for i in range(ROW_LENGTH):
        count += grid[i].count(0)

    if not count:
        if check(grid):
            return grid, True

    if state == True:
        while True:
            row = random.randint(0, ROW_LENGTH - 1)
            column = random.randint(0, ROW_LENGTH - 1)
            if grid[row][column] == 0:
                grid[row][column] = generateTile()
                return grid, False
    return grid, False


def bestmove(grid, CURR_DEPTH, SET_OF_MOVES, currentscore):
    CURR_DEPTH += 1
    placeholder = [x[:] for x in grid]
    if CURR_DEPTH != DEPTH:
        for DIRECTION in POSSIBLE_MOVES:
            grid = move(DIRECTION, grid, currentscore)[0]
            SET_OF_MOVES.append(DIRECTION)
            if grid != placeholder:
                grid = updateGrid(grid, True)[0]
                bestmove(grid, CURR_DEPTH, SET_OF_MOVES, currentscore)

            SET_OF_MOVES.pop()
            grid = [x[:] for x in placeholder]
        return

    else:
        global BEST_SCORE
        global BEST_DIRECTION
        global BEST_GRID
        SCORE = evalgrid(grid)
        if BEST_SCORE < SCORE:
            BEST_SCORE = SCORE
            BEST_DIRECTION = SET_OF_MOVES[0]
            BEST_GRID = grid

        return
    return


def main():

    board = createGrid(ROW_LENGTH)
    TOTAL_MOVES = 0
    PLAYER_SCORE = 0

    while board:
        bestmove(board, 0, [], PLAYER_SCORE)
        placeholder = [x[:] for x in board]
        board = BEST_GRID

        if placeholder == board:

            ended = True
        else:
            board, ended = updateGrid(board, True)
        TOTAL_MOVES += 1
        if TOTAL_MOVES%1000==0:
            displayGrid(board)
        if ended:
            displayGrid(board)
            print("DONE")
            PLAYER_SCORE = sum(map(sum,board))
            return TOTAL_MOVES, PLAYER_SCORE


for i in range(NUMBER_OF_RUNS):
    start = time.time()
    moves, score = main()

    DEPTH += 1
    if score>=2048:
        print("WIN")
    else: print("GAME OVER");
    print("Run: ",i)
    print ("Number of moves of run = ",moves)
    print ("Final score of run = ",score)
    print("Time of run = %s s/min" % (time.time() - start))
    print (" ")
    print("-------------NEW RUN---------------------")
    print (" ")
