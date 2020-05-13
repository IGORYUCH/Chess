import pygame
from random import randrange
import copy
def check_cell(cell, opponent_figures, field):
    if (0 <= cell[0] <= 7) and (0 <= cell[1] <= 7):
        if field[cell[1]][cell[0]] == ' ':
            return 1
        elif cell in opponent_figures:
            return 2
        else:
            return 0
    else:
        return 0


def check_shah(player_figures, opponent_figures, field):# Проверяет, бьет ли игрок короля своего оппонента
    admissible = []
    for player_figure in player_figures:
        if field[player_figure[1]][player_figure[0]] == 'k':
            player_king = player_figure[:]
            break
    for opponent_figure in opponent_figures:
        admissible = check_positions(opponent_figure, opponent_figures, player_figures, field)
        if player_king in admissible:
            return True
    else:
        return False


def check_checkmate(player_figures, opponent_figures, field):
    for player_figure in player_figures:
        admissible = check_positions(player_figure, player_figures, opponent_figures, field)
        admissible = exclude_check_unprotected(field[player_figure[1]][player_figure[0]], player_figure, admissible, player_figures, opponent_figures, field)
        if admissible:
            return False
    else:
        return True


def check_pawn(cell, opponent_figures, field): # Проверяет допустимые ячейки поля для хода пешкой
    admissible = []
    if opponent_figures == black_figures:
        direction, start_pos = -1, 6
    else:
        direction, start_pos = 1, 1
    if cell[1] == start_pos:
        for x,y in ([cell[0], cell[1] + 1*direction], [cell[0], cell[1] + 2*direction]):
            if check_cell([x, y], opponent_figures, field) == 1:
                admissible.append([x, y])
            else:
                break
    else:
        if check_cell((cell[0], cell[1] + 1*direction), opponent_figures, field) == 1:
            admissible.append([cell[0], cell[1] + 1*direction])
    if check_cell([cell[0] + 1, cell[1] + 1*direction], opponent_figures, field) == 2:
        admissible.append([cell[0] + 1, cell[1] + 1*direction])
    if check_cell([cell[0] - 1, cell[1] + 1*direction], opponent_figures, field) == 2:
        admissible.append([cell[0] - 1, cell[1] + 1*direction])
    return admissible


def check_king(cell, opponent_figures, field): # Проверяет допустимые поля ячейки для хода королем
    admissible = []
    for x, y in ([-1,-1], [0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0]):
        if check_cell([cell[0] + x, cell[1] + y], opponent_figures, field):
            admissible.append([cell[0] + x, cell[1] + y])
    return admissible


def check_bishop(cell, opponent_figures, field): # Проверяет допустимые ячейки поля для хода ладьей
    admissible = []
    for x,y in zip(range(cell[0]+1, 8), range(cell[1]-1, -1, -1)):
        code = check_cell([x, y], opponent_figures, field)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    for x,y in zip(range(cell[0]+1, 8), range(cell[1]+1, 8)):
        code = check_cell([x, y], opponent_figures, field)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    for x,y in zip(range(cell[0]-1, -1, -1), range(cell[1]+1,8)):
        code = check_cell([x, y], opponent_figures, field)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    for x,y in zip(range(cell[0]-1, -1, -1), range(cell[1]-1, -1, -1)):
        code = check_cell([x, y], opponent_figures, field)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    return admissible


def check_knight(cell, opponent_figures, field): # Проверяет допустимые ячейки поля для хода конем
    admissible = []
    for x,y in ([1, -2], [2, -1], [2, 1], [1, 2], [-1, 2], [-2, 1], [-2, -1], [-1, -2]):
        if check_cell([cell[0] + x, cell[1] + y], opponent_figures, field):
            admissible.append([cell[0] + x, cell[1] + y])
    return admissible


def check_rook(cell, opponent_figures, field): # Проверяет допустимые ячейки поля для хода ладьей
    admissible = []
    for x in range(cell[0] + 1, 8):
        code = check_cell([x, cell[1]], opponent_figures, field)
        if code == 1:
            admissible.append([x, cell[1]])
        elif code == 2:
            admissible.append([x, cell[1]])
            break
        else:
            break
    for x in range(cell[0]-1, -1, -1):
        code = check_cell([x, cell[1]], opponent_figures, field)
        if code == 1:
            admissible.append([x, cell[1]])
        elif code == 2:
            admissible.append([x, cell[1]])
            break
        else:
            break
    for y in range(cell[1]+1, 8):
        code = check_cell([cell[0], y], opponent_figures, field)
        if code == 1:
            admissible.append([cell[0], y])
        elif code == 2:
            admissible.append([cell[0], y])
            break
        else:
            break
    for y in range(cell[1]-1, -1, -1):
        code = check_cell([cell[0], y], opponent_figures, field)
        if code == 1:
            admissible.append([cell[0], y])
        elif code == 2:
            admissible.append([cell[0], y])
            break
        else:
            break
    return admissible


def check_queen(cell, opponent_figures, field): # Проверяет допустимые ячейки поля для хода ферзем
    admissible = []
    for x,y in zip(range(cell[0]+1, 8), range(cell[1]-1, -1, -1)):
        code = check_cell([x, y], opponent_figures, field)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    for x,y in zip(range(cell[0]+1, 8), range(cell[1]+1, 8)):
        code = check_cell([x, y], opponent_figures, field)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    for x,y in zip(range(cell[0]-1, -1, -1), range(cell[1]+1,8)):
        code = check_cell([x, y], opponent_figures, field)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    for x,y in zip(range(cell[0]-1, -1, -1), range(cell[1]-1, -1, -1)):
        code = check_cell([x, y], opponent_figures, field)
        if code == 1:
            admissible.append([x, y])
        elif code == 2:
            admissible.append([x, y])
            break
        else:
            break
    for x in range(cell[0] + 1, 8):
        code = check_cell([x, cell[1]], opponent_figures, field)
        if code == 1:
            admissible.append([x, cell[1]])
        elif code == 2:
            admissible.append([x, cell[1]])
            break
        else:
            break
    for x in range(cell[0] - 1, -1, -1):
        code = check_cell([x, cell[1]], opponent_figures, field)
        if code == 1:
            admissible.append([x, cell[1]])
        elif code == 2:
            admissible.append([x, cell[1]])
            break
        else:
            break
    for y in range(cell[1] + 1, 8):
        code = check_cell([cell[0], y], opponent_figures, field)
        if code == 1:
            admissible.append([cell[0], y])
        elif code == 2:
            admissible.append([cell[0], y])
            break
        else:
            break
    for y in range(cell[1] - 1, -1, -1):
        code = check_cell([cell[0], y], opponent_figures, field)
        if code == 1:
            admissible.append([cell[0], y])
        elif code == 2:
            admissible.append([cell[0], y])
            break
        else:
            break
    return admissible


def exclude_check_unprotected(figure, figure_cell, admissible, player_figures, opponent_figures, field): # Исключает из допустимых для хода ячеек поля те, которые не защищают короля от шаха
    new_admissible = copy.deepcopy(admissible)
    for admissible_pos in admissible:
        player_figures_copy = copy.deepcopy(player_figures)
        field_copy = copy.deepcopy(field)
        field_copy[admissible_pos[1]][admissible_pos[0]] = figure
        field_copy[figure_cell[1]][figure_cell[0]] = ' '
        opponent_figures_copy = copy.deepcopy(opponent_figures)
        if admissible_pos in opponent_figures:
            opponent_figures_copy.remove(admissible_pos)
        player_figures_copy[player_figures_copy.index(figure_cell)] = admissible_pos[:]
        future_check = check_shah(player_figures_copy, opponent_figures_copy, field_copy)
        if future_check:
            new_admissible.remove(admissible_pos)
    return new_admissible


def check_positions(cell, player_figures, opponent_figures, field): # Проверяет допустимые ячейки поля для хода фигуры в зависимости от ее типа
    # cell = field[y][x] -> 'f','p'...
    admissible = []
    figure = field[cell[1]][cell[0]]
    if figure == 'p':
        admissible = check_pawn(cell, opponent_figures, field)
    elif figure == 'r':
        admissible = check_rook(cell, opponent_figures, field)
    elif figure == 'h':
        admissible = check_knight(cell, opponent_figures, field)
    elif figure == 'b':
        admissible = check_bishop(cell, opponent_figures, field)
    elif figure == 'q':
        admissible = check_queen(cell, opponent_figures, field)
    elif figure == 'k':
        admissible = check_king(cell, opponent_figures, field)
    return admissible


def draw_figures(): # Рисует изображения фигур на на поверхности
    for figure in black_figures:
        x = figure[0] * CELL_SIZE + FIGURE_START_POS[0]
        y = figure[1] * CELL_SIZE + FIGURE_START_POS[1]
        if black_pictures[field[figure[1]][figure[0]]]:
            screen.blit(black_pictures[field[figure[1]][figure[0]]], (x, y))
    for figure in white_figures:
        x = figure[0] * CELL_SIZE + FIGURE_START_POS[0]
        y = figure[1] * CELL_SIZE + FIGURE_START_POS[1]
        if black_pictures[field[figure[1]][figure[0]]]:
            screen.blit(white_pictures[field[figure[1]][figure[0]]], (x, y))


def draw_admissible():
    for cell in admissible_positions:
        if selected_figure in white_figures and cell in black_figures:
            pygame.draw.rect(screen, COLOR_RED, (cell[0]*CELL_SIZE + FIELD_START_POS[0], cell[1]*CELL_SIZE + FIELD_START_POS[1], CELL_SIZE, CELL_SIZE), 3)
        elif selected_figure in black_figures and cell in white_figures:
            pygame.draw.rect(screen, COLOR_RED, (cell[0]*CELL_SIZE + FIELD_START_POS[0], cell[1]*CELL_SIZE + FIELD_START_POS[1], CELL_SIZE, CELL_SIZE), 3)
        else:
            pygame.draw.rect(screen, COLOR_YELLOW, (cell[0]*CELL_SIZE + FIELD_START_POS[0], cell[1]*CELL_SIZE + FIELD_START_POS[1], CELL_SIZE, CELL_SIZE), 3)
    

def take_figure(player_figures, opponent_figures): # Снимает атакуемую фигуру противника с поля и перемещает атакующую фигуру на ее место
    global selected, selected_figure, selected_cell, white_step, black_step
    opponent_figures.remove(selected_cell) # Удаляем фигуру у противника
    field[selected_cell[1]][selected_cell[0]] = field[selected_figure[1]][selected_figure[0]] # Перемещаем свою фигуру на место удаленной
    field[selected_figure[1]][selected_figure[0]] = ' ' # Очищаем клетку перемещенной фигуры
    player_figures[player_figures.index(selected_figure)] = selected_cell[:] # Меняем координаты выбранной фигуры на координаты выбранной ячейки
    white_step, black_step = black_step, white_step


def move_figure(player_figures):
    global selected, selected_figure, selected_cell, white_step, black_step
    field[selected_cell[1]][selected_cell[0]] = field[selected_figure[1]][selected_figure[0]] # Перемещаем фигуру на новое место
    field[selected_figure[1]][selected_figure[0]] = ' ' 
    player_figures[player_figures.index(selected_figure)] = selected_cell[:]
    white_step, black_step = black_step, white_step


def init_pictures(folder = 'pictures'): # Формирует массив из изображений фигур, взятых из папки

    def init_picture(file,colorkey = (0,255,0)): # Загружает файл картинки и подгоняет его под установленный размер фигуры внутри ячейки
        picture = pygame.image.load(file).convert()
        adjusted_picture = pygame.transform.scale(picture, (FIGURE_SIZE, FIGURE_SIZE))
        adjusted_picture.set_colorkey(colorkey)
        return adjusted_picture


    for black in ('p','r','h','b','q','k'):
        if black == 'p':
            black_pictures[black] = init_picture(folder + '/pawn_black.png')
        elif black == 'r':
            black_pictures[black] = init_picture(folder + '/rook_black.png')
        elif black == 'h':
            black_pictures[black] = init_picture(folder + '/knight_black.png')
        elif black == 'b':
            black_pictures[black] = init_picture(folder + '/bishop_black.png')
        elif black == 'q':
            black_pictures[black] = init_picture(folder + '/queen_black.png')
        elif black == 'k':
            black_pictures[black] = init_picture(folder + '/king_black.png')
    for white in ('p','r','h','b','q','k'):
        if white == 'p':
            white_pictures[white] = init_picture(folder + '/pawn_white.png')
        elif white == 'r':
            white_pictures[white] = init_picture(folder + '/rook_white.png')
        elif white == 'h':
            white_pictures[white] = init_picture(folder + '/knight_white.png')
        elif white == 'b':
            white_pictures[white] = init_picture(folder + '/bishop_white.png')
        elif white == 'q':
            white_pictures[white] = init_picture(folder + '/queen_white.png')
        elif white == 'k':
            white_pictures[white] = init_picture(folder + '/king_white.png')


def init_chess_field(surface): # 
    grid = 1
    grid_colors = ((200, 200, 200), (50, 50, 50))
    for x in range(8):
        for y in range(8):
            grid +=1
            pygame.draw.rect(surface, grid_colors[grid%2],(CELL_SIZE*x,CELL_SIZE*y, CELL_SIZE, CELL_SIZE),0)
        grid +=1
    pygame.draw.rect(surface,(0,0,0), (0,0,FIELD_LENGTH,FIELD_LENGTH), 1)

def reset():
    global selected, selected_figure, selected_cell
    selected = False
    selected_figure = None
    selected_cell = None


SIZE_X, SIZE_Y = 640, 480
FPS = 30
COLOR_BACKGROUND = 255, 255, 255
COLOR_TEXT = 0, 0, 0
COLOR_YELLOW = 220, 220, 0
COLOR_RED = 220, 0, 0
COLOR_GREEN = 0, 220, 0
CELL_SIZE = 40
FIGURE_SIZE = 30
FIELD_START_POS = 5, 5
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
black_figures = [[j,i] for j in range(8) for i in range(2)]
white_figures = [[j,i] for j in range(8) for i in range(6,8)]
admissible_positions = []
selected_cell, selected_figure = None, None
game = True
selected = False
black_step, white_step = False, True
white_check, black_check = False, False
white_checkmate, black_checkmate = False, False
pygame.init()
pygame.display.set_caption('CHESS')
screen = pygame.display.set_mode((SIZE_X, SIZE_Y)) # pygame.DOUBLEBUF
print(dir(screen))
field_screen = pygame.Surface((FIELD_LENGTH, FIELD_LENGTH))
init_chess_field(field_screen)
clock = pygame.time.Clock()
black_pictures = {}
white_pictures = {}
init_pictures()
text_font = pygame.font.SysFont('arial', 24)
checkmate_font = pygame.font.SysFont('arial', 42)
while not (white_checkmate or black_checkmate) and game:
    clock.tick(FPS)
    screen.fill(COLOR_BACKGROUND)
    screen.blit(field_screen, FIELD_START_POS)
    if selected:
        draw_admissible()
        pygame.draw.rect(screen, COLOR_GREEN, (selected_cell[0]*CELL_SIZE + FIELD_START_POS[0],selected_cell[1]*CELL_SIZE + FIELD_START_POS[1],CELL_SIZE,CELL_SIZE), 3)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
            break
        elif event.type == pygame.KEYDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x = ((pygame.mouse.get_pos()[0] - FIELD_START_POS[0]) // CELL_SIZE)
                y = ((pygame.mouse.get_pos()[1] - FIELD_START_POS[1]) // CELL_SIZE)
                selected_cell = [x, y]
                if selected_cell in white_figures and white_step:
                    selected_figure = selected_cell[:]
                    admissible_positions = check_positions(selected_figure[:], white_figures, black_figures,field)
                    admissible_positions = exclude_check_unprotected(field[selected_figure[1]][selected_figure[0]], selected_figure[:], admissible_positions, white_figures, black_figures, field)
                    selected = True
                elif selected_cell in black_figures and black_step:
                    selected_figure = selected_cell[:]
                    admissible_positions = check_positions(selected_figure[:], black_figures, white_figures, field)
                    admissible_positions = exclude_check_unprotected(field[selected_figure[1]][selected_figure[0]], selected_figure[:], admissible_positions, black_figures, white_figures, field)
                    selected = True
                else:
                    if selected_figure != None and white_step: # Если выбрана фигура и ячейка
                        if selected_cell in black_figures and selected_cell in admissible_positions:
                            take_figure(white_figures, black_figures)
                            black_check = check_shah(black_figures, white_figures, field)
                            #white_check = check_shah(white_figures, black_figures, field)
                            black_checkmate = check_checkmate(black_figures, white_figures, field)
                            #white_checkmate = check_checkmate(white_figures, black_figures, field)
                            selected,selected_figure,selected_cell = False, None, None
                            if black_checkmate or white_checkmate:
                                reset()
                                break
                        elif selected_cell in admissible_positions:
                            move_figure(white_figures)
                            black_check = check_shah(black_figures, white_figures, field)
                            #white_check = check_shah(white_figures, black_figures, field)
                            black_checkmate = check_checkmate(black_figures, white_figures, field)
                            #white_checkmate = check_checkmate(white_figures, black_figures, field)
                            selected,selected_figure,selected_cell = False, None, None
                            if black_checkmate or white_checkmate:
                                reset()
                                break
                        else:
                            reset()
                    elif selected_figure != None and black_step:
                        if selected_cell in white_figures and selected_cell in admissible_positions:
                            take_figure(black_figures, white_figures)
                            #white_check = check_shah(white_figures, black_figures, field)
                            black_check = check_shah(black_figures, white_figures, field)
                            selected,selected_figure,selected_cell = False, None, None
                        elif selected_cell in admissible_positions:
                            move_figure(black_figures)
                            #white_check = check_shah(white_figures, black_figures, field)
                            black_check = check_shah(black_figures, white_figures, field)
                            selected,selected_figure,selected_cell = False, None, None
                        else:
                            reset()
            elif event.button == 3:
                x = (pygame.mouse.get_pos()[0] // CELL_SIZE) * CELL_SIZE + 5
                y = (pygame.mouse.get_pos()[1] // CELL_SIZE) * CELL_SIZE + 5
                if [x,y] in white_figures and white_step:
                    reset()
                elif [x,y] in black_figures and black_step:
                    reset()

    step_white = text_font.render('white step: ' + str(white_step), 0, COLOR_TEXT)
    step_black = text_font.render('black step: ' + str(black_step), 0, COLOR_TEXT)
    check_white = text_font.render('white check: ' + str(white_check), 0, COLOR_TEXT)
    check_black = text_font.render('black check: ' + str(black_check), 0, COLOR_TEXT)
    fps = text_font.render('fps: ' + str(int(clock.get_fps())), 0, COLOR_TEXT)
    screen.blit(step_white,(410, 20))
    screen.blit(step_black,(410, 50))
    screen.blit(check_white,(410, 100))
    screen.blit(check_black, (410, 130))
    screen.blit(fps,(410, 180))
    draw_figures()
    pygame.display.flip()

if black_checkmate or white_checkmate:
    text = 'Black wins!' if white_check else 'White wins!'
    checkmate = checkmate_font.render(text, 0, COLOR_TEXT)
    screen.blit(checkmate, (40, 420))
    pygame.display.flip()
    pygame.time.delay(10000)
pygame.quit()

#  print(pygame.mouse.get_pos()) позиция мыши
#  rint(event.buttons[0]) нажата ли левая кнопка мыши
# pygame.MOUSEMOTION - event.buttons = (0,0,0)
# pygame.MOUSEBUTTONDWON - event.button = 1,2...5
# text_font = pygame.font.Font(FONT_FILE, 24)
# score_text = text_font.render('score:{: >3}'.format(int(score)),0,TEXT_COLOR)
# screen.blit(score_text, (tetris_len_x+10,240))
