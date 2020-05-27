from copy import deepcopy

def exclude_check_unprotected(figure, figure_cell, admissible, player_figures, opponent_figures, opponent_check, field):
    # Исключает из допустимых для хода ячеек поля те, которые не защищают короля от шаха
    new_admissible = deepcopy(admissible)
    for admissible_pos in admissible:
        player_figures_copy = deepcopy(player_figures)
        field_copy = deepcopy(field)
        field_copy[admissible_pos[1]][admissible_pos[0]] = figure
        field_copy[figure_cell[1]][figure_cell[0]] = ' '
        opponent_figures_copy = deepcopy(opponent_figures)
        if admissible_pos in opponent_figures:
            opponent_figures_copy.remove(admissible_pos)
        player_figures_copy[player_figures_copy.index(figure_cell)] = admissible_pos[:]
        future_check = check_shah(player_figures_copy,
                                  opponent_figures_copy,
                                  opponent_check,
                                  field_copy)
        if future_check:
            new_admissible.remove(admissible_pos)
    return new_admissible


def check_cell(cell, player_figures, field):
    if (0 <= cell[0] <= 7) and (0 <= cell[1] <= 7):
        if field[cell[1]][cell[0]] == ' ':
            return 1
        elif cell in player_figures:
            return 2
        else:
            return 0
    else:
        return 0


def check_shah(player_figures, opponent_figures, check_opponent, field):# Проверяет, бьет ли игрок короля своего оппонента
    admissible = []
    for player_figure in player_figures:
        if field[player_figure[1]][player_figure[0]] == 'k':
            player_king = player_figure[:]
            break
    for opponent_figure in opponent_figures:
        admissible = check_opponent(opponent_figure, opponent_figures, player_figures, field)
        if player_king in admissible:
            return True
    else:
        return False


def check_checkmate(player_figures, check_player, opponent_figures, check_opponent, field):
    for player_figure in player_figures:
        admissible = check_player(player_figure, player_figures, opponent_figures, field)
        admissible = exclude_check_unprotected(field[player_figure[1]][player_figure[0]],
                                               player_figure,
                                               admissible,
                                               player_figures,
                                               opponent_figures,
                                               check_opponent,
                                               field)
        if admissible:
            return False
    else:
        return True


def check_black_pawn(cell, opponent_figures, field):
    # Проверяет допустимые ячейки поля для хода пешкой
    admissible = []
    direction, start_pos = 1, 1
    if cell[1] == start_pos:
        for x,y in ([cell[0], cell[1] + 1*direction], [cell[0], cell[1] + 2*direction]):
            if check_cell([x, y], opponent_figures, field) == 1:
                admissible.append([x, y])
            else: break
    else:
        if check_cell((cell[0], cell[1] + 1*direction), opponent_figures, field) == 1:
            admissible.append([cell[0], cell[1] + 1*direction])
    if check_cell([cell[0] + 1, cell[1] + 1*direction], opponent_figures, field) == 2:
        admissible.append([cell[0] + 1, cell[1] + 1*direction])
    if check_cell([cell[0] - 1, cell[1] + 1*direction], opponent_figures, field) == 2:
        admissible.append([cell[0] - 1, cell[1] + 1*direction])
    return admissible


def check_white_pawn(cell, opponent_figures, field):
    # Проверяет допустимые ячейки поля для хода пешкой
    admissible = []
    direction, start_pos = -1, 6
    if cell[1] == start_pos:
        for x,y in ([cell[0], cell[1] + 1*direction], [cell[0], cell[1] + 2*direction]):
            if check_cell([x, y], opponent_figures, field) == 1:
                admissible.append([x, y])
            else: break
    else:
        if check_cell((cell[0], cell[1] + 1*direction), opponent_figures, field) == 1:
            admissible.append([cell[0], cell[1] + 1*direction])
    if check_cell([cell[0] + 1, cell[1] + 1*direction], opponent_figures, field) == 2:
        admissible.append([cell[0] + 1, cell[1] + 1*direction])
    if check_cell([cell[0] - 1, cell[1] + 1*direction], opponent_figures, field) == 2:
        admissible.append([cell[0] - 1, cell[1] + 1*direction])
    return admissible


def check_king(cell, opponent_figures, field):
    # Проверяет допустимые поля ячейки для хода королем
    admissible = []
    for x, y in ([-1,-1], [0,-1], [1,-1], [1,0], [1,1], [0,1], [-1,1], [-1,0]):
        if check_cell([cell[0] + x, cell[1] + y], opponent_figures, field):
            admissible.append([cell[0] + x, cell[1] + y])
    return admissible


def check_bishop(cell, opponent_figures, field):
    # Проверяет допустимые ячейки поля для хода ладьей
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


def check_knight(cell, opponent_figures, field): #
    #Проверяет допустимые ячейки поля для хода конем
    admissible = []
    for x,y in ([1, -2], [2, -1], [2, 1], [1, 2], [-1, 2], [-2, 1], [-2, -1], [-1, -2]):
        if check_cell([cell[0] + x, cell[1] + y], opponent_figures, field):
            admissible.append([cell[0] + x, cell[1] + y])
    return admissible


def check_rook(cell, opponent_figures, field):
    # Проверяет допустимые ячейки поля для хода ладьей
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


def check_queen(cell, opponent_figures, field):
    # Проверяет допустимые ячейки поля для хода ферзем
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


def check_positions_black(cell, player_figures, opponent_figures, field):
    # Проверяет допустимые ячейки поля для хода фигуры в зависимости от ее типа
    admissible = []
    figure = field[cell[1]][cell[0]]
    if figure == 'p':
        admissible = check_black_pawn(cell, opponent_figures, field)
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


def check_positions_white(cell, player_figures, opponent_figures, field):
    # Проверяет допустимые ячейки поля для хода фигуры в зависимости от ее типа
    admissible = []
    figure = field[cell[1]][cell[0]]
    if figure == 'p':
        admissible = check_white_pawn(cell, opponent_figures, field)
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
