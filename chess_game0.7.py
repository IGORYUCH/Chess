import pygame
from random import randrange
from check_module import *

def draw_figures(): # Рисует изображения фигур на поверхности
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
            pygame.draw.rect(screen,
                             COLOR_RED,
                             (cell[0]*CELL_SIZE + FIELD_START_POS[0],
                              cell[1]*CELL_SIZE + FIELD_START_POS[1],
                              CELL_SIZE,
                              CELL_SIZE),
                             3)
        elif selected_figure in black_figures and cell in white_figures:
            pygame.draw.rect(screen, COLOR_RED,
                             (cell[0]*CELL_SIZE + FIELD_START_POS[0],
                              cell[1]*CELL_SIZE + FIELD_START_POS[1],
                              CELL_SIZE,
                              CELL_SIZE),
                             3)
        else:
            pygame.draw.rect(screen,
                             COLOR_YELLOW,
                             (cell[0]*CELL_SIZE + FIELD_START_POS[0],
                              cell[1]*CELL_SIZE + FIELD_START_POS[1],
                              CELL_SIZE,
                              CELL_SIZE),
                             3)
    

def take_figure(player_figures, opponent_figures, old_pos, new_pos): # Снимает атакуемую фигуру противника с поля и перемещает атакующую фигуру на ее место
    opponent_figures.remove(new_pos) # Удаляем фигуру у противника
    field[new_pos[1]][new_pos[0]] = field[old_pos[1]][old_pos[0]] # Перемещаем свою фигуру на место удаленной
    field[old_pos[1]][old_pos[0]] = ' ' # Очищаем клетку перемещенной фигуры
    player_figures[player_figures.index(old_pos)] = new_pos[:] # Меняем координаты выбранной фигуры на координаты выбранной ячейки


def move_figure(player_figures, old_pos, new_pos):
    field[new_pos[1]][new_pos[0]] = field[old_pos[1]][old_pos[0]] # Перемещаем фигуру на новое место
    field[old_pos[1]][old_pos[0]] = ' ' 
    player_figures[player_figures.index(old_pos)] = new_pos[:]


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
            pygame.draw.rect(surface,
                             grid_colors[grid%2],
                             (CELL_SIZE*x,
                              CELL_SIZE*y,
                              CELL_SIZE,
                              CELL_SIZE),
                             0)
        grid +=1
    pygame.draw.rect(surface,
                     (0,0,0),
                     (0,0,FIELD_LENGTH,FIELD_LENGTH),
                     1)

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
        pygame.draw.rect(screen, COLOR_GREEN,
                         (selected_cell[0]*CELL_SIZE + FIELD_START_POS[0],
                          selected_cell[1]*CELL_SIZE + FIELD_START_POS[1],
                          CELL_SIZE,
                          CELL_SIZE),
                         3)
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
                    admissible_positions = check_positions_white(selected_figure[:],
                                                                 white_figures,
                                                                 black_figures,
                                                                 field)
                    figure_type = field[selected_figure[1]][selected_figure[0]]
                    figure_pos = selected_figure[:]
                    admissible_positions = exclude_check_unprotected(figure_type,
                                                                     figure_pos,
                                                                     admissible_positions,
                                                                     white_figures,
                                                                     black_figures,
                                                                     check_positions_black,
                                                                     field)
                    selected = True
                elif selected_cell in black_figures and black_step:
                    selected_figure = selected_cell[:]
                    admissible_positions = check_positions_black(selected_figure[:],
                                                                 black_figures,
                                                                 white_figures,
                                                                 field)
                    figure_type = field[selected_figure[1]][selected_figure[0]]
                    figure_pos = selected_figure[:]
                    admissible_positions = exclude_check_unprotected(figure_type,
                                                                     figure_pos,
                                                                     admissible_positions,
                                                                     black_figures,
                                                                     white_figures,
                                                                     check_positions_white,
                                                                     field)
                    selected = True
                else:
                    if selected_figure != None and white_step: # Если выбрана фигура и ячейка
                        if selected_cell in black_figures and selected_cell in admissible_positions:
                            take_figure(white_figures, black_figures, selected_figure, selected_cell)
                            white_step, black_step = black_step, white_step
                            black_check = check_shah(black_figures,
                                                     white_figures,
                                                     check_positions_white,
                                                     field)
                            white_check = check_shah(white_figures, black_figures, check_positions_black, field)
                            black_checkmate = check_checkmate(black_figures,
                                                              check_positions_black,
                                                              white_figures,
                                                              check_positions_white,
                                                              field)
                            white_checkmate = check_checkmate(white_figures,
                                                              check_positions_white,
                                                              black_figures,
                                                              check_positions_black,
                                                              field)
                            selected,selected_figure,selected_cell = False, None, None
                            if black_checkmate or white_checkmate:
                                reset()
                                break
                        elif selected_cell in admissible_positions:
                            move_figure(white_figures, selected_figure, selected_cell)
                            white_step, black_step = black_step, white_step
                            black_check = check_shah(black_figures,
                                                     white_figures,
                                                     check_positions_white,
                                                     field)
                            white_check = check_shah(white_figures,
                                                     black_figures,
                                                     check_positions_black,
                                                     field)
                            black_checkmate = check_checkmate(black_figures,
                                                              check_positions_black,
                                                              white_figures,
                                                              check_positions_white,
                                                              field)
                            white_checkmate = check_checkmate(white_figures,
                                                              check_positions_white,
                                                              black_figures,
                                                              check_positions_black,
                                                              field)
                            selected,selected_figure,selected_cell = False, None, None
                            if black_checkmate or white_checkmate:
                                reset()
                                break
                        else:
                            reset()
                    elif selected_figure != None and black_step:
                        if selected_cell in white_figures and selected_cell in admissible_positions:
                            take_figure(black_figures, white_figures, selected_figure, selected_cell)
                            white_step, black_step = black_step, white_step
                            white_check = check_shah(white_figures,
                                                     black_figures,
                                                     check_positions_black,
                                                     field)
                            black_check = check_shah(black_figures,
                                                     white_figures,
                                                     check_positions_white,
                                                     field)
                            selected,selected_figure,selected_cell = False, None, None
                        elif selected_cell in admissible_positions:
                            move_figure(black_figures, selected_figure, selected_cell)
                            white_step, black_step = black_step, white_step
                            white_check = check_shah(white_figures,
                                                     black_figures,
                                                     check_positions_black,
                                                     field)
                            black_check = check_shah(black_figures,
                                                     white_figures,
                                                     check_positions_white,
                                                     field)
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
    c = checkmate_font.render(text, 0, COLOR_TEXT)
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
