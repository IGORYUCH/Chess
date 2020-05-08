import pygame
import pygame_menu
from random import randint
#import pygameMenu
X, Y = 640, 480
FPS = 30
COLOR_BACKGROUND = (128, 230, 198)
CELL_SIZE = 40
pygame.init()
screen = pygame.display.set_mode((X, Y))
pygame.display.flip()
screen.fill([255,255,255])
s = pygame.font.SysFont('arial',34)
#menu = pygameMenu.TextMenu(screen, 200, 200,'arial', "Fucker",Bgfun = None)
pygame.display.set_caption('CHESS')
game = True
selected_cell = [0,0]
selected = False
black_figures = []
white_figures = []
x,y = 0,0

def init_field_screen(grid = False):
    grid_colors = [(200,200,200),(50,50,50)]
    CELL = 40
    s = 0
    c_x = field_screen.get_width()//CELL
    c_y = field_screen.get_height()//CELL
    START_X = 5
    START_Y = 5
    for y in range(c_y):
        for x in range(c_x):
            pygame.draw.rect(field_screen, grid_colors[s%2], (x*CELL, y*CELL,CELL,CELL),0)
            s +=1
        s+=1

    
field_screen = pygame.Surface((640,480))
init_field_screen()
screen.blit(field_screen,(x,y))
##field_screen.get_alpha = 23
field = f = [[0 for i in range(10)] for j in range(10)]

knight = pygame.image.load('chess_knight.jpg').convert()

scaled_knight = pygame.transform.scale(knight,(int(knight.get_width()/15), int(knight.get_height()/15)))

##knight = pygame.image.load('chess_knight.jpg').conert() Переводит формат кодирования пикселей в формат главной поповерхности (Типо быстрее)
##knight.set_colorkey((0,0,0)) # Указанный цвет изображения как альфа канал
##knight_rect = knight.get_rect(bottomright = (1000,0))
def draw_grid():
    start = [5,5]
    for cells_x in range(10):
        for cells_y in range(10):
            pygame.draw.rect(screen,(0,0,0),(start[0] + CELL_SIZE*cells_x, start[1] + CELL_SIZE*cells_y, CELL_SIZE, CELL_SIZE),1)

def change_difficulty(*args):
    print(args)
    pygame.draw.rect(screen,(randint(0,255),randint(0,255),randint(0,255)), (randint(0,640),randint(0,480),5,5),0)

def start_the_game():
    screen.fill((255,255,255))
    x = 0
    y = 0
    for x,y in zip(range(X),range(Y)):
        pygame.time.delay(2)
        pygame.draw.rect(screen,(randint(0,255),randint(0,255),randint(0,255)), (x,y,20,20),0)
        pygame.display.flip()
    screen.blit(field_screen,(x,y))
    pygame.display.flip()
    

def quit1():
    x,y  = menu._pos_x, menu._pos_y
    menu_pos_x = 5
    menu._pos_y = 5
    menu.reset()
    pygame.time.delay(2000)
    menu._pos_x = x
    menu._pos_y = y
    menu.reset()
    
    
    


menu = pygame_menu.Menu(300, 400, 'v0.5.2', theme=pygame_menu.themes.THEME_DEFAULT)
#menu.add_text_input('Name: ',default='John Joe')
#menu.add_selector('Difficulty: ', [('Hard',2), ('Easy',2),('NIGHTMARE',999)], onchange=change_difficulty)
menu.add_button('Play offline', start_the_game)
menu.add_button('Play offline',start_the_game)
menu.add_button('Settings',start_the_game)
menu.add_button('Quit', quit1) #
menu.mainloop(screen)
while game:
    x += randint(-2,2)
    y += randint(-2,2)
    pygame.time.delay(100)
    screen.fill([255,255,255])
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
                selected = True
    draw_grid()
    screen.blit(field_screen,(x,y))
    pygame.display.flip()
pygame.quit()
                


#  print(pygame.mouse.get_pos()) позиция мыши
#  rint(event.buttons[0]) нажата ли левая кнопка мыши

# pygame.MOUSEMOTION - event.buttons = (0,0,0)
# pygame.MOUSEBUTTONDWON event.button = 1,2...5


['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__',
 '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__',
 '__subclasshook__', '__weakref__', '_append_widget', '_auto_center_content', '_back', '_background_function', '_build_widget_surface', '_check_id_duplicated',
 '_clock', '_close', '_column_max_width', '_column_pos_x', '_column_widths', '_columns', '_configure_widget', '_current', '_draw_focus_widget', '_enabled', '_exit',
 '_filter_widget_attributes', '_force_fit_text', '_get_depth', '_get_input_data', '_get_widget_max_position', '_handle_joy_event', '_height', '_id', '_index', '_joy_event',
 '_joy_event_down', '_joy_event_left', '_joy_event_repeat', '_joy_event_right', '_joy_event_up', '_joystick', '_left', '_menubar', '_mouse', '_mouse_motion_selection', '_mouse_visible',
 '_mouse_visible_default', '_onclose', '_open', '_pos_x', '_pos_y', '_prev', '_right', '_rows', '_scroll', '_select', '_sounds', '_submenus', '_theme', '_top', '_update_column_width',
 '_update_widget_position', '_widget_offset', '_widgets', '_widgets_surface', '_width', 'add_button', 'add_color_input', 'add_image', 'add_label', 'add_selector', 'add_text_input',
 'add_vertical_margin', 'center_content', 'clear', 'disable', 'draw', 'enable', 'full_reset', 'get_current', 'get_id', 'get_index', 'get_input_data', 'get_rect',
 'get_selected_widget', 'get_title', 'get_widget', 'is_enabled', 'mainloop', 'remove_widget', 'reset', 'set_relative_position', 'set_sound', 'toggle', 'update']
