import pygame
import time
import random
pygame.font.init()

win = pygame.display.set_mode((545,700))

pygame.display.set_caption("Sudoku")
icon = pygame.image.load('sudoku.png')
pygame.display.set_icon(icon)

class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    board_easy = [
        [9, 7, 0, 8, 0, 3, 5, 0, 1],
        [6, 0, 8, 0, 4, 0, 9, 0, 3],  
        [0, 5, 0, 0, 9, 1, 0, 8, 0],  
        [5, 0, 9, 1, 0, 8, 7, 0, 6],  
        [0, 2, 0, 6, 0, 7, 0, 5, 0],  
        [7, 0, 6, 4, 5, 0, 2, 0, 8],  
        [2, 0, 5, 3, 0, 0, 0, 7, 4],  
        [1, 0, 0, 0, 7, 2, 3, 0, 5], 
        [0, 6, 7, 5, 0, 4, 8, 0, 2],
    ]

    board_medium = [
        [3, 4, 0, 8, 0, 1, 0, 6, 0],  
        [0, 0, 9, 6, 0, 3, 1, 0, 4], 
        [8, 0, 0, 0, 2, 0, 0, 3, 0],
        [0, 9, 0, 0, 0, 6, 8, 0, 0], 
        [4, 5, 2, 7, 1, 0, 0, 9, 6],
        [0, 0, 3, 5, 0, 2, 0, 0, 1],
        [7, 3, 0, 0, 6, 0, 9, 0, 0], 
        [0, 0, 0, 9, 0, 7, 0, 2, 0],  
        [9, 0, 4, 0, 8, 0, 6, 0, 3],
    ]

    board_hard = [
        [0, 9, 4, 0, 6, 0, 0, 1, 0],  
        [7, 0, 0, 4, 0, 9, 6, 0, 8],  
        [0, 6, 0, 0, 0, 0, 0, 9, 0],  
        [1, 0, 2, 0, 4, 7, 0, 6, 0],  
        [0, 7, 0, 3, 0, 0, 2, 0, 1], 
        [6, 0, 0, 5, 0, 2, 9, 7, 0],  
        [0, 8, 6, 0, 3, 4, 0, 0, 5],
        [5, 0, 0, 0, 7, 0, 3, 0, 9], 
        [0, 4, 0, 2, 0, 0, 0, 8, 0],
    ]


    list_board = [board,board_easy,board_medium,board_hard]

    rand_int = random.randint(0,3)
    board = list_board[rand_int]

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row,col)) and self.solve():
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (255, 255, 255), (2, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win, (255, 255, 255), (i * gap, 2), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i

                if self.solve():
                    return True

                self.model[row][col] = 0

        return False

    def solve_gui(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (255, 255, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (0, 0, 0), (x, y, gap, gap), 0)

        if self.value == 0:
            text = fnt.render(str(self.value), 1, (255, 255, 255))
        else:
            text = fnt.render(str(self.value), 1, (0, 125, 0))

        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None


def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True


def redraw_window(win, board, time, strikes,over,score):
    win.fill((0,0,0))
    # Draw time

    if Grid.rand_int == 0:
        level = "Normal"
    elif Grid.rand_int == 1:
        level = "Easy"
    elif Grid.rand_int == 2:
        level = "Medium"
    elif Grid.rand_int == 3:
        level = "Hard"

    fnt = pygame.font.SysFont("comicsans", 40)
    fnt1 = pygame.font.SysFont("comicsans", 35)
    if not over:
        lev = fnt1.render("Difficulty Rating: " + level,1,(255, 0, 255))
        win.blit(lev, (115,560))

        text = fnt.render("Time: " + format_time(time), 1, (255, 255, 255))
        win.blit(text, (540 - 160, 600))
        # Draw Strikes
        text = fnt.render("X " * strikes, 1, (255, 0, 0))
        win.blit(text, (20, 600))

        text = fnt.render("Score: " + str(score), 1, (200, 210, 220))
        win.blit(text, (540 - 160, 650))
    #
    elif over:

        lev = fnt.render("Difficulty Rating: " + level,1,(255, 0, 255))
        win.blit(lev, (115,560))

        text = fnt.render("Score: " + str(score), 1, (255, 255, 255))
        win.blit(text, (540 - 160, 650))

        text = fnt.render("Press R to restart or Q to quit", 1, (255, 255, 255))
        win.blit(text, (80, 600))

        text = fnt.render("Game over", 1, (255, 255, 0))
        win.blit(text, (20, 650))
    # Draw grid and board
    board.draw()


def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat

def write_board(bo, color = (255,255,255)): #writes the board to grid in pygame
    font = pygame.font.SysFont('Comic Sans', 50)
    for i in range(len(bo)):
        #selects the offset position of i and j
        pi = 12 + (i * tile_size) 
        for j in range(len(bo[0])):
            pj = 12 + (tile_size*j)
            if bo[i][j] == 0:
                text = font.render(" ", 1, (255,255,255))
            else:
                text = font.render(str(bo[i][j]), 1, color)
                win.blit(text, (pj,pi))
    pygame.display.update()

def main_screen():

    intro = True
    main_icon = pygame.image.load('sudoku1.png')

    win.fill((0,0,0))
    while intro:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
               intro = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                    main()
                if event.key == pygame.K_q:
                    intro=False
        
        main_font1 = pygame.font.Font('freesansbold.ttf',40)
        main_font2 = pygame.font.Font('freesansbold.ttf',20) 

        main_text1 = main_font1.render("Welcome to SODOKU",True ,(255,255,255))
        win.blit(main_text1,(80,150))

        main_text2 = main_font2.render("The objective is to complete the board",True,(255,255,255))
        win.blit(main_text2,(100,300))

        main_text4 = main_font2.render("Press C to continue or Q to quit",True,(255,255,255))
        win.blit(main_text4,(125,330))

        win.blit(main_icon,(210,440))

        pygame.display.update()


def main():
    
    fnt = pygame.font.SysFont("comicsans", 40)
    board = Grid(9, 9, 540, 540, win)

    key = None
    run = True
    over = False
    score = 0

    start = time.time()
    strikes = 0

    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None

                if event.key == pygame.K_SPACE:
                    board.solve_gui()
                    over = True

                if event.key == pygame.K_r:
                    main() 

                if event.key == pygame.K_q:
                    run = False                   

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                            score+=1
                        else:
                            print("Wrong")
                            strikes += 1
                            if strikes > 10:
                                over = True
                                print("Game over")
                        key = None

                        if board.is_finished():
                            print("Game over")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes,over,score)
        pygame.display.update()


main_screen()
pygame.quit()