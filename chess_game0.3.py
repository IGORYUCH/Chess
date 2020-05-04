import pygame
from random import randrange
#menu = pygameMenu.TextMenu(screen, 200, 200,pygame.font.Font('arial',34), "Fucker")
## k - король
## f - королева (ферзь)
## b - епископ (слон)
## r - крепость (ладья)
## h - рыцарь (конь)
## p - пешка
def draw_grid():
    for cells_x in range(8):
        for cells_y in range(8):
            pygame.draw.rect(screen,(0,0,0),(FIELD_START_POS[0] + CELL_SIZE*cells_x, FIELD_START_POS[1] + CELL_SIZE*cells_y, CELL_SIZE, CELL_SIZE),1)


def draw_figures():
    for figure in black_figures:
        x = figure[0] * CELL_SIZE + FIGURE_START_POS[0]
        y = figure[1] * CELL_SIZE + FIGURE_START_POS[1]
        pygame.draw.rect(screen,(0,0,0),(x, y, FIGURE_SIZE, FIGURE_SIZE), 0)
        figure_letter = text_font.render(field[figure[1]][figure[0]],0, COLOR_BACKGROUND)
        screen.blit(figure_letter, (x+MARGIN, y+MARGIN))        
    for figure in white_figures:
        x = figure[0] * CELL_SIZE + FIGURE_START_POS[0]
        y = figure[1]*CELL_SIZE + FIGURE_START_POS[1]
        pygame.draw.rect(screen,(0,0,0),(x, y, FIGURE_SIZE, FIGURE_SIZE), 1)
        figure_letter = text_font.render(field[figure[1]][figure[0]],0, COLOR_TEXT)
        screen.blit(figure_letter, (x+MARGIN, y+MARGIN))


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

field = [
    ['r','k','b','q','k','b','h','r'],
    ['p','p','p','p','p','p','p','p'],
    [' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' '],
    ['p','p','p','p','p','p','p','p'],
    ['r','h','b','q','k','b','h','r'],
    ]

black_figures = [[j,i] for j in range(8) for i in range(6,8)]
white_figures = [[j,i] for j in range(8) for i in range(2)]
selected_cell = [0,0]
selected_figure = [0,0]
game = True
selected = False
black_step = False
white_step = True
pygame.init()
pygame.display.set_caption('CHESS')
screen = pygame.display.set_mode((SIZE_X, SIZE_Y))
text_font = pygame.font.SysFont('arial', 24)

while game:
    pygame.time.delay(DELAY)
    screen.fill(COLOR_BACKGROUND)
    if selected:
        pygame.draw.rect(screen,(0,200,0),(selected_cell[0]*CELL_SIZE+FIELD_START_POS[0],selected_cell[1]*CELL_SIZE+FIELD_START_POS[1],CELL_SIZE,CELL_SIZE),4)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.KEYDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x = ((pygame.mouse.get_pos()[0] - FIELD_START_POS[0]) // CELL_SIZE)
                y = ((pygame.mouse.get_pos()[1] - FIELD_START_POS[1]) // CELL_SIZE)
                if [x,y] in white_figures and white_step:
                    selected_cell = [x,y]
                    print('selected white',field[y][x])
                    selected = True
                elif [x,y] in black_figures and black_step:
                    selected_cell = [x,y]
                    print('selected black',field[y][x])
                    selected = True
                else:
                    if selected_cell != [0,0] and white_step:
                        
                        selected = False
                    white_step, black_step = black_step, white_step
                        selected_cell = [0,0]
                    


##
##                    
##                if selected_cell in white_figures and white_step:
##                    selected_figure = selected_cell[:]
##                    print('selected white',selected_cell)
##                    selected = True
##                elif selected_cell in black_figures and black_step:
##                    selected_figure = selected_cell[:]
##                    print('selected black',selected_cell)
##                    selected = True
##                else:
##                    if selected_figure != [0,0] and white_step:
##                        white_figures[white_figures.index(selected_figure)] = selected_cell[:]
##                        selected_figure = [0,0]
##                        selected = False
##                        white_step, black_step = black_step, white_step
##                    elif selected_figure != [0,0] and black_step:
##                        black_figures[black_figures.index(selected_figure)] = selected_cell[:]
##                        selected_figure = [0,0]
##                        black_step, white_step = white_step, black_step
##                        selected = False
##                    else:
##                        selected = False
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
