import pygame
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
    

while game:
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
    screen.blit(knight,(100,100))
    screen.blit(scaled_knight,(5,5))
    pygame.display.flip()
pygame.quit()
                


#  print(pygame.mouse.get_pos()) позиция мыши
#  rint(event.buttons[0]) нажата ли левая кнопка мыши

# pygame.MOUSEMOTION - event.buttons = (0,0,0)
# pygame.MOUSEBUTTONDWON event.button = 1,2...5
