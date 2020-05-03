import pygame
from random import randrange
pygame.init()
#import sys
#import pygameMenu
SIZE_X, SIZE_Y = 640, 480
DELAY = 30
COLOR_BACKGROUND = [255, 255, 255]
COLOR_TEXT = [0,0,0]
CELL_SIZE = 40
FIGURE_SIZE = 30
FIELD_START_POS = [5, 5]
FIELD_LENGTH = 400
CELL_SIZE = int(FIELD_LENGTH/8)
MARGIN = 5 # Расстояние откраев ячейки до фигуры
FIGURE_SIZE = CELL_SIZE - MARGIN*2
FIGURE_START_POS = [FIELD_START_POS[0] + MARGIN, FIELD_START_POS[1] + MARGIN]
text_font = pygame.font.SysFont('arial', 24)

screen = pygame.display.set_mode((SIZE_X, SIZE_Y))
pygame.display.flip()
screen.fill([255,255,255])

#menu = pygameMenu.TextMenu(screen, 200, 200,pygame.font.Font('arial',34), "Fucker")
pygame.display.set_caption('CHESS')
game = True
selected_cell = [0,0]
selected_figure = [0,0]
selected = False
black_step = False
white_step = True

black_figures = []
white_figures = []

field = f = [[0 for i in range(10)] for j in range(10)]

class ChessFigure():

    def __init__(self, x, y, type, side):
        self.x = x
        self.y = y
        self.type = type
        self.side = side


def check_position(figure_pos):# Проверяет, в какие точки поля может пойти переданная фигура, и возвращает список досткпных точек
    if 1:
        
        True
    else:
        return False


def draw_grid():
    for cells_x in range(8):
        for cells_y in range(8):
            pygame.draw.rect(screen,(0,0,0),(FIELD_START_POS[0] + CELL_SIZE*cells_x, FIELD_START_POS[1] + CELL_SIZE*cells_y, CELL_SIZE, CELL_SIZE),1)

def draw_figures():
    for figure in black_figures:
        pygame.draw.rect(screen,(0,0,0),(figure[0]+MARGIN, figure[1]+MARGIN, FIGURE_SIZE, FIGURE_SIZE) ,0)
    for figure in white_figures:
        pygame.draw.rect(screen,(0,0,0),(figure[0]+MARGIN, figure[1]+MARGIN, FIGURE_SIZE, FIGURE_SIZE), 1)

        
def init_white_figures():
    figures = []
    for cells_x in range(8):
        for cells_y in [0,1]:
            x = FIELD_START_POS[0] + CELL_SIZE*cells_x
            y = FIELD_START_POS[1] + CELL_SIZE*cells_y
            figures.append([x,y])
    return figures
            

def init_black_figures():
    figures = []
    for cells_x in range(8):
        for cells_y in [6,7]:
            x = FIELD_START_POS[0] + CELL_SIZE*cells_x
            y = FIELD_START_POS[1] + CELL_SIZE*cells_y
            figures.append([x,y])
    return figures

black_figures = init_black_figures()
white_figures = init_white_figures()
    

while game:
    pygame.time.delay(DELAY)
    screen.fill(COLOR_BACKGROUND)
    if selected:
        pygame.draw.rect(screen,(0,200,0),(selected_cell[0],selected_cell[1],CELL_SIZE,CELL_SIZE),4)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.KEYDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                selected_cell[0] = (pygame.mouse.get_pos()[0] // CELL_SIZE) * CELL_SIZE + 5
                selected_cell[1] = (pygame.mouse.get_pos()[1] // CELL_SIZE) * CELL_SIZE + 5
##                if CELL_SIZE*9 < selected_cell[0] < CELL_SIZE*10 and CELL_SIZE*9 < selected_cell[1] < CELL_SIZE*:
##                    pass
                if selected_cell in white_figures and white_step:
                    selected_figure = selected_cell[:]
                    print('selected white',selected_cell)
                    selected = True
                elif selected_cell in black_figures and black_step:
                    selected_figure = selected_cell[:]
                    print('selected black',selected_cell)
                    selected = True
                else:
                    if selected_figure != [0,0] and white_step:
                        white_figures[white_figures.index(selected_figure)] = selected_cell[:]
                        selected_figure = [0,0]
                        selected = False
                        white_step, black_step = black_step, white_step
                    elif selected_figure != [0,0] and black_step:
                        black_figures[black_figures.index(selected_figure)] = selected_cell[:]
                        selected_figure = [0,0]
                        black_step, white_step = white_step, black_step
                        selected = False
                    else:
                        selected = False
            elif event.button == 3:
                x = (pygame.mouse.get_pos()[0] // CELL_SIZE) * CELL_SIZE + 5
                y = (pygame.mouse.get_pos()[1] // CELL_SIZE) * CELL_SIZE + 5
                if x == selected_cell[0] and y == selected_cell[1]:
                    print('deselected', selected_cell)
                    selected = False
                    
    white_text = text_font.render('white step: ' + str(white_step), 0, COLOR_TEXT)
    black_text = text_font.render('black step: ' + str(black_step), 0, COLOR_TEXT)
    screen.blit(white_text,(410,20))
    screen.blit(black_text,(410,50))
    
    draw_grid()
    draw_figures()    
    pygame.display.flip()
pygame.quit()
                


#  print(pygame.mouse.get_pos()) позиция мыши
#  rint(event.buttons[0]) нажата ли левая кнопка мыши

# pygame.MOUSEMOTION - event.buttons = (0,0,0)
# pygame.MOUSEBUTTONDWON - event.button = 1,2...5

# text_font = pygame.font.Font(FONT_FILE, 24)
# score_text = text_font.render('score:{: >3}'.format(int(score)),0,TEXT_COLOR)
# screen.blit(score_text, (tetris_len_x+10,240))
