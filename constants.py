import pygame

pygame.init()
pygame.font.init()


# touch related vars
minSwipe = 50


# GLOBAL VARIABLES RELATED TO DRAWING THE MAZE
infoObject = pygame.display.Info()

LENGTH, BREADTH = (
    (800, 800,)
    if infoObject.current_w > 800 and infoObject.current_h > 800
    else (infoObject.current_w, infoObject.current_h)
)

HEIGHT_BUFFER = 50  # make some space for buttons and score


rows = 15  # Number of rows = Number of cols
WIDTH = int((BREADTH - HEIGHT_BUFFER) / rows)
cols = int(LENGTH / WIDTH)

WIDTH_BUFFER = (LENGTH - cols * WIDTH) // 2


wallwidth = min(WIDTH // 10, 8)  # WIDTH OF EVERY WALL
pointRadius = min(WIDTH // 10, 8)

animate_generation = False
FPS = 10

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

# IMAGES
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

pause_img = pygame.transform.scale(
    pygame.image.load("static/pause.png"), (min(WIDTH, 50), min(WIDTH, 50))
)
play_img = pygame.transform.scale(
    pygame.image.load("static/play.png"), (min(WIDTH, 50), min(WIDTH, 50))
)
restart_img = pygame.transform.scale(
    pygame.image.load("static/restart.png"), (min(WIDTH, 50), min(WIDTH, 50))
)


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

