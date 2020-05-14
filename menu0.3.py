import pygame
import pygame_gui


def init_field_screen(grid = False):
    grid_colors = [(200,200,200),(50,50,50)]
    CELL = 40
    s = 0
    c_x = field_screen.get_width()//CELL
    c_y = field_screen.get_height()//CELL
    for y in range(c_y):
        for x in range(c_x):
            pygame.draw.rect(field_screen, grid_colors[s%2], (x*CELL, y*CELL,CELL,CELL),0)
            s +=1
        s+=1


pygame.init()
X, Y = 640,480
field_screen = pygame.Surface((X,Y))
init_field_screen()
        
pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((X, Y)) #'data/themes/quick_theme.json'
manager = pygame_gui.UIManager((X, Y))

#background = pygame.Surface((800, 600))
#background.fill(manager.ui_theme.get_colour('dark_bg'))



panel1 = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((120, 80), (400, 320)),manager = manager,starting_layer_height=1)
dialog = pygame_gui.windows.UIConfirmationDialog(rect = pygame.Rect((10,10),(200,200)), manager = manager,action_long_desc='KOKO', window_title = 'Ready for fuck?')
msg = pygame_gui.windows.UIMessageWindow(rect = pygame.Rect((100,100),(300,300)), manager = manager,html_message='Is yer mom about?')
#panel2 = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((200, 200), (200, 400)),manager = manager,starting_layer_height=0)
play_with_computer_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (380, 40)), text='Play with computer', manager=manager, parent_element=panel1,container = panel1)
play_offline_button =       pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 60), (380, 40)), text='Play offline', manager=manager, parent_element=panel1,container = panel1)
play_online_button =        pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 110), (380, 40)), text='Play online', manager=manager, parent_element=panel1,container = panel1)
play_settings_button =      pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 160), (380, 40)), text='Settings', manager=manager, parent_element=panel1,container = panel1)
play_qut_button =           pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 260), (380, 40)), text='Quit game', manager=manager, parent_element=panel1,container = panel1)
clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = pygame

        if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_element == hello_button):
            print('Hello World!')

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(field_screen, (0, 0))
    manager.draw_ui(window_surface)
    
    pygame.display.update()
