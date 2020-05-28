import pygame
import pygame_gui
import socket
import rsa
import threading
from copy import deepcopy
from random import randrange as r
from random import choice
from webbrowser import open_new_tab
import json

def err_handler(function):
    def wrapper(*args,**kwargs):
        try:
            result = function(*args,**kwargs)
            return result
        except Exception as err:
            add_str('An error occured in ', function.__name__)
            show_alert('An error occured. Check error_log.txt', pygame_gui.UIManager((SIZE_X, SIZE_Y)))
            with open('error_log.txt','a') as err_file:
                err_file.write('[' + ctime() + '] ' + 'in' + function.__name__ + ' ' + str(err.args) + '\n')
    return wrapper


def init_background(surface, cell_size = 50):
    grid_colors = [(200,200,200),(50,50,50)]
    s = 0
    c_x = surface.get_width()//cell_size
    c_y = surface.get_height()//cell_size
    for y in range(c_y):
        for x in range(c_x):
            pygame.draw.rect(surface, grid_colors[s%2], (x*cell_size, y*cell_size, cell_size, cell_size), 0)
            s +=1
        s+=1


def play_offline():
    game = True
    window_surface.fill((128,128,128))
    text_font = pygame.font.SysFont('arial', 24)
    escape_text = text_font.render('Press ESCAPE to run menu', 0, (0,0,0))
    while game:
        time_delta = clock.tick(FPS)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    pygame.draw.rect(window_surface,(r(255),r(255),r(255)),(x,y, 10,10),0)
                elif event.button == 3:
                    pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    should_exit = show_in_game_menu(pygame_gui.UIManager((SIZE_X, SIZE_Y)))
                    if should_exit:
                        return
        window_surface.blit(escape_text, (5,5))
        pygame.display.update()


def play_with_bot():
    pass

def play_online(sock):
    
    def draw_figures(screen): # Рисует изображения фигур на поверхности
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


    black_pictures = {}
    white_pictures = {}
    field_screen = pygame.Surface((FIELD_LENGTH, FIELD_LENGTH))
    init_chess_field(field_screen)
    init_pictures()
    black_figures = [[j,i] for j in range(8) for i in range(2)]
    white_figures = [[j,i] for j in range(8) for i in range(6,8)]
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

    game = True
    window_surface.fill((128,128,128))
    pygame.display.flip()
    selected_cell = [100,100]
    admissible = []
    text_font = pygame.font.SysFont('arial', 18)
    status_text = text_font.render('STATUS TEXT', 0, (0,0,0))
    while game:
        time_delta = clock.tick(FPS)/1000.0
        window_surface.blit(field_screen, FIELD_START_POS)
        draw_figures(window_surface)
        if selected_cell != [100,100]:
            pygame.draw.rect(window_surface, (0,255,0),
                         (selected_cell[0]*CELL_SIZE + FIELD_START_POS[0],
                          selected_cell[1]*CELL_SIZE + FIELD_START_POS[1],
                          CELL_SIZE,
                          CELL_SIZE),
                         3)
        for x,y in admissible:
            pygame.draw.rect(window_surface,
                             (255,255,0),
                             (x*CELL_SIZE + FIELD_START_POS[0],
                              y*CELL_SIZE + FIELD_START_POS[1],
                              CELL_SIZE,
                              CELL_SIZE),
                             3)
        for event2 in sock.get_events():
            if event2['type'] == 'gameover':
                show_alert(event2['text'], pygame_gui.UIManager((SIZE_X, SIZE_Y)))
                game = False
            elif event2['type'] == 'move':
                selected_cell = [event2['x'], event2['y']]
            elif event2['type'] == 'msg':
                show_alert(event2['text'],  pygame_gui.UIManager((SIZE_X, SIZE_Y)))
            elif event2['type'] == 'admissible':
                admissible = deepcopy(event2['admissible_list'])
            elif event2['type'] == 'light':
                selected_cell = event2['cell'][:]
            elif event2['type'] == 'msg':
                status_text = text_font.render(event2['text'], 0, (0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = ((pygame.mouse.get_pos()[0] - FIELD_START_POS[0]) // CELL_SIZE)
                y = ((pygame.mouse.get_pos()[1] - FIELD_START_POS[1]) // CELL_SIZE)
                sock.send_data('SELECT ' + str(x) + ' ' + str(y))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    should_exit = show_in_game_menu(pygame_gui.UIManager((SIZE_X, SIZE_Y)))
                    if should_exit:
                        sock.socket.close()
                        game = False
        window_surface.blit(status_text,(5,450))
        pygame.display.flip()


def play_online_menu(manager):
    window_copy = window_surface.copy()
    i = False
    server_menu = ServerMenu(250,100,manager)
    server_menu.window.set_blocking(True)
    player_socket = PlayerSocket(ADDRESS, PORT, KEYLEN, server_menu)
    player_socket.start()
    while not i:
        time_delta = clock.tick(FPS)/1000.0
        for event2 in player_socket.get_events():
            if event2['type'] == 'gamebegin':
                play_online(player_socket)
                i = True
            elif event2['type'] == 'msg':
                server_menu.text_label.set_text(event2['text'])
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == server_menu.accept_button:
                        player_socket.send_data('ACCEPT')
                        server_menu.text_label.set_text('Game Accepted')
                        server_menu.accept_button.disable()
                    elif event.ui_element == server_menu.cancel_button:
                        player_socket.socket.close()
                        i = True
            manager.process_events(event)
        manager.update(time_delta)
        window_surface.blit(window_copy, (0,0))
        manager.draw_ui(window_surface)
        pygame.display.update()
    server_menu.window.kill()


def show_alert(message, manager):
    window_copy = window_surface.copy()
    accepted = False
    alert = pygame_gui.windows.UIMessageWindow(pygame.Rect(250,200,300,200),
                                               html_message = message,
                                               manager = manager)
    alert.dismiss_button.set_text('OK')
    alert.set_blocking(True)
    while not accepted:
        time_delta = clock.tick(FPS)/1000.0
        for event in pygame.event.get():
            if alert.dismiss_button.pressed:
                accepted = True
            manager.process_events(event)
        manager.update(time_delta)
        window_surface.blit(window_copy, (0,0))
        manager.draw_ui(window_surface)
        pygame.display.update()
    alert.kill()



def show_settings_menu(manager):
    back = False
    settings_menu = SettingsMenu(250,100, manager)
    settings_menu.window.set_blocking(True)
    while not back:
        time_delta = clock.tick(FPS)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == settings_menu.back_button:
                        settings_menu.save_changes()
                        back = True
                    elif event.user_type == settings_menu.restore_default_button:
                        settings_menu.restore_default()
            manager.process_events(event)
        manager.update(time_delta)
        window_surface.blit(background_surface, (0,0))
        manager.draw_ui(window_surface)
        pygame.display.update()
    settings_menu.window.kill()


def show_confirm(message, manager):
    window_copy = window_surface.copy()
    answer = None
    confirm = pygame_gui.windows.UIConfirmationDialog(pygame.Rect(250,200,300,200),
                                                      window_title = 'confirm',
                                                      action_long_desc= message,manager = manager)
    confirm.set_blocking(True)
    while answer == None:
        time_delta = clock.tick(FPS)/1000.0
        for event in pygame.event.get():
            if confirm.cancel_button.pressed:
                answer = False
            elif confirm.confirm_button.pressed:
                answer = True
            manager.process_events(event)
        manager.update(time_delta)
        window_surface.blit(window_copy,(0,0))
        manager.draw_ui(window_surface)
        pygame.display.update()
    confirm.kill()
    window_surface.blit(window_copy, (0,0))
    return answer


def show_in_game_menu(manager):
    window_copy = window_surface.copy()
    esc = False
    exit_answer = None
    in_game_menu = InGameMenu(250,100, manager)
    in_game_menu.window.set_blocking(True)
    while not esc and exit_answer == None:
        time_delta = clock.tick(FPS)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    esc = True
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == in_game_menu.return_to_game_button:
                        exit_answer = False
                    elif event.ui_element == in_game_menu.rules_button:
                        open_new_tab('https://ru.wikipedia.org/wiki/%D0%9F%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0_%D1%88%D0%B0%D1%85%D0%BC%D0%B0%D1%82')
                    elif event.ui_element == in_game_menu.quit_button:
                        if show_confirm('Are you shure? Game will be lost', pygame_gui.UIManager((SIZE_X, SIZE_Y))):
                            exit_answer = True
            manager.process_events(event)
        manager.update(time_delta)
        window_surface.blit(window_copy,(0,0))
        manager.draw_ui(window_surface)
        pygame.display.update()
    in_game_menu.window.kill()
    window_surface.blit(window_copy,(0,0))
    return exit_answer


class PlayerSocket(threading.Thread):

    def __init__(self,address, port, keylength, menu):
        threading.Thread.__init__(self)
        self.menu = menu
        self.address = address
        self.port = port
        self.xor_key = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.events = []

    def get_data(self):
        try:
            server_data = self.socket.recv(1024)
            if not server_data:
                print('system: disconnected by server')
                return False
        except ConnectionResetError:
            print('system: disconnected by server (connection reset)')
        except ConnectionAbortedError:
            print('system: disconnected by self')
            return False
        return self.xor_crypt(server_data, self.xor_key).decode('utf-8')

    def send_data(self, message):
        try:
            self.socket.send(self.xor_crypt(message.encode('utf-8'), self.xor_key))
            return True
        except ConnectionResetError:
            print('system: disconnected by server')
        except ConnectionAbortedError:
            print('system: disconnected by self')
            return False

    def run(self):
        connected = self.connect_to_server()
        while connected:
            server_data = self.get_data()
            if not server_data:
                break
            data_words = server_data.split(' ')
            if data_words[0] == 'MSG':
                self.events.append({'type':'msg','text':' '.join(data_words[1:])})
            elif data_words[0] == 'END':
                self.events.append({'type':'gameover','text':''.join(data_words[1:])})
            elif data_words[0] == 'ACCEPT':
                self.menu.text_label.set_text('Opponent accepted')
            elif data_words[0] == 'READY':
                self.menu.text_label.set_text('Game is ready, press "accept" to accept')
                self.menu.accept_button.enable()
            elif data_words[0] == 'GAME':
                self.events.append({'type':'gamebegin'})
            elif data_words[0] == 'CANCEL':
                self.menu.text_label.set_text(' '.join(data_words[1:]))
                self.menu.accept_button.disable()
            elif data_words[0] == 'ALERT':
                self.events.append({'type':'msg','text':' '.join(data_words[1:])})
            elif data_words[0] == 'LIGHT':
                print('msg',server_data,'splitted',data_words)
                self.events.append(
                    {'type':'light','cell':json.loads(''.join(data_words[1:]))
                     }
                    )
            elif data_words[0] == 'ADMISSIBLE':
                print('msg',server_data,'splitted',data_words)
                self.events.append(
                    {'type':'admissible',
                     'admissible_list':json.loads(''.join(data_words[1:]))
                     }
                    )
            print('server data', server_data)

    def get_events(self):
        events = deepcopy(self.events)
        self.events = []
        return events

    def connect_to_server(self):
        try:
            self.socket.connect((ADDRESS, PORT))
        except Exception as err:
            print(err.args)
            self.menu.text_label.set_text('Could not connect to server!')
            return False
        else:
            self.menu.text_label.set_text('Establishing secure connection')
            self.xor_key = bytes([choice(b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTYVWXYZ1234567890+/') for i in range(KEYLEN)])
            server_public_key_data = self.socket.recv(1024)
            server_key = rsa.PublicKey.load_pkcs1(server_public_key_data)
            encrypted_key = rsa.encrypt(self.xor_key, server_key)
            self.menu.text_label.set_text('Searching for players...')
            self.socket.send(encrypted_key)
            return True

    def xor_crypt(self, string:bytes, key:bytes) -> bytes:
        key_len = len(key)
        fitted_key = bytes(key[index % key_len] for index in range(len(string)))
        crypto_str = bytes([string[index] ^ fitted_key[index] for index in range(len(string))])
        return crypto_str


class ServerMenu():

    def __init__(self, startX, startY, manager):
        self.window = pygame_gui.elements.ui_window.UIWindow(rect = pygame.Rect(startX, startY, 300, 200),
                                                                manager = manager,
                                                                window_display_title = 'Online game mode')
        self.text_label = pygame_gui.elements.UILabel(relative_rect = pygame.Rect(5, 5, 260, 30),
                                                                text = 'Connecting to server...',
                                                                manager = manager,
                                                                container = self.window)
##        print(dir(self.text_label))
        self.accept_button = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(10,100,120,30),
                                                                text = 'Accept',
                                                                manager = manager,
                                                                container = self.window)
        self.cancel_button = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(135,100,120,30),
                                                                text = 'Cancel',
                                                                manager = manager,
                                                                container = self.window)
        self.accept_button.disable()


class SettingsMenu():

    def __init__(self, startX, startY, manager):
        self.window = pygame_gui.elements.ui_window.UIWindow(rect = pygame.Rect(startX, startY, 300, 400),
                                                                manager = manager,
                                                                window_display_title = 'Settings')
        self.back_button = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(5, 5, 100, 30),
                                                                text = 'Back',
                                                                manager = manager,
                                                                container = self.window)
        self.restore_default_button = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(120,5,140,30),
                                                                text = 'Restore default',
                                                                manager = manager,
                                                                container = self.window)
        self.bot_difficulty_label = pygame_gui.elements.UILabel(relative_rect = pygame.Rect(5, 55, 120, 20),
                                                                text = 'Bot difficulty',
                                                                manager = manager,
                                                                container = self.window)
        self.bot_difficulty_drop_down_menu = pygame_gui.elements.UIDropDownMenu(relative_rect = pygame.Rect(130,50, 120, 30),
                                                                manager = manager, options_list = ['Easy', 'Medium', 'Hard'],
                                                                starting_option = 'Easy',
                                                                container = self.window)
        self.ip_address_label = pygame_gui.elements.UILabel(relative_rect = pygame.Rect(5, 85, 120, 20),
                                                                text = 'Server IP',
                                                                manager = manager,
                                                                container = self.window)
        self.ip_adress_line = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect = pygame.Rect(130, 80, 120, 20),
                                                                manager = manager,
                                                                container = self.window)
        self.port_label = pygame_gui.elements.UILabel(relative_rect = pygame.Rect(5, 115, 120, 20),
                                                                text = 'Server port',
                                                                manager = manager,
                                                                container = self.window)
        self.port_line = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect = pygame.Rect(130, 110, 120, 20),
                                                                manager = manager,
                                                                container = self.window)
        self.nickname_label = pygame_gui.elements.UILabel(relative_rect = pygame.Rect(5, 145, 120, 20),
                                                                text='Nickname',
                                                                manager = manager,
                                                                container = self.window)
        self.nickname_line = self.port_line = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect = pygame.Rect(130, 140, 120, 20),
                                                                manager = manager,
                                                                container = self.window)
        self.black_cell_label = pygame_gui.elements.UILabel(relative_rect = pygame.Rect(5, 175, 120, 20),
                                                                text='Black cell RGB',
                                                                manager = manager,
                                                                container = self.window)
        self.black_cell_line = self.port_line = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect = pygame.Rect(130, 170, 120, 20),
                                                                manager = manager,
                                                                container = self.window)
        self.white_cell_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(5, 205, 120, 20),
                                                                text='White cell RGB',
                                                                manager = manager,
                                                                container = self.window)
        self.white_cell_line = self.port_line = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect = pygame.Rect(130, 200, 120, 20),
                                                                manager = manager,
                                                                container = self.window)
        self.cell_hints_label = pygame_gui.elements.UILabel(relative_rect = pygame.Rect(5, 235, 120, 20),
                                                                text = 'Cell hints',
                                                                manager = manager,
                                                                container = self.window)
        self.cell_hints_drop_down_menu = pygame_gui.elements.UIDropDownMenu(relative_rect = pygame.Rect(130, 230, 120, 30),
                                                                manager = manager, options_list = ['Yes', 'No'],
                                                                starting_option = 'Yes',
                                                                container = self.window)


    def save_changes(self):
        pass


    def restore_default(self):
        pass


class InGameMenu():

    def __init__(self, startX, startY, manager):
        self.height = 40
        self.width = 180
        self.window = pygame_gui.elements.ui_window.UIWindow(rect = pygame.Rect(startX, startY, 300, 300),
                                                                manager = manager,
                                                                window_display_title = 'Chess v0.7')
        self.return_to_game_button = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(40, 10, self.width, self.height),
                                                                text='Return to game',
                                                                manager = manager,
                                                                container = self.window)
        self.rules_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(40,50,self.width, self.height),
                                                                text='Rules',
                                                                manager = manager,
                                                                container = self.window)
        self.quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(40, 90, self.width, self.height),
                                                                text = 'Quit',
                                                                manager = manager,
                                                                container = self.window)


class MainMenu():

    def __init__(self, startX, startY, manager):
        self.height = 40
        self.width = 180
        self.window = pygame_gui.elements.ui_window.UIWindow(rect = pygame.Rect(startX, startY, 300, 400),
                                                                manager = manager,
                                                                window_display_title = 'Chess v0.7')
        self.play_online_button = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(40,10,self.width, self.height),
                                                                text='Play online',
                                                                manager = manager,
                                                                container = self.window)
        self.play_offline_button = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(40, 50, self.width, self.height),
                                                                text = 'Play offline',
                                                                manager = manager,
                                                                container = self.window)
        self.play_with_bot_button = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(40, 90, self.width, self.height),
                                                                text = 'Play with bot',
                                                                manager = manager,
                                                                container = self.window)
        self.settings_button = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(40, 130, self.width, self.height),
                                                                text = 'Settings',
                                                                manager = manager,
                                                                container = self.window)
        self.rules_button = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(40, 170, self.width, self.height),
                                                                text = 'Rules',
                                                                manager = manager,
                                                                container = self.window)
        self.quit_button = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(40, 220, self.width, self.height),
                                                                text = 'Quit',
                                                                manager = manager,
                                                                container = self.window)


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


VERSION = '0.7.4'
FPS = 60
SIZE_X, SIZE_Y = 800, 600
ADDRESS, PORT = '127.0.0.1', 6666
FIELD_START_POS = [5,5]
FIELD_LENGTH = 400
KEYLEN = 64
CELL_SIZE = int(FIELD_LENGTH/8)
MARGIN = 5
FIGURE_SIZE  = CELL_SIZE - MARGIN*2
FIGURE_START_POS = [FIELD_START_POS[0] + MARGIN, FIELD_START_POS[1] + MARGIN]
pygame.init()
pygame.display.set_caption('Chess game')
window_surface = pygame.display.set_mode((SIZE_X, SIZE_Y))
background_surface = pygame.Surface((SIZE_X, SIZE_Y))
init_background(background_surface)
ui_manager = pygame_gui.UIManager((SIZE_X, SIZE_Y))
main_menu = MainMenu(250, 100, ui_manager)
clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(FPS)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == main_menu.play_online_button:
                    play_online_menu(pygame_gui.UIManager((SIZE_X, SIZE_Y)))
                elif event.ui_element == main_menu.settings_button:
                    show_settings_menu(pygame_gui.UIManager((SIZE_X, SIZE_Y)))
                elif event.ui_element == main_menu.play_with_bot_button:
                    play_with_bot()
                elif event.ui_element == main_menu.play_offline_button:
                    play_offline()
                elif event.ui_element == main_menu.rules_button:
                    open_new_tab('https://ru.wikipedia.org/wiki/%D0%9F%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0_%D1%88%D0%B0%D1%85%D0%BC%D0%B0%D1%82')
                elif event.ui_element == main_menu.quit_button:
                    is_running = False
        ui_manager.process_events(event)
    ui_manager.update(time_delta)
    window_surface.blit(background_surface,(0,0))
    ui_manager.draw_ui(window_surface)
    pygame.display.update()
pygame.quit()
