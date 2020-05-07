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
    for x in range(8):
        for y in range(8):
            pygame.draw.rect(screen,(0,0,0),(FIELD_START_POS[0] + CELL_SIZE*x, FIELD_START_POS[1] + CELL_SIZE*y, CELL_SIZE, CELL_SIZE),1)


def check_cell(cell, opponent_figures):
    if (0 <= cell[0] <= 7) and (0 <= cell[1] <= 7):
        if field[cell[1]][cell[0]] == ' ':
            return 1
        elif cell in opponent_figures:
            return 2
        else:
            return 0
    else:
        return 0
    

def check_pawn(cell, opponent_figures):
    admissible = []
    if opponent_figures == black_figures:
        direction, start = 1, 1
    else:
        direction, start = -1, 6
    if cell[1] == start:
        if check_cell((cell[0], cell[1] + 1*direction), opponent_figures) == 1: admissible.append([cell[0], cell[1] + 1*direction])
        if check_cell((cell[0], cell[1] + 2*direction), opponent_figures) == 1: admissible.append([cell[0], cell[1] + 2*direction])
    else:
        if check_cell((cell[0], cell[1] + 1*direction), opponent_figures) == 1: admissible.append([cell[0], cell[1] + 1*direction])
    if check_cell([cell[0] + 1, cell[1] + 1*direction], opponent_figures) == 2: admissible.append([cell[0] + 1, cell[1] + 1*direction])
    if check_cell([cell[0] - 1, cell[1] + 1*direction], opponent_figures) == 2: admissible.append([cell[0] - 1, cell[1] + 1*direction])
    return admissible


def check_king(cell, opponent_figures):
    admissible = []
    for x, y in ([-1,-1], [0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0]):
        if check_cell([cell[0] + x, cell[1] + y], opponent_figures): admissible.append([cell[0] + x, cell[1] + y])
    return admissible


def check_bishop(cell, opponent_figures):
    admissible = []
    for x,y in zip(range(cell[0]+1, 8), range(cell[1]-1, -1, -1)):
        code = check_cell([x, y], opponent_figures)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    for x,y in zip(range(cell[0]+1, 8), range(cell[1]+1, 8)):
        code = check_cell([x, y], opponent_figures)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    for x,y in zip(range(cell[0]-1, -1, -1), range(cell[1]+1,8)):
        code = check_cell([x, y], opponent_figures)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    for x,y in zip(range(cell[0]-1, -1, -1), range(cell[1]-1, -1, -1)):
        code = check_cell([x, y], opponent_figures)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    return admissible


def check_knight(cell, opponent_figures):
    admissible = []
    for x,y in ([1,-2], [2,-1], [2,1], [1,2], [-1,2], [-2,1], [-2,-1], [-1,-2]):
        if check_cell([cell[0] + x, cell[1] + y], opponent_figures): admissible.append([cell[0] + x, cell[1] + y])
    return admissible


def check_rook(cell, opponent_figures):
    admissible = []
    for x in range(cell[0]+1, 8):
        code = check_cell([x, cell[1]], opponent_figures)
        if code == 1:
            admissible.append([x, cell[1]])
        elif code == 2:
            admissible.append([x, cell[1]])
            break
        else:
            break
    for x in range(cell[0]-1, -1, -1):
        code = check_cell([x, cell[1]], opponent_figures)
        if code == 1:
            admissible.append([x, cell[1]])
        elif code == 2:
            admissible.append([x, cell[1]])
            break
        else:
            break
    for y in range(cell[1]+1, 8):
        code = check_cell([cell[0], y], opponent_figures)
        if code == 1:
            admissible.append([cell[0], y])
        elif code == 2:
            admissible.append([cell[0], y])
            break
        else:
            break
    for y in range(cell[1]-1, -1, -1):
        code = check_cell([cell[0], y], opponent_figures)
        if code == 1:
            admissible.append([cell[0], y])
        elif code == 2:
            admissible.append([cell[0], y])
            break
        else:
            break    
    return admissible


def check_queen(cell, opponent_figures):
    admissible = []
    for x,y in zip(range(cell[0]+1, 8), range(cell[1]-1, -1, -1)):
        code = check_cell([x, y], opponent_figures)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    for x,y in zip(range(cell[0]+1, 8), range(cell[1]+1, 8)):
        code = check_cell([x, y], opponent_figures)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    for x,y in zip(range(cell[0]-1, -1, -1), range(cell[1]+1,8)):
        code = check_cell([x, y], opponent_figures)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    for x,y in zip(range(cell[0]-1, -1, -1), range(cell[1]-1, -1, -1)):
        code = check_cell([x, y], opponent_figures)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    for x in range(cell[0]+1, 8):
        code = check_cell([x, cell[1]], opponent_figures)
        if code == 1:
            admissible.append([x, cell[1]])
        elif code == 2:
            admissible.append([x, cell[1]])
            break
        else:
            break
    for x in range(cell[0]-1, -1, -1):
        code = check_cell([x, cell[1]], opponent_figures)
        if code == 1:
            admissible.append([x, cell[1]])
        elif code == 2:
            admissible.append([x, cell[1]])
            break
        else:
            break
    for y in range(cell[1]+1, 8):
        code = check_cell([cell[0], y], opponent_figures)
        if code == 1:
            admissible.append([cell[0], y])
        elif code == 2:
            admissible.append([cell[0], y])
            break
        else:
            break
    for y in range(cell[1]-1, -1, -1):
        code = check_cell([cell[0], y], opponent_figures)
        if code == 1:
            admissible.append([cell[0], y])
        elif code == 2:
            admissible.append([cell[0], y])
            break
        else:
            break
    return admissible


def check_positions(cell, player_figures, opponent_figures):
    # cell = field[y][x] -> 'f','p'...
    admissible = []
    figure = field[cell[1]][cell[0]]
    if figure == 'p':
        admissible = check_pawn(cell, opponent_figures)
    elif figure == 'r':
        admissible = check_rook(cell, opponent_figures)
    elif figure == 'h':
        admissible = check_knight(cell, opponent_figures)
    elif figure == 'b':
        admissible = check_bishop(cell, opponent_figures)
    elif figure == 'q':
        admissible = check_queen(cell, opponent_figures)
    elif figure == 'k':
        admissible = check_king(cell, opponent_figures)
    return admissible
    

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


def take_figure(player_figures, opponent_figures):
    global selected, selected_figure, selected_cell, white_step, black_step
    opponent_figures.remove(selected_cell) # Удаляем фигуру у противника
    field[selected_cell[1]][selected_cell[0]] = field[selected_figure[1]][selected_figure[0]] # Перемещаем свою фигуру на место удаленной
    field[selected_figure[1]][selected_figure[0]] = ' ' # Очищаем клетку перемещенной фигуры
    player_figures[player_figures.index(selected_figure)] = selected_cell[:] # Меняем координаты выбранной фигуры на координаты выбранной ячейки
    white_step, black_step = black_step, white_step
    selected,selected_figure,selected_cell = False, None, None


def move_figure(player_figures):
    global selected, selected_figure, selected_cell, white_step, black_step
    field[selected_cell[1]][selected_cell[0]] = field[selected_figure[1]][selected_figure[0]] # Перемещаем фигуру на новое место
    field[selected_figure[1]][selected_figure[0]] = ' ' # Очищаем клетку перемещенной фигуры
    player_figures[player_figures.index(selected_figure)] = selected_cell[:]
    white_step, black_step = black_step, white_step
    selected,selected_figure,selected_cell = False, None, None



SIZE_X, SIZE_Y = 640, 480
DELAY = 30
COLOR_BACKGROUND = [255, 255, 255]
COLOR_TEXT = [0, 0, 0]
COLOR_YELLOW = (200, 200, 0)
COLOR_RED = (200, 0, 0)
COLOR_GREEN = (0, 200, 0)
CELL_SIZE = 40
FIGURE_SIZE = 30
FIELD_START_POS = [5, 5]
FIELD_LENGTH = 400
CELL_SIZE = int(FIELD_LENGTH/8)
MARGIN = 5 # Расстояние откраев ячейки до фигуры
FIGURE_SIZE = CELL_SIZE - MARGIN*2
FIGURE_START_POS = [FIELD_START_POS[0] + MARGIN, FIELD_START_POS[1] + MARGIN]

field = [
    ['r','h','b','q','k','b','h','r'],
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
admissible_positions = []
selected_cell = None
selected_figure = None
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
        pygame.draw.rect(screen, COLOR_GREEN, (selected_cell[0]*CELL_SIZE + FIELD_START_POS[0],selected_cell[1]*CELL_SIZE + FIELD_START_POS[1],CELL_SIZE,CELL_SIZE), 4)
        for cell in admissible_positions:
            pygame.draw.rect(screen, COLOR_YELLOW, (cell[0]*CELL_SIZE + FIELD_START_POS[0], cell[1]*CELL_SIZE + FIELD_START_POS[1], CELL_SIZE, CELL_SIZE), 4)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.KEYDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x = ((pygame.mouse.get_pos()[0] - FIELD_START_POS[0]) // CELL_SIZE)
                y = ((pygame.mouse.get_pos()[1] - FIELD_START_POS[1]) // CELL_SIZE)
                selected_cell = [x,y]
                if selected_cell in white_figures and white_step:
                    selected_figure = selected_cell[:]
                    admissible_positions = check_positions(selected_figure[:], white_figures, black_figures)
                    print('selected white',field[y][x])
                    selected = True
                elif selected_cell in black_figures and black_step:
                    selected_figure = selected_cell
                    admissible_positions = check_positions(selected_figure[:], black_figures, white_figures)
                    print('selected black',field[y][x])
                    selected = True
                else:
                    if selected_figure != None and white_step: # Если выбрана фигура и ячейка
                        if selected_cell in black_figures:
                            take_figure(white_figures, black_figures)
                        else:
                            move_figure(white_figures)
                    elif selected_figure != None and black_step:
                        if selected_cell in white_figures:
                            take_figure(black_figures, white_figures)
                        else:
                            move_figure(black_figures)
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
