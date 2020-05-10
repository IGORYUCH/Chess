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
game = True
x,y = 0,0

def init_field_screen(grid = False):
    grid_colors = [(200,200,200),(50,50,50)]
    print(True)
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
    print(False)
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
                    stopped = True
        pygame.display.flip()


def play_online():
    pass

def play_with_computer():
    pass
        


def alert():
    pass

field_screen = pygame.Surface((640,480))
init_field_screen()

dialog = 




main_menu =pygame_menu.Menu(onclose=pygame_menu.events.DISABLE_CLOSE,height = 400, title = 'Chess v0.5.2', width = 400)
main_menu.add_button('Play with computer', play_with_computer)
main_menu.add_button('Play offline', play_offline)
main_menu.add_button('Play online', play_online)
main_menu.add_button('Settings', settings_menu)
main_menu.add_button('Quit', pygame_menu.events.EXIT)
background1 = background()
while game:
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
    next(background1)
    if main_menu.is_enabled():
        main_menu.update(events)
        main_menu.draw(screen)
        pygame.draw.rect
    pygame.display.flip()
pygame.quit()
                

