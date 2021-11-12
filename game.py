# MAZE CREATOR USING RANDOMISED DFS AND BACKTRACKING
# PATH GENERATION USING DFS AND BFS (ANY ONE)

import random  # FOR RANDOMISING THE MAZE
import time  # FOR KEEPING TRACK OF HOW MUCH TIME IT TAKES TO GENERATE THE MAZE
from queue import (
    LifoQueue as lifo,
    Queue as fifo,
)  # LIFO- USED FOR BACKTRACKING & DFS, AND FIFO- USED FOR BFS

import pygame  # USE PYGAME TO CREATE THE  GUI

pygame.init()
# GLOBAL VARIABLES RELATED TO DRAWING THE MAZE
LENGTH, BREADTH = 800, 800  # LENGTH AND BREADTH OF THE MAZE

WIDTH = 50  # WIDTH OF EACH SQUARE
cols = LENGTH // WIDTH  # NO. OF COLUMNS
rows = BREADTH // WIDTH  # NO. OF ROWS
GRID = []  # THE ENTIRE GRID/MAZE STORED IN  A 2D ARRAY
paths = {}  # CREATE A DICTIONARY TO STORE ALL THE ROOT CELLS OF EVERY VISITED CELL
wallwidth = WIDTH // 10  # WIDTH OF EVERY WALL
pointRadius = WIDTH // 10

# GLOBAL VARIABLES THAT KEEP TRACK OF MAZE MAKING AND PATH FINDING
# MAKE A VARIABLE TO KNOW IF ALL CELLS ARE VISITED ( MAZE MAKING )
all_visited = False
# MAKE A VARIABLE TO KNOW IF THE PATH FROM START TO END IS FOUND ( PATH FINDING )
path_found = False

# CHANGE FRAME RATE OF THE MAZE MAKER
clock = pygame.time.Clock()

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

WIN = pygame.display.set_mode((LENGTH, BREADTH))


playerR = pygame.transform.scale(
    pygame.image.load("pacman.png"), (WIDTH // 2, WIDTH // 2)
)
playerU = pygame.transform.rotate(playerR, 90)
playerL = pygame.transform.flip(playerR, True, False)
playerD = pygame.transform.rotate(playerL, 90)

playerImg = playerR  # start if off facing right
chaserImg = pygame.transform.scale(
    pygame.image.load("chaser.png"), (WIDTH // 2, WIDTH // 2)
)

scoreFont = pygame.font.Font("freesansbold.ttf", (WIDTH // 2) - wallwidth)


# Class Cell. Every element in the grid is a Cell
class Cell:
    def __init__(self, row, col):
        self.row = row  # ROW NUMBER
        self.col = col  # COLUMN NUMBER
        self.y = row * WIDTH  # POSITION X COORDINATE
        self.x = col * WIDTH  # POSITION Y COORDINATE

        self.visited = False  # IS IT VISITED OR NOT, USED WHILE MAZE MAKING
        self.searched = False  # IS IT SEARCHED OR NOT, USED WHILE PATH FINDING
        self.start = False  # IS IT THE START CELL
        self.end = False  # IS IT THE END CELL
        self.ispath = False  # DOES THIS CELL COME IN THE PATH
        self.blank = False
        # RIGHT, LEFT, TOP AND BOTTOM WALLS. CHANGE TO False TO REMOVE THEM
        self.right = True
        self.left = True
        self.top = True
        self.bottom = True

        # COLORS USED FOR DRAWING THE CELL,HIGHLIGHTING IT AND DRAWING ITS WALLS
        self.color = KHAKI
        self.highlight_color = ORANGE
        self.line_color = TURQUOISE

        self.playerHost = False
        self.chaserHost = False
        self.point = True

    # THIS FUNCTION CHECKS ALL UNVISITED NEIGHBOURS OF A CELL AND RETURNS A RANDOM ONE IF IT DOES
    def get_neighbour(self):
        neighbours = (
            []
        )  # A LIST NEIGHBOURS. TO TEMPORARILY STORE ALL NEIGHBOURS OF A GIVEN CELL

        # THIS PART IS FOR THE MAZE MAKING...HERE THE NEIGHBOURS OF A GIVEN CELL ARE THOSE CELLS WHICH SURROUND IT (TOP,BOTTOM,LEFT,RIGHT)
        # AND ARE NOT YET VISITED
        # WALLS IN BETWEEN NEIGHBOURS ARE NOT CONSIDERED
        if not all_visited:
            # IF THE GIVEN CELL IS NOT THE IN FIRST ROW AND HAS A NON VISITED NEIGHBOUR ABOVE IT, APPEND IT TO NEIGHBOURS
            if (
                0 < self.row
                and not GRID[self.row - 1][self.col].visited
                and not GRID[self.row - 1][self.col].blank
            ):
                neighbours.append(GRID[self.row - 1][self.col])  # top

            # IF THE GIVEN CELL IS NOT THE IN LAST ROW AND HAS A NON VISITED NEIGHBOUR BELOW IT, APPEND IT TO NEIGHBOURS
            if (
                rows - 1 > self.row
                and not GRID[self.row + 1][self.col].visited
                and not GRID[self.row + 1][self.col].blank
            ):
                neighbours.append(GRID[self.row + 1][self.col])  # bottom

            # IF THE GIVEN CELL IS NOT THE IN FIRST COLUMN AND HAS A NON VISITED NEIGHBOUR TO THE LEFT OF IT, APPEND IT TO NEIGHBOURS
            if (
                0 < self.col
                and not GRID[self.row][self.col - 1].visited
                and not GRID[self.row][self.col - 1].blank
            ):
                neighbours.append(GRID[self.row][self.col - 1])  # left

            # IF THE GIVEN CELL IS NOT THE IN LAST COLUMN AND HAS A NON VISITED NEIGHBOUR TO THE RIGHT OF IT, APPEND IT TO NEIGHBOURS
            if (
                cols - 1 > self.col
                and not GRID[self.row][self.col + 1].visited
                and not GRID[self.row][self.col + 1].blank
            ):
                neighbours.append(GRID[self.row][self.col + 1])  # right

            # IF THERE ARE ANY NEIGHBOURS FOR A GIVEN CELL, THEN RETURN A RANDOM ONE, TO RANDOMISE THE FORMATION OF THE MAZE
            if len(neighbours) > 0:
                return neighbours[random.randint(0, len(neighbours) - 1)]
            # IF THERE ARE NO NEIGHBOURS THAT ARE UNVISITED RETURN FALSE
            return False

    def get_unsearched_neighbour(self, searched):
        neighbours = (
            []
        )  # A LIST NEIGHBOURS. TO TEMPORARILY STORE ALL NEIGHBOURS OF A GIVEN CELL

        # THIS PART IS FOR THE PATH FINDING...HERE THE NEIGHBOURS OF A CELL ARE THOSE THAT SURROUND IT
        # AND ARE NOT YET SEARCHED
        # AND THERE IS NO WALL BETWEEN THE TWO MUTUAL NEIGHBOURS

        # IF THERE IS A RIGHT NEIGHBOUR THAT SATISFIES THE CONDITIONS APPEND IT
        if not self.right and GRID[self.row][self.col + 1] not in searched:
            neighbours.append(GRID[self.row][self.col + 1])  # right

        # IF THERE IS A BOTTOM NEIGHBOUR THAT SATISFIES THE CONDITIONS APPEND IT
        if not self.bottom and GRID[self.row + 1][self.col] not in searched:
            neighbours.append(GRID[self.row + 1][self.col])  # bottom

        # IF THERE IS A LEFT NEIGHBOUR THAT SATISFIES THE CONDITIONS APPEND IT
        if not self.left and GRID[self.row][self.col - 1] not in searched:
            neighbours.append(GRID[self.row][self.col - 1])  # left

        # IF THERE IS A TOP NEIGHBOUR THAT SATISFIES THE CONDITIONS APPEND IT
        if not self.top and GRID[self.row - 1][self.col] not in searched:
            neighbours.append(GRID[self.row - 1][self.col])  # top

        # IF THERE WERE ANY NEIGHBOURS FOR THIS CELL, RETURN THE LIST OF NEIGHBOURS
        if len(neighbours) > 0:
            return neighbours
        # IF NOT RETURN A LIST WITH FALSE (IN A LIST TO AVOID "BOOL TYPE NOT ITERABLE ERROR")
        return False

    # CHANGE THE COLOR OF THE END CELL
    def make_end(self):
        self.color = LIGHTBLUE

    # CHANGE THE COLOR OF THE START CELL
    def make_start(self):
        self.color = BROWN

    # CHANGE THE COLOR OF VISITED CELLS,WHEN MAZE IS COMPLETED ALL CELLS BECOME VISITED
    def make_visited(self):
        if not self.end and not self.start:
            self.color = BLACK

    # CHANGE THE COLOR OF THOSE CELLS THAT COME IN THE PATH FROM START TO END
    def make_path(self):
        if not self.end and not self.start:
            self.color = PURPLE

    # HIGHLIGHT ANY CELL FOR DEBUGGING
    def highlight(self):
        pygame.draw.rect(WIN, self.highlight_color, (self.x, self.y, WIDTH, WIDTH), 0)
        pygame.display.flip()

    # logic to move player or chaser
    def move(self):
        global playerImg, player, chaser, score

        if self.playerHost and self.chaserHost:
            return True # game over

        # logic for moving player
        elif self.playerHost:
            if self.point:
                self.point = False
                score += 1
                self.show()
                pygame.display.update()
                write_text(scoreFont, WHITE, "SCORE: " + str(score), 100, WIDTH // 2)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT] and not self.right:
                self.playerHost = False
                GRID[self.row][self.col + 1].playerHost = True
                self.show()
                pygame.display.flip()
                playerImg = playerR
                GRID[self.row][self.col + 1].show()
                pygame.display.flip()

                player = GRID[self.row][self.col + 1]

            elif keys[pygame.K_LEFT] and not self.left:
                self.playerHost = False
                GRID[self.row][self.col - 1].playerHost = True
                self.show()
                pygame.display.flip()
                playerImg = playerL
                GRID[self.row][self.col - 1].show()
                pygame.display.flip()

                player = GRID[self.row][self.col - 1]

            elif keys[pygame.K_UP] and not self.top:
                self.playerHost = False
                GRID[self.row - 1][self.col].playerHost = True
                self.show()
                pygame.display.flip()
                playerImg = playerU
                GRID[self.row - 1][self.col].show()
                pygame.display.flip()

                player = GRID[self.row - 1][self.col]

            elif keys[pygame.K_DOWN] and not self.bottom:
                self.playerHost = False
                GRID[self.row + 1][self.col].playerHost = True
                self.show()
                pygame.display.flip()
                playerImg = playerD
                GRID[self.row + 1][self.col].show()
                pygame.display.flip()

                player = GRID[self.row + 1][self.col]

        # logic for moving chaser
        elif self.chaserHost:
            chaser = bfs(self, player)
            self.chaserHost = False
            chaser.chaserHost = True
            self.show()
            pygame.display.update()
            chaser.show()
            pygame.display.update()

    # THIS FUNCTION SHOWS THE CELL ON PYGAME WINDOW
    def show(self):
        # DRAW A RECTANGLE WITH THE DIMENSIONS OF THE CELL, TO COLOR IT
        pygame.draw.rect(WIN, self.color, (self.x, self.y, WIDTH, WIDTH), 0)

        # DRAW RIGHT, LEFT, TOP, BOTTOM WALLS
        if self.right:  # RIGHT
            pygame.draw.line(
                WIN,
                self.line_color,
                (self.x + WIDTH, self.y),
                (self.x + WIDTH, self.y + WIDTH),
                width=wallwidth,
            )
        if self.left:  # LEFT
            pygame.draw.line(
                WIN,
                self.line_color,
                (self.x, self.y),
                (self.x, self.y + WIDTH),
                width=wallwidth,
            )
        if self.top:  # TOP
            pygame.draw.line(
                WIN,
                self.line_color,
                (self.x, self.y),
                (self.x + WIDTH, self.y),
                width=wallwidth,
            )
        if self.bottom:  # BOTTOM
            pygame.draw.line(
                WIN,
                self.line_color,
                (self.x, self.y + WIDTH),
                (self.x + WIDTH, self.y + WIDTH),
                width=wallwidth,
            )
        if self.point:
            pygame.draw.circle(
                WIN, KHAKI, (self.x + WIDTH // 2, self.y + WIDTH // 2), pointRadius
            )
        if self.playerHost:
            WIN.blit(playerImg, (self.x + WIDTH // 4, self.y + WIDTH // 4))
        if self.chaserHost:
            WIN.blit(chaserImg, (self.x + WIDTH // 4, self.y + WIDTH // 4))

# CREATES THE GRID FULL OF CELLS. GRID IS 2D
def setup():
    for row in range(rows):
        GRID.append([])
        for col in range(cols):
            GRID[row].append(Cell(row, col))

# empty off some space in the middle
def make_blank(size=2):
    for i in range(rows // (2 * size), rows - (rows // (2 * size))):
        for j in range(cols // (2 * size), cols - (cols // (2 * size))):
            GRID[i][j].blank = True

# FUNCTION TO REMOVE A WALL BETWEEN THE CURRENT AND THE NEXT CELL
def removeWall(curr, next):
    # r IS THE CURRENT ROW - NEXT ROW AND c IS THE CURRENT COLUMN - NEXT COLUMN
    r, c = curr.row - next.row, curr.col - next.col
    # IF c IS 1 WE KNOW THE NEXT CELL IS THE TO THE LEFT OF THE CURRENT CELL
    if c == 1:
        curr.left = False
        next.right = False
    # IF c IS -1 WE KNOW THE NEXT CELL IS THE TO THE RIGHT OF THE CURRENT CELL
    if c == -1:
        next.left = False
        curr.right = False
    # IF r IS 1 WE KNOW THE CURRENT CELL IS BELOW THE NEXT CELL
    if r == 1:
        next.bottom = False
        curr.top = False
    # IF r IS -1 WE KNOW THE CURRENT CELL IS ABOVE THE NEXT CELL
    if r == -1:
        curr.bottom = False
        next.top = False

    # SHOW THE UPDATED VERSIONS OF THE CURRENT AND NEXT CELL
    curr.show()
    next.show()
    pygame.display.flip()

# THE ALGORITHM FOR CREATING THE MAZE
def maze_algorithm():
    # USING THE GLOBAL VARIABLE, TO STOP MAZE MAKING WHEN ALL CELLS HAVE BEEN VISITED
    global all_visited, paths

    # STARTING THE TIMER FOR MAZE MAKING
    start_time = time.time()

    # ---- STEP 1 MAZE MAKER ---- #
    # MAKE THE START CELL FOR MAZE MAKING (THE CELL TO BEGIN MAKING THE MAZE FROM)
    # MAKE THE CURRENT CELL THE START CELL
    # MAKE IT VISITED
    start = GRID[0][0]
    current = start
    current.visited = True
    current.make_visited()

    # INITIALISE THE STACK FOR BACKTRACKING ( WHEN THERE ARE NO NEIGHBOURS FOR A CELL, BACKTRACK TO A CELL WITH NEIGHBOURS )
    stack = lifo()

    # --- STEP 2--- #
    # WHILE THERE ARE UNVISITED CELLS
    while not all_visited:
        CheckQuit()  # CHECK IF THE USER WANTS TO QUIT PYGAME

        next = (
            current.get_neighbour()
        )  # STEP 2.1, A RANDOM UNVISITED NEIGHBOUR. VALUE IS FALSE IF THERE ARE NONE
        if (
            next
        ):  # CONDITION OF STEP 2.1. IF THERE ARE ANY UNVISITED NEIGHBOURS THEN DO THE FOLLOWING
            stack.put(current)  # STEP 2.1.2... PUSH THE CURRENT CELL TO THE STACK
            removeWall(
                current, next
            )  # STEP 2.1.3... REMOVE THE WALL BETWEEN THE CURRENT AND THE NEXT CELL
            # STEP 2.1.4... MARK THE CHOSEN CELL AS VISITED AND MAKE IT THE CURRENT CELL
            next.visited = True
            next.make_visited()
            paths[
                next
            ] = current  # BEFORE MAKING NEXT CURRENT MAKE CURRENT THE ROOT OF THE NEXT CELL, TO HELP IN PATH FINDING
            current = next

        elif (
            stack.qsize() > 0
        ):  # STEP 2.2... IF THERE ARE NO UNVISITED NEIGHBOURS AND THE STACK SIZE IS NOT ZERO
            current = (
                stack.get()
            )  # STEP 2.2.1. POP A CELL FROM THE STACK AND MAKE IT THE CURRENT CELL

        # SHOW THE UPDATED CURRENT CELL
        current.show()
        pygame.display.flip()

        # ---- STEP 2 DONE ---- ALGORITHM IS COMPLETE ----

        # IF ALL CELLS ARE VISITED, ANNOUNCE THE COMPLETION OF MAZE TO BE ABLE TO CONTINUE WITH THE PATH FINDING
        if stack.qsize() == 0:
            all_visited = True
            end_time = time.time()  # END THE TIMER
            # PRINT THE TIME TAKE TO FIND THE PATH
            print(f"Time taken to create the maze : {end_time - start_time}")

            # SAVE AN IMAGE OF THE MAZE
            # pygame.image.save(WIN, 'maze.png')

# show all the cells
def draw_grid():
    for i in range(rows):
        for j in range(cols):
            GRID[i][j].show()

    # blit_pic(centerPic, (WIDTH * (cols // 4) + wallwidth // 2), (WIDTH * (rows // 4)) + wallwidth // 2)

    pygame.display.update()

# path finding - bfs is ideal for maze
def bfs(start_cell, end_cell):
    # CREATE A QUEUE TO SEARCH THROUGH THE MAZE 'BREADTH FIRST'
    Q = fifo()
    searched = []
    # STEP 1. MAKE THE START CELL SEARCHED AND PUSH IT TO THE QUEUE
    searched.append(start_cell)
    Q.put(start_cell)
    # CREATE A HASH-MAP TO KEEP TRACK OF WHERE EACH CELL COMES FROM ( ROOT OF EACH CELL ), AND ALL THE SEARCHED CELLS
    track = {}
    # KEEP SEARCHING UNTIL A PATH IS FOUND
    while True:
        CheckQuit()  # CHECK IF THE USER WANTS TO QUIT PYGAME
        # STEP 2
        # POP A CELL FROM THE QUEUE AND ASSIGN IT TO ROOT
        root = Q.get()
        # IF ROOT IS THE END CELL, PATH HAS BEEN FOUND
        if root == end_cell:
            # BACKTRACK THE PATH FROM THE END CELL TO THE START CELL USING THE HASH-MAP
            while track[root] != start_cell:
                CheckQuit()  # CHECK IF THE USER WANTS TO QUIT PYGAME

                # UPDATE ROOT TO BE THE ROOT OF THE CURRENT ROOT CELL
                root = track[root]
            # ANNOUNCE THE COMPLETION OF PATH
            return root

        # IF ROOT HAS ANY NEIGHBOURS, MAKE THEM ALL SEARCHED IF THEY HAVEN'T ALREADY BEEN AND PUSH THEM TO THE QUEUE
        neighbours = root.get_unsearched_neighbour(searched)
        if neighbours:
            for n in neighbours:
                searched.append(n)
                track[n] = root
                Q.put(n)

# A FUNCTION TO CHECK IF THE USER WANTS TO QUIT PYGAME
def CheckQuit():
    # clock.tick(speed)  # SET THE FRAME RATE
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Quit via user interruption")
            pygame.quit()
            quit()

def write_text(font, color, text, x, y, fill=True):
    text = font.render(text, True, color)
    textRect = text.get_rect()

    textRect.center = (x, y)
    if fill:
        WIN.fill(BLACK, textRect)
    WIN.blit(text, textRect)
    pygame.display.flip()

# creates maze and then starts game
def main():
    global path_found, all_visited, GRID  # GLOBALISE THESE VARIABLES TO RE-INITIALISE THEM WHEN THE USER WANTS TO RESTART

    run = True  # WHILE THIS IS TRUE THE MAIN LOOP WILL RUN

    # DRAW THE GRID
    draw_grid()
    # INSTRUCT THE USER TO HIT ENTER TO START THE MAZE MAKING
    pygame.display.set_caption("Hit Enter to start creating maze")
    print("Hit Enter to start creating maze")

    # THE MAIN GUI LOOP
    while run:
        for event in pygame.event.get():
            # IF THE USER HITS THE CROSS BUTTON . CLOSE THE WINDOW
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            # IF THE USER PRESSES ANY KEY PROCEED TO THE FOLLOWING
            if event.type == pygame.KEYDOWN:
                # IF THE USER HITS ENTER AND THE MAZE HASN'T BEEN CREATED YET, DO SO
                if event.key == pygame.K_RETURN and not all_visited:
                    pygame.display.set_caption("Creating Maze...")
                    print("Creating Maze...")

                    # CREATE THE MAZE
                    maze_algorithm()

                    make_easy()  # randomly remove a few walls

                    pygame.display.set_caption(
                        "Maze Created...Hit space to start game."
                    )
                    print("Maze Created...Hit space to start game.")

                elif all_visited and event.key == pygame.K_SPACE:
                    run = False
                    break

    game()

# function to randomly remove a few walls to make it easy.
def make_easy():
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if not GRID[i][j].blank:
                removeProbability = [random.randint(0, 3) for _ in range(4)]
                if (
                    GRID[i][j].right
                    and removeProbability[0] == 0
                    and not GRID[i][j + 1].blank
                ):
                    removeWall(GRID[i][j], GRID[i][j + 1])
                if (
                    GRID[i][j].left
                    and removeProbability[1] == 0
                    and not GRID[i][j - 1].blank
                ):
                    removeWall(GRID[i][j], GRID[i][j - 1])
                if (
                    GRID[i][j].top
                    and removeProbability[2] == 0
                    and not GRID[i - 1][j].blank
                ):
                    removeWall(GRID[i][j], GRID[i - 1][j])
                if (
                    GRID[i][j].bottom
                    and removeProbability[3] == 0
                    and not GRID[i + 1][j].blank
                ):
                    removeWall(GRID[i][j], GRID[i + 1][j])

def blit_pic(pic, x, y):
    WIN.blit(pic, (x, y))
    pygame.display.update()

# initialise all vars
def restart():
    global start, end, player, chaser, GRID, all_visited, paths, playerImg, score
    GRID = []
    all_visited = False
    paths = {}
    setup()
    start = GRID[0][0]
    end = GRID[-1][-1]
    player = start
    player.playerHost = True
    chaser = GRID[0][-1]
    chaser.chaserHost = True
    score = 0
    playerImg = playerR


# setup all variables
restart()


# load a pic to fill in the center
# centerPic = pygame.transform.smoothscale(pygame.image.load('pic path'), (
# int(LENGTH - (WIDTH * ((cols // 4) * 2)) - wallwidth), (int(LENGTH - (WIDTH * ((cols // 4) * 2)) - wallwidth))))

# all the game logic
def game():
    global player, chaser
    game = True
    player.show()
    pygame.display.update()
    chaser.show()
    pygame.display.update()
    speed = 10
    count = 0
    write_text(
        scoreFont, WHITE, "SCORE: " + str(score), 2 * WIDTH, rows * WIDTH + WIDTH // 2
    )
    # blit the center pic
    # blit_pic(centerPic,(WIDTH*(cols//4)+wallwidth//2),(WIDTH*(rows//4))+wallwidth//2)

    pygame.display.set_caption("Maze Game.")
    print("Game started.")

    while game:
        clock.tick(speed)
        CheckQuit()
        player.move()
        count += 1

        if score == rows * cols:
            write_text(
                pygame.font.Font("freesansbold.ttf", 100),
                PURPLE,
                "You Have Won!",
                LENGTH // 2,
                BREADTH // 2,
                False,
            )
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                restart()
                main()
                break
        elif chaser == player:
            write_text(
                pygame.font.Font("freesansbold.ttf", 100),
                PURPLE,
                "Game Over!",
                LENGTH // 2,
                BREADTH // 2,
                False,
            )
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                restart()
                main()
                break
        elif count % 5 == 0:
            chaser.move()


if __name__ == "__main__":
    main()
