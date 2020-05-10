import pygame
import pygame_menu
from random import randint
import easygui as ui
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
    screen.blit(field_screen,(0,0))
    pygame.display.flip()

def draw_rect():
    pygame.draw.rect(screen,(0,0,0), menu.get_rect(),5)
def draw_rect2():
    pygame.draw.rect(screen, (0,0,0), dialog.get_rect(),5)   


def play_offline():
    def draw_rect2():
        pygame.draw.rect(screen, (0,0,0), dialog.get_rect(),5)   


    


    def ok():
        ui.msgbox('agreed')
        dialog.toggle()
        menu.toggle()
    def cancel():
         ui.msgbox('canceled')
         dialog.toggle()
         menu.toggle()
        
        
    menu.toggle()
    dialog = pygame_menu.Menu(200, 410, 'confirm',theme=pygame_menu.themes.THEME_DEFAULT,columns = 3,rows = 2)
    dialog.add_label('_____')
    dialog.add_button('Ok', ok, align=pygame_menu.locals.ALIGN_RIGHT)
    dialog.add_label('Are you sure?',align=pygame_menu.locals.ALIGN_CENTER)
    dialog.add_label('_')
    dialog.add_label('_______',align=pygame_menu.locals.ALIGN_RIGHT)
    dialog.add_button('Cancel',cancel,align=pygame_menu.locals.ALIGN_LEFT)
    dialog.mainloop(screen,draw_rect2)

def quit_chess():
    def draw_rect2():
        pygame.draw.rect(screen, (0,0,0), dialog.get_rect(),5)   


    


    def ok():
        ui.msgbox('agreed')
        dialog.toggle()
        menu.toggle()

        
    def cancel():
         ui.msgbox('canceled')
         dialog.toggle()
         menu.toggle()
        
        
    menu.toggle()
    dialog = pygame_menu.Menu(200, 410, 'confirm',theme=pygame_menu.themes.THEME_DEFAULT,columns = 3,rows = 2)
    dialog.add_label('     ')
    dialog.add_button('Ok', ok, align=pygame_menu.locals.ALIGN_RIGHT)
    dialog.add_label('Are you sure?',align=pygame_menu.locals.ALIGN_CENTER)
    dialog.add_label(' ')
    dialog.add_label('       ',align=pygame_menu.locals.ALIGN_RIGHT)
    dialog.add_button('Cancel',cancel,align=pygame_menu.locals.ALIGN_LEFT)
    dialog.mainloop(screen,draw_rect2)
    
    

def settings_menu():

    def do_nothing(a):
        ui.msgbox('Nothing happened in ' + str(a))

    def go_back():
        s_menu.toggle()
        menu.toggle()
        
    menu.toggle()
    s_menu = pygame_menu.Menu(400, 400, 'Settings',
                              theme=pygame_menu.themes.THEME_DEFAULT)
    s_menu.add_button('setting 0', do_nothing,0,align=pygame_menu.locals.ALIGN_LEFT)
    s_menu.add_button('setting 1', do_nothing,1,align=pygame_menu.locals.ALIGN_LEFT)
    s_menu.add_button('setting 2', do_nothing,2,align=pygame_menu.locals.ALIGN_LEFT)
    s_menu.add_button('setting 3', do_nothing,3,align=pygame_menu.locals.ALIGN_LEFT)
    s_menu.add_button('setting 4', do_nothing,4,align=pygame_menu.locals.ALIGN_LEFT)
    s_menu.add_button('setting 5', do_nothing,5,align=pygame_menu.locals.ALIGN_LEFT)
    s_menu.add_button('setting 6', do_nothing,6,align=pygame_menu.locals.ALIGN_LEFT)
    s_menu.add_button('setting 7', do_nothing,7,align=pygame_menu.locals.ALIGN_LEFT)
    s_menu.add_button('back', go_back)
    s_menu.mainloop(screen)
    
theme1 = pygame_menu.themes.THEME_DEFAULT.copy()

##theme1.title_background_color = (220,20,220)
#theme1.title_font_color = (0,0,0)
theme1.title_font_color = (0,0,0)
theme1.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE
# pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE_TITLE
# 
menu = pygame_menu.Menu(onclose=pygame_menu.events.DISABLE_CLOSE,height = 400, title = 'Chess v0.5.2', width = 400,theme = theme1)
#menu.add_text_input('Name: ',default='John Joe')
#menu.add_selector('Difficulty: ', [('Hard',2), ('Easy',2),('NIGHTMARE',999)], onchange=change_difficulty)
#s_menu.add_button('setting 7', do_nothing,7,align=pygame_menu.locals.ALIGN_LEFT) aligned to left widget
#main_menu.mainloop(surface, main_background, disable_loop=test, fps_limit=FPS) main_background - выполняется на фоне

menu.add_button('Play with computer',start_the_game)
menu.add_button('Play online', start_the_game)
menu.add_button('Play offline',play_offline)
menu.add_button('Settings', settings_menu)
menu.add_label('Sometext',label_id='213')
menu.add_button('Quit', pygame_menu.events.EXIT) #
menu.get_widget('213').set_background_color((0,0,240))
#print(dir(menu.get_widget("213")))
menu.mainloop(screen,draw_rect)
#menu.toggle() # Switch disabled\enabled
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
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
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
