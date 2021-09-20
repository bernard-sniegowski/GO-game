# Welcome to GO - like game
# Author: Bernard Sniegowski
#
# You can find the description of the game in Readme.txt

import pygame
import numpy as np

# pylint: disable=E1101

# some RGB colors
WHITE = (255, 255, 255)  # color of the WHITE stones
BLACK = (0, 0, 0)  # will serve several purposes, mainly as the color of the grid and BLACK stones
BOARD_COLOR = (222, 184, 135)  # color of the board
TIME_END = (252, 18, 18)  # color of the "END OF TIME" text at the end of the game

whitePOINTS = 0  # number of points equal to the number of WHITE circles on the board
blackPOINTS = 0  # number of points equal to the number of BLACK circles on the board
whiteTIME = 6 * 1000  # time for the whole game for WHITE player in milliseconds
blackTIME = 600 * 1000  # time for the whole game for BLACK player in milliseconds
turnTIME = 30 * 1000  # time for one turn in milliseconds
turnTIME_left = turnTIME  # will keep track of time left in a given turn

# size of board - not to be changed during runtime
n = 19  # size of board edge

# window dimensions - not to be changed during runtime
win_width = 850
win_height = 850

# distance between board edge and the edge of the window
offset = 80

# board dimensions in window - not to be changed during runtime
board_width = win_width - 2 * offset
board_height = win_height - 2 * offset

# create board and fill with 0's
board = [[0 for i in range(n + 1)] for j in range(n + 1)]

# radius of circles
radius = 10


def main():
    """Main function of the program tha starts and maintains the game window"""
    # points and time need to be global, as well as window
    global whitePOINTS, blackPOINTS, whiteTIME, blackTIME, turnTIME_left, window, font, fontSIZE
    global n

    pygame.init()
    window = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption("GO with handicap")

    # font size and type - to display points and time and results
    fontSIZE = 20
    font = pygame.font.SysFont('arial', fontSIZE, True)

    # let the player choose grid size
    set_grid_size()

    run = True
    white_turn = True

    clock = pygame.time.Clock()
    move_time = pygame.time.get_ticks()

    # start the game
    while run and blackTIME > 10 and whiteTIME > 10 and whitePOINTS + blackPOINTS < n * n:
        redrawGameWindow()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                circ = pygame.mouse.get_pos()
                x = closest(circ[0], X)
                y = closest(circ[1], Y)
                i = int(np.where(X == x)[0])
                j = int(np.where(Y == y)[0])

                if board[i][j] == 0:
                    turnTIME_left = turnTIME
                    if white_turn:
                        pygame.draw.circle(window, WHITE, (x, y), radius)
                        board[i][j] = 'W'
                        whitePOINTS += 1
                        kill_enemies(i, j)
                    else:
                        pygame.draw.circle(window, BLACK, (x, y), radius)
                        board[i][j] = 'B'
                        blackPOINTS += 1
                        kill_enemies(i, j)
                    white_turn = not white_turn
                    pygame.display.update()

        current_time = pygame.time.get_ticks()
        time_difference = current_time - move_time
        if white_turn:
            whiteTIME -= time_difference
        else:
            blackTIME -= time_difference

        move_time = current_time
        turnTIME_left -= time_difference

        if turnTIME_left < 10:
            turnTIME_left = turnTIME
            white_turn = not white_turn

        clock.tick(60)

    # loop after game ends
    while run:
        timeEND = font.render('END OF TIME', True, TIME_END)
        x = np.random.rand() * win_width
        y = np.random.rand() * win_width
        window.blit(timeEND, (x, y))

        pygame.display.update()
        pygame.time.delay(500)

        r = np.random.rand() * 255
        g = np.random.rand() * 255
        b = np.random.rand() * 255
        WINNER = (r, g, b)
        winner = font.render('DRAW! NO ONE WINS', True, WINNER)
        x = np.random.rand() * win_width
        y = np.random.rand() * win_width

        if whitePOINTS + blackPOINTS == n * n:
            if whitePOINTS > blackPOINTS:
                winner = font.render('WHITE WINS!', True, WINNER)
            elif blackPOINTS > whitePOINTS:
                winner = font.render('BLACK WINS!', True, WINNER)
        else:
            if whiteTIME > blackTIME and whitePOINTS > blackPOINTS:
                winner = font.render('WHITE WINS!', True, WINNER)
            elif blackTIME > whiteTIME and blackPOINTS > whitePOINTS:
                winner = font.render('BLACK WINS!', True, WINNER)

        window.blit(winner, (x, y))

        pygame.display.update()
        pygame.time.delay(500)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


def set_grid_size():
    global window, n

    window.fill(BOARD_COLOR)

    font_for_title = pygame.font.SysFont('arial', 30, True)
    window.blit(font_for_title.render('Choose grid size', True, BLACK), (win_width / 2 - 2 * offset, 0))

    grid_sizes = ['19x19', '17x17', '13x13', '9x9']
    grid_dict = {0 : 19, 1 : 17, 2 : 13, 3 : 9}

    grid_sizes_render = []
    input_boxes = []
    for i in range(4):
        grid_sizes_render += [font.render(grid_sizes[i], True, BLACK)]
        input_boxes += [pygame.Rect(win_width * i / 4, win_height * i / 4, 70, 30)]
        pygame.draw.rect(window, WHITE, (win_width * i / 4, win_height * i / 4, 70, 30))
        window.blit(grid_sizes_render[i], (win_width * i / 4, win_height * i / 4))

    pygame.display.update()

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect in input_boxes:
                    if rect.collidepoint(event.pos):
                        index = input_boxes.index(rect)
                        n = grid_dict[index]
                        run = False


def redrawGameWindow():
    """Redraws the whole game window. Will be called continuously in main() function."""
    window.fill(BOARD_COLOR)
    drawBoard()
    textWHITE = font.render('White: ' + str(whitePOINTS), True, BLACK)
    textBLACK = font.render('Black: ' + str(blackPOINTS), True, BLACK)
    timerWHITE = font.render('Time left: ' + str(whiteTIME // 1000) + ' s', True, BLACK)
    timerBLACK = font.render('Time left: ' + str(blackTIME // 1000) + ' s', True, BLACK)
    timerTURN = font.render('Time left in this turn: ' + str(turnTIME_left // 1000), True, BLACK)
    window.blit(textWHITE, (offset + 1, 1))
    window.blit(timerWHITE, (offset + 1, fontSIZE + 3))
    window.blit(textBLACK, (win_width / 2 + offset + 1, 1))
    window.blit(timerBLACK, (win_width / 2 + offset + 1, fontSIZE + 3))
    window.blit(timerTURN, (offset + 1, 2 * fontSIZE + 6))

    for i in range(n):
        for j in range(n):
            COLOR = board[i][j]
            if COLOR == 'W':
                draw_circle(i, j, WHITE)
            if COLOR == 'B':
                draw_circle(i, j, BLACK)
    pygame.display.update()


def drawBoard():
    """Draw board on window surface."""
    COLOR = BLACK

    # two numpy arrays to store X-Y positions
    global X, Y
    X = np.linspace(offset, board_width + offset, n)
    Y = np.linspace(offset, board_height + offset, n)

    vertical = [((X[k], Y[0]), (X[k], Y[n-1])) for k in range(n)]
    horizontal = [((X[0], Y[k]), (X[n-1], Y[k]))for k in range(n)]

    for point in vertical:
        pygame.draw.line(window, COLOR, point[0], point[1])
    for point in horizontal:
        pygame.draw.line(window, COLOR, point[0], point[1])


def closest(x, A):
    """Find closest element to x in A."""
    return A[np.abs(A-x).argmin()]


def draw_circle(i, j, COLOR):
    """Draw circle on window surface centerd at (i, j) on board"""
    pygame.draw.circle(window, COLOR, (X[i], Y[j]), radius)


def find_dead(i, j):
    """Checks wheter a stone on (i, j) belongs to a dead group. Uses BFS"""
    COLOR = board[i][j]
    current = (i, j)
    queue = [current]
    visited = []

    while queue:
        current = queue[0]
        visited += [current]
        queue.pop(0)
        neighbours = get_neighbours(*current)
        zero_neighbours = [index for index in neighbours if board[index[0]][index[1]] == 0]
        if zero_neighbours:
            visited.clear()
            return visited
        neighbours = [index for index in neighbours if board[index[0]][index[1]] == COLOR]
        for neighbour in neighbours:
            if neighbour not in visited:
                queue += [neighbour]

    return visited


def kill_enemies(i, j):
    """Tries to kill all opponent's neighbours of (i, j). Uses find_dead() on every neighbout of (i, j)"""
    global whitePOINTS, blackPOINTS
    COLOR = board[i][j]
    enemyCOLOR = 'W'
    if COLOR == 'W':
        enemyCOLOR = 'B'

    dead_enemies = []

    for neighbour in [index for index in get_neighbours(i, j) if board[index[0]][index[1]] == enemyCOLOR]:
        dead_enemies += find_dead(*neighbour)

    dead_enemies = set(dead_enemies)
    if enemyCOLOR == 'W':
        whitePOINTS -= len(dead_enemies)
    else:
        blackPOINTS -= len(dead_enemies)

    for index in dead_enemies:
        i = index[0]
        j = index[1]
        draw_circle(i, j, BOARD_COLOR)
        board[i][j] = 0


def get_neighbours(i, j):
    """Gets all neighbours of (i, j) index"""
    RANGE = [(a, b) for a in range(n) for b in range(n)]
    return [(i + a, j) for a in [-1, 1] if (i + a, j) in RANGE] + [(i, j + a) for a in [-1, 1] if (i, j + a) in RANGE]


if __name__ == "__main__":
    main()
