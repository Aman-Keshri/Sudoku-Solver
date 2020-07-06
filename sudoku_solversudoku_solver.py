import pygame, time
#Global vars
board_initial = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]


board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

s_width = 450
s_height = 450

tile_size = s_width // 9
gray = (128,128,128)

def solve(bo): #recursive backtracking
#once we reach end of board, solution has been found
#we can print up here in order to see all steps
    font = pygame.font.SysFont('Comic Sans', 50)
    win.fill((0,0,0))
    drawGrid()
    write_board(board)

    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            text = font.render(str(i), 1, (0,255,0))
            win.blit(text, ((12+(col*tile_size)),(12+(row*tile_size))))
            pygame.display.update()
            time.sleep(0.1)
            if solve(bo): #solve gets called within itself, which is why it is recursive
                return True
        
            bo[row][col] = 0
    return False


def valid(bo, num, pos):
    #check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    #check column
    for i in range(len(bo[0])):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    #check 3x3 modules or boxes
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    #loop through 9 elems in box

    for i in range(box_y*3, box_y*3 + 3): #finds index of number we're on multiplying box pos by 3 and adding 3
        for j in range(box_x*3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False
    return True


def format(bo): #used to display board as a string
    for i in range(len(bo)):
        if i %3 == 0 and i != 0:
            print("- - - - - - - - - - - - - - - -") 
        for j in range(len(bo[0])): #Length of each row
            if j %3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]), " ", end="")


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j) #row and column
    
    return None #if there's no blank sqrs return none


def drawGrid(): #Draws grid in pygame
    for i in range(0, s_height, tile_size):
        if i % 3 == 0 and i != 0:
            pygame.draw.line(win, gray, (i, 0 ), (i, s_height), 4)
        else:
            pygame.draw.line(win, gray, (i, 0 ), (i, s_height))
    for j in range(0, s_width, tile_size):
        if j % 3 == 0 and i != 0:
            pygame.draw.line(win, gray, (0, j), (s_width, j), 4)
        else:
            pygame.draw.line(win, gray, (0, j), (s_width, j))
    

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
            

def main_menu(win):
    run = True
    while run:
        pygame.font.init()
        win.fill((0,0,0))
        drawGrid()
        write_board(board)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                run = False
            if event.type == pygame.KEYDOWN: #Detects keypress state and solves
                if event.key == pygame.K_RETURN:
                    solve(board)
                    write_board(board, (0,255,0))
                    write_board(board_initial)
                    run = False
    time.sleep(10)

win = pygame.display.set_mode((s_width, s_height)) #Initializes and creates display
pygame.display.set_caption('Sudoku Solver')
main_menu(win)  # start game
