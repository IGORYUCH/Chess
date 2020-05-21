import pygame
import pygame_gui
from random import randrange as r
from webbrowser import open_new_tab

def init_background(surface, cell_size = 50):
    grid_colors = [(200,200,200),(50,50,50)]
    s = 0
    c_x = surface.get_width()//cell_size
    c_y = surface.get_height()//cell_size
    for y in range(c_y):
        for x in range(c_x):
            pygame.draw.rect(surface, grid_colors[s%2], (x*cell_size, y*cell_size,cell_size,cell_size),0)
            s +=1
        s+=1


def play():
##    global main_menu
##    main_menu.window.kill()
    #window_surface.fill((r(255),r(255),0))
##    gamewindow  = pygame_gui.elements.ui_window.UIWindow(rect = pygame.Rect(0,0,800,600),manager = ui_manager, window_display_title = 'alert window')
##    gamewindow.set_blocking(True)
##    label = pygame_gui.elements.UILabel(relative_rect = pygame.Rect(5,5,100,100),text = 'been alerted',manager = ui_manager,container = gamewindow)
##    ok_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(30,40,100,20),text='OK', manager=ui_manager,container=gamewindow)
    game = True
    window_surface.fill((128,128,128))
    while game:
        time_delta = clock.tick(60)/1000.0
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
                    show_alert('Are you sure you want to exit?', pygame_gui.UIManager((800, 600)))
                    return
            #ui_manager.process_events(event)
        #ui_manager.update(time_delta)
        #ui_manager.draw_ui(window_surface)
        pygame.display.update()
##    main_window = MainMenu()

def play2():
    game = True
    gamewindow  = pygame_gui.elements.ui_window.UIWindow(rect = pygame.Rect(0,0,800,600),manager = ui_manager, window_display_title = 'alert window')
    quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(30,40,100,20),text='OK', manager=ui_manager,container=gamewindow)
    gamewindow.set_blocking(True)
    while game:
        window_surface.fill((r(255),0,0))
        
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == 'window.#close_button':
                print('on close')
            print('AAAA',event,event.type)
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event,event.type)
            gamewindow.ui_manager.process_events(event)
##            #print(event)
        gamewindow.ui_manager.update(time_delta)
##        ui_manager.draw_ui(window_surface)
        gamewindow.ui_manager.draw_ui(window_surface)
        pygame.display.update()
    
def show_alert(message, manager):    
    accepted = False
    alert = pygame_gui.windows.UIMessageWindow(pygame.Rect(100,100,300,200),html_message = message,manager= manager)
    alert.dismiss_button.set_text('OK')
    alert.set_blocking(True)
    
    while not accepted:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if alert.dismiss_button.pressed:
                accepted = True
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(window_surface)
        pygame.display.update()
    alert.kill()
    print('alerted')

def show_settings_menu(manager):
    back = False
    settings_menu = SettingsMenu(250,100, manager)
    settings_menu.window.set_blocking(True)
    while not back:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == settings_menu.back_button:
                        back = True
            manager.process_events(event)
        manager.update(time_delta)
        window_surface.blit(background_surface, (0,0))
        manager.draw_ui(window_surface)
        pygame.display.update()
    settings_menu.window.kill()
        


def show_confirm():
    pass


class SettingsMenu():

#bot difficulty easy,medium,hard,nightmare
#server ip adress 192.168.0.1
#server port 6666
#nickname big_ass
#cell black color(RGB) (0,0,0)
#cell white color(RGB) (255,255,255)
#show cell hints Yes,No
#
    def __init__(self,startX,startY,manager):
        self.window = pygame_gui.elements.ui_window.UIWindow(rect = pygame.Rect(startX,startY,300,400),
                                                             manager = manager,
                                                             window_display_title = 'Settings')
        self.back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(5,5,100,20),
                                                         text='back',
                                                         manager=manager,
                                                        container=self.window)
        self.bot_difficulty_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(5, 50, 120, 20),
                                                                text='Bot difficulty',
                                                                manager=manager,
                                                                container = self.window)
        print(dir(self.bot_difficulty_label.bg_colour))
        self.bot_difficulty_drop_down_menu = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(140,50, 100, 30),
                                               manager=manager, options_list=['Easy', 'Medium', 'Hard'],
                                               starting_option='Easy',container = self.window)

        self.ip_address_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(5, 80, 120, 20),
                                                                text='Server IP',
                                                                manager=manager,
                                                                container = self.window)
        self.ip_adress_line = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect(140, 80, 100, 20),
                                                                manager=manager,
                                                                container = self.window)
        self.port_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(5, 110, 120, 20),
                                                                text='Server port',
                                                                manager=manager,
                                                                container = self.window)
        self.port_line = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect(140, 110, 100, 20),
                                                                manager=manager,
                                                                container = self.window)
        self.nickname_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(5, 140, 120, 20),
                                                                text='Nickname',
                                                                manager=manager,
                                                                container = self.window)
        self.nickname_line = self.port_line = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect(140, 140, 100, 20),
                                                                manager=manager,
                                                                container = self.window)
        self.black_cell_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(5, 180, 120, 20),
                                                                text='Black cell',
                                                                manager=manager,
                                                                container = self.window)
        self.black_cell_line = self.port_line = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect(140, 180, 100, 20),
                                                                manager=manager,
                                                                container = self.window)
        self.white_cell_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(5, 220, 120, 20),
                                                                text='White cell',
                                                                manager=manager,
                                                                container = self.window)
        self.white_cell_line = self.port_line = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=pygame.Rect(140, 220, 100, 20),
                                                                manager=manager,
                                                                container = self.window)
        
        
        

    def save_changes(self):
        pass

    def restore_default(self):
        pass


class InGameMenu():
    pass


class MainMenu():
    
    def __init__(self, startX, startY):
        self.height = 40
        self.width = 180
        self.window = pygame_gui.elements.ui_window.UIWindow(rect = pygame.Rect(startX,startY,300,400),
                                                             manager = ui_manager,
                                                             window_display_title = 'Chess v0.6')
        self.play_online_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(40,10,self.width, self.height),
                                                         text='Play online',
                                                         manager=ui_manager,
                                                        container=self.window)

        self.play_offline_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(40,50,self.width, self.height),
                                                         text='Play offline',
                                                         manager=ui_manager,
                                                        container=self.window)
        self.play_with_bot_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(40,90,self.width, self.height),
                                                         text='Play with bot',
                                                         manager=ui_manager,
                                                        container=self.window)
        self.settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(40,130,self.width,self.height),
                                                        text='Settings',
                                                        manager=ui_manager,
                                                        container=self.window)
        self.rules_button = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(40,170,self.width,self.height),
                                                  text = 'Rules',
                                                  manager = ui_manager,
                                                  container = self.window)
        self.quit_button = pygame_gui.elements.UIButton(relative_rect = pygame.Rect(40,220,self.width,self.height),
                                                  text = 'Quit',
                                                  manager = ui_manager,
                                                  container = self.window)

pygame.init()
pygame.display.set_caption('Chess game')
window_surface = pygame.display.set_mode((800, 600))
background_surface = pygame.Surface((800, 600))
init_background(background_surface)
ui_manager = pygame_gui.UIManager((800, 600))
main_menu = MainMenu(250,100)
##text_box = pygame_gui.elements.UITextBox(html_text = 'enter some text',manager = ui_manager,relative_rect = pygame.Rect(30,60,100,20),container = window)
##entry_box = pygame_gui.elements.UITextBox(html_text = 'enter some text',manager = ui_manager,relative_rect = pygame.Rect(30,90,100,20),container = window)

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == main_menu.play_online_button:
                    print('AEFQ')
                    play()
                elif event.ui_element == main_menu.settings_button:
                    show_settings_menu(pygame_gui.UIManager((800, 600)))
                elif event.ui_element == main_menu.play_with_bot_button:
                    show_alert('Ar u sure?', pygame_gui.UIManager((800, 600)))
                elif event.ui_element == main_menu.play_offline_button:
                    pass
                elif event.ui_element == main_menu.rules_button:
                    open_new_tab('https://ru.wikipedia.org/wiki/%D0%9F%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0_%D1%88%D0%B0%D1%85%D0%BC%D0%B0%D1%82')
                elif event.ui_element == main_menu.quit_button:
                    is_running = False
        elif event.type ==  pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                pygame.draw.rect(window_surface,(r(255),r(255),r(255)),(x,y, 10,10),2)
                pygame.display.flip()
                pygame.time.delay(100)
        ui_manager.process_events(event)
    ui_manager.update(time_delta)
    window_surface.blit(background_surface,(0,0))
    ui_manager.draw_ui(window_surface)
    pygame.display.update()
pygame.quit()
