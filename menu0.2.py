import pygame
import pygame_menu
from random import randint
import easygui as ui


def init_field_screen(grid = False):
    grid_colors = [(200,200,200),(50,50,50)]
    CELL = 40
    s = 0
    c_x = field_screen.get_width()//CELL
    c_y = field_screen.get_height()//CELL
    for y in range(c_y):
        for x in range(c_x):
            pygame.draw.rect(screen, grid_colors[s%2], (x*CELL, y*CELL,CELL,CELL),0)
            s +=1
        s+=1

def background():
    grid_colors = [(200,200,200),(50,50,50)]
    CELL = 40
    s = 0
    c_x = screen.get_width()//CELL
    c_y = screen.get_height()//CELL
    while True:
        for y in range(c_y):
            for x in range(c_x):
                pygame.draw.rect(screen, grid_colors[s%2], (x*CELL, y*CELL,CELL,CELL),0)
                s +=1
            s+=1
        yield s

def play_offline():
    stopped = False
    screen.fill((255,255,255))
    while not stopped:
        pygame.time.delay(100)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game = False
            elif event.type == pygame.KEYDOWN:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x1 = pygame.mouse.get_pos()[0]
                    y1 = pygame.mouse.get_pos()[1]
                    pygame.draw.rect(screen,(randint(0,255),0,randint(0,255)), (x1-5,y1-5,10,10),4)
                elif event.button == 3:
                    x1 = pygame.mouse.get_pos()[0]
                    y1 = pygame.mouse.get_pos()[1]
                    if x1 > 600 and y1 > 440:
                        if confirm_menu():
                            stopped = True
        pygame.display.flip()

def draw_rect(surface, rect, color = (0,0,0)):
    pygame.draw.rect(surface,(0,0,0), rect, 2)
    
def play_online():
    pass

def play_with_computer():
    pass
        
def alert():
    main_menu.toggle()
    
    pass

def settings_menu():
    pass


def on_game_menu():
    pass

def confirm_menu():
    answer = None
    copy_screen = screen.copy()
    dialog_screen = pygame.Surface((420,220))
    dialog_screen.fill((255,0,0))
    screen.blit(dialog_screen,(5,5))
    def ok():
        nonlocal answer
        answer = True
        
    def cancel():
        nonlocal answer
        answer = False
    
    dialog = pygame_menu.Menu(200, 410, 'confirm',onclose=pygame_menu.events.DISABLE_CLOSE,menu_position=(0,0),theme=pygame_menu.themes.THEME_DEFAULT,columns = 3,rows = 2)
    dialog.add_label('     ')
    dialog.add_button('Ok', ok, align=pygame_menu.locals.ALIGN_RIGHT)
    dialog.add_label('Are you sure?',align=pygame_menu.locals.ALIGN_CENTER)
    dialog.add_label(' ')
    dialog.add_label('       ',align=pygame_menu.locals.ALIGN_RIGHT)
    dialog.add_button('Cancel',cancel,align=pygame_menu.locals.ALIGN_LEFT)
    while answer == None:
        dialog_screen.fill((255,0,0))
        events = pygame.event.get()
        if dialog.is_enabled():
            dialog.update(events)
            dialog.draw(dialog_screen)
        screen.blit(dialog_screen,(5,5))
        pygame.display.flip()
    screen.blit(copy_screen,(0,0))
    return answer


#import pygameMenu
X, Y = 640, 480
FPS = 0
COLOR_BACKGROUND = (128, 230, 198)
CELL_SIZE = 40
pygame.init()
screen = pygame.display.set_mode((X, Y))
clock = pygame.time.Clock()
fps_font = pygame.font.SysFont('arial', 12)
game = True
x,y = 0,0
field_screen = pygame.Surface((640,480))
init_field_screen()



main_menu = pygame_menu.Menu(onclose=pygame_menu.events.DISABLE_CLOSE,height = 400, title = 'Chess v0.6', width = 400)
main_menu.add_button('Play with computer', play_with_computer)
main_menu.add_button('Play offline', play_offline)
main_menu.add_button('Play online', play_online)
main_menu.add_button('Settings', settings_menu)
main_menu.add_button('Quit', pygame_menu.events.EXIT)
background1 = background()
while game:
    clock.tick(FPS)
    events = pygame.event.get()
    for event in events:

        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.KEYDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x1 = pygame.mouse.get_pos()[0]
                y1 = pygame.mouse.get_pos()[1]
                pygame.draw.rect(screen,(randint(0,255),0,randint(0,255)), (x1-5,y1-5,10,10),4)
    next(background1)
    if main_menu.is_enabled():
        main_menu.update(events)
        main_menu.draw(screen)
        draw_rect(screen, main_menu.get_rect())
    fps = fps_font.render('fps: ' + str(int(clock.get_fps())), 0,(20,20,20))
    screen.blit(fps, (595,465))
    pygame.display.flip()
pygame.quit()
                

