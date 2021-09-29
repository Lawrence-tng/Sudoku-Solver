import pygame
import time

pygame.font.init()

board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7],
]


def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False


def valid(bo, num, pos):
    # check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i].value == num and pos[1] != i:
            return False

    # check col
    for i in range(len(bo)):
        if bo[i][pos[1]].value == num and pos[0] != i:
            return False

    # check box
    box_x = pos[1] // 3

    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j].value == num and (i, j) != pos:
                return False

    return True


def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - - ")

        for j in range(len(bo[0])):
            if j % 3 == 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])

            else:
                print(str(bo[i][j]) + " ", end="")


def find_empty(bo):
    for i in range(9):
        for j in range(9):
            print(bo[i][j].value)
            if bo[i][j].value == 0:

                return (i,j)  # row, col

    return None


board_width = 540
board_height = 540
gap = board_width / 9
pygame.init()
win = pygame.display.set_mode((board_width, board_height))

pygame.display.set_caption("SudokuSolver")


class Grids:
    def __init__(self):
        self.grids = [[Grid(board[i][j], i, j, ) for j in range(9)] for i in range(9)]
        self.win = win

    def solve_grids(self):
        find = find_empty(self.grids)
        if not find:
            return True
        else:
            row, col = find
            print(find)

        for i in range(1, 10):
            if valid(self.grids, i, (row, col)):
                self.grids[row][col].value = i
                self.grids[row][col].draw_grid(self.win, True)
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_grids():
                    return True

                self.grids[row][col].value = 0
                self.grids[row][col].draw_grid(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


class Grid:
    def __init__(self, value, row, col):
        self.value = value
        self.col = col
        self.row = row
        self.selected = False

    def select(self):
        pygame.draw.rect(win, (0, 0, 255), (self.col * gap, self.row * gap, gap, gap))
        pygame.display.update()
        draw_initial_brd()

    def unselect(self):
        pygame.draw.rect(win, (255, 255, 255), (self.col * gap, self.row * gap, gap, gap))
        pygame.display.update()
        draw_initial_brd()

    def draw_grid(self, win, valid=True):
        fnt = pygame.font.SysFont("comicsans", 40)
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))

        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap/2 - text.get_height() / 2)))
        if valid:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)

        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)


def draw_initial_brd():
    square_length = board_width / 9
    for i in range(9):
        if i % 3 == 0 and i != 0:
            line_size = 4
        else:
            line_size = 1

        pygame.draw.line(win, (0, 0, 0), (0, i * square_length), (board_width, i * square_length), line_size)
        pygame.draw.line(win, (0, 0, 0), (i * square_length, 0), (i * square_length, board_height), line_size)

    pygame.display.update()


def draw_brd(bo):
    fnt = pygame.font.SysFont("comicsans", 40)
    space = board_width / 9

    for i in range(9):
        for j in range(9):
            x = i * space
            y = j * space

            if bo[i][j] != 0:
                text = fnt.render(str(bo[i][j]), 1, (0, 0, 0))
                win.blit(text, (y + (space / 2 - text.get_height() / 2), x + (space / 2 - text.get_width() / 2)))

#run to start visualier
def main():
    win.fill((255, 255, 255))
    run = True
    while run:
        pygame.time.delay(100)

        draw_initial_brd()
        draw_brd(board)

        game_grid = Grids()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if event.key == pygame.K_SPACE:
                        game_grid.solve_grids()

    pygame.quit()


main()
