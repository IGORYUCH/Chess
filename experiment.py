import pygame
import pygame_gui
from random import randrange as r

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

ui_manager = pygame_gui.UIManager((800, 600))
#manager.set_visual_debug_mode(True)
button_layout_rect = pygame.Rect(30, 20, 100, 20)
rect1 = pygame.Rect(20,20,300,400)
def play():
    #window_surface.fill((r(255),r(255),0))
    gamewindow  = pygame_gui.elements.ui_window.UIWindow(rect = pygame.Rect(0,0,800,600),manager = ui_manager, window_display_title = 'alert window')
    gamewindow.set_blocking(True)
##    label = pygame_gui.elements.UILabel(relative_rect = pygame.Rect(5,5,100,100),text = 'been alerted',manager = ui_manager,container = gamewindow)
##    ok_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(30,40,100,20),text='OK', manager=ui_manager,container=gamewindow)
    game = True
    while game:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            ui_manager.process_events(event)
            #print(event)
        ui_manager.update(time_delta)
        ui_manager.draw_ui(window_surface)
        pygame.display.update()

def play():
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
    
def show_alert2():    
    m = True
##                    alert = pygame_gui.windows.UIMessageWindow(pygame.Rect(100,100,300,300),html_message = 'alertbox',manager= ui_manager)
    alert_window = pygame_gui.elements.ui_window.UIWindow(rect = pygame.Rect(100,100,200,200),manager = ui_manager, window_display_title = 'alert window')
    alert_window.set_blocking(True)
    label = pygame_gui.elements.UILabel(relative_rect = pygame.Rect(5,5,100,100),text = 'been alerted',manager = ui_manager,container = alert_window)                                
    ok_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(30,40,100,20),text='OK', manager=ui_manager,container=alert_window)
    while m:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == ok_button:
                        m = False
                        print(alert_window.process_event(event))
            ui_manager.process_events(event)
        ui_manager.update(time_delta)
        ui_manager.draw_ui(window_surface)
        pygame.display.update()
    alert_window.kill()
    print('alerted')
def show_alert():    
    m = True
    alert = pygame_gui.windows.UIMessageWindow(pygame.Rect(100,100,300,300),html_message = 'alertbox',manager= ui_manager)
    alert.set_blocking(True)
    while m:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if alert.dismiss_button.pressed:
                m = False
            ui_manager.process_events(event)
        ui_manager.update(time_delta)
        ui_manager.draw_ui(window_surface)
        pygame.display.update()
    alert.kill()
    print('alerted')
window = pygame_gui.elements.ui_window.UIWindow(rect = rect1,
                                                    manager = ui_manager,
                                                window_display_title = 'Chess v 0.6',
                                                resizable = True
                                                    )
hello_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect,
                                             text='Say Hello',
                                             manager=ui_manager,
                                            container=window)
bye_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(30,40,100,20),
                                             text='Good bye',
                                             manager=ui_manager,
                                            container=window)
sure_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(30,160,100,20),
                                             text='Check sure',
                                             manager=ui_manager,
                                            container=window)

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
                if event.ui_element == hello_button:
                    print('AEFQ')
                    play()
                elif event.ui_element == bye_button:
                    background.fill((0,0,0))
                    print('bye')
                elif event.ui_element == sure_button:
                    show_alert()
        elif event.type ==  pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                pygame.draw.rect(window_surface,(r(255),r(255),r(255)),(x,y, 10,10),0)
                pygame.display.flip()
                pygame.time.delay(100)
        ui_manager.process_events(event)
    ui_manager.update(time_delta)
    #window_surface.blit(background, (0, 0))
    ui_manager.draw_ui(window_surface)

    pygame.display.update()
pygame.quit()
