import pygame

pygame.font.init()

# GLOBAL VARIABLES RELATED TO DRAWING THE MAZE
LENGTH, BREADTH = 800, 800  # LENGTH AND BREADTH OF THE MAZE ought to be same
BUFFER_HEIGHT = 100  # make some space for buttons and score

rows = 20  # Number of rows = Number of cols
WIDTH = int(LENGTH / rows)

BREADTH += BUFFER_HEIGHT  # increase the height/breadth

wallwidth = min(WIDTH // 10, 10)  # WIDTH OF EVERY WALL
pointRadius = min(WIDTH // 10, 10)

# COLORS
KHAKI = (240, 230, 140)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (200, 202, 255)
LIGHTGREEN = (20, 246, 211)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
BROWN = (150, 94, 0)

playerR = pygame.transform.scale(
    pygame.image.load("static/pacman.png"), (WIDTH // 2, WIDTH // 2)
)
playerU = pygame.transform.rotate(playerR, 90)
playerL = pygame.transform.flip(playerR, True, False)
playerD = pygame.transform.rotate(playerL, 90)

chaserImg = pygame.transform.scale(
    pygame.image.load("static/chaser.png"), (WIDTH // 2, WIDTH // 2)
)

scoreFont = pygame.font.Font("freesansbold.ttf", 25)

pause_img = pygame.transform.scale(pygame.image.load("static/pause.png"), (50, 50))
play_img = pygame.transform.scale(pygame.image.load("static/play.png"), (50, 50))
restart_img = pygame.transform.scale(pygame.image.load("static/restart.png"), (50, 50))


button_style = {
    "call_on_release": True,
    "hover_color": LIGHTGREEN,
    "clicked_color": GREY,
    "click_sound": None,
    "hover_sound": None,
    "image": None,
}

pause_play_button_style = button_style.copy()
pause_play_button_style["image"] = pause_img

restart_button_style = button_style.copy()
restart_button_style["image"] = restart_img

