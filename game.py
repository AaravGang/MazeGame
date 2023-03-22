# MAZE CREATOR USING RANDOMISED DFS AND BACKTRACKING
# PATH GENERATION USING DFS AND BFS (ANY ONE)

import random  # FOR RANDOMISING THE MAZE
import time  # FOR KEEPING TRACK OF HOW MUCH TIME IT TAKES TO GENERATE THE MAZE
from queue import (
    LifoQueue as lifo,
)  # LIFO- USED FOR BACKTRACKING & DFS, AND FIFO- USED FOR BFS

import pygame  # USE PYGAME TO CREATE THE  GUI
import asyncio

pygame.init()

from checkquit import CheckQuit
from constants import *
from cell import Cell
from button import Button


WIN = pygame.display.set_mode((LENGTH, BREADTH))
clock = pygame.time.Clock()


try:
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())
except:
    with open("highscore.txt", "w") as f:
        f.write("0")
        highscore = 0


# CREATES THE GRID FULL OF CELLS. GRID IS 2D
def setup(create=False, grid=None):
    if create:
        grid = []
        for row in range(rows):
            grid.append([])
            for col in range(cols):
                grid[row].append(
                    Cell(
                        row, col, width_buffer=WIDTH_BUFFER, height_buffer=HEIGHT_BUFFER
                    )
                )
        return grid

    else:
        for row in grid:
            for cell in row:
                cell.reinit()


GRID = setup(create=True)  # THE ENTIRE GRID/MAZE STORED IN  A 2D ARRAY
start = GRID[0][0]
end = GRID[-1][-1]


# change highscore
def change_highscore(s):
    global highscore
    highscore = s
    with open("highscore.txt", "w") as f:
        f.write(str(highscore))


# empty off some space in the middle where ghosts live
def make_den(size=2):
    for i in range(rows // 2 - 1, rows // 2 + rows % 2 + 1):
        for j in range(cols // 2 - 1, cols // 2 + cols % 2 + 1):
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
    if animate_generation:
        curr.show(WIN)
        next.show(WIN)
        pygame.display.flip()


# THE ALGORITHM FOR CREATING THE MAZE
def maze_algorithm():
    all_visited = False
    paths = {}  # CREATE A DICTIONARY TO STORE ALL THE ROOT CELLS OF EVERY VISITED CELL

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

        next = current.get_neighbour(
            GRID
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
        if animate_generation:
            current.show(WIN)
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
    WIN.fill(BLACK)
    for i in range(rows):
        for j in range(cols):
            GRID[i][j].show(WIN)

    # pygame.draw.rect(WIN,TURQUOISE,(GRID[0][0].x,GRID[0][0].y,cols*WIDTH,rows*WIDTH),width=wallwidth)

    # blit_pic(centerPic, (WIDTH * (cols // 4) + wallwidth // 2), (WIDTH * (rows // 4)) + wallwidth // 2)
    write_text(
        scoreFont,
        TURQUOISE,
        f"High Score: {highscore}",
        LENGTH - max(100, scoreFont.size(f"High Score: {highscore}")[0] + 10),
        10,
        True,
    )

    pygame.display.update()


def write_text(font, color, text, x, y, fill=True, center=False):
    text = font.render(text, True, color)
    textRect = text.get_rect()

    if center:
        textRect.center = (x, y)
    else:
        textRect.topleft = (x, y)
    if fill:
        WIN.fill(BLACK, textRect)
    WIN.blit(text, textRect)
    pygame.display.flip()


# function to randomly remove a few walls to make it easy.
def make_easy(difficulty=25):  # simplicity: 25 %
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if not GRID[i][j].blank:
                # 1 in 4 chance to remove each wall
                removeProbability = [random.randint(0, 3) for _ in range(4)][
                    : int(4 * (100 - difficulty) / 100)
                ]
                if (
                    GRID[i][j].right
                    and 0 in removeProbability
                    and not GRID[i][j + 1].blank
                ):
                    removeWall(GRID[i][j], GRID[i][j + 1])
                if (
                    GRID[i][j].left
                    and 0 in removeProbability
                    and not GRID[i][j - 1].blank
                ):
                    removeWall(GRID[i][j], GRID[i][j - 1])
                if (
                    GRID[i][j].top
                    and 0 in removeProbability
                    and not GRID[i - 1][j].blank
                ):
                    removeWall(GRID[i][j], GRID[i - 1][j])
                if (
                    GRID[i][j].bottom
                    and 0 in removeProbability
                    and not GRID[i + 1][j].blank
                ):
                    removeWall(GRID[i][j], GRID[i + 1][j])


def blit_pic(pic, x, y):
    WIN.blit(pic, (x, y))
    pygame.display.update()


# random colored chaser
def rand_chaser(image, color):
    image = image.copy()
    colorImage = pygame.Surface(image.get_size()).convert_alpha()
    colorImage.fill(color)
    image.blit(colorImage, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return image


# initialise all vars
def restart(level=1):
    setup(create=False, grid=GRID)

    player = GRID[0][0]
    player.make_player(player_img=playerR)

    chasers = []

    free_spots = sum(
        [
            list(filter(lambda spot: not spot.blank, row[cols // 2 :]))
            for row in GRID[rows // 2 :]
        ],
        [],
    )

    while len(chasers) < level:
        chaser_temp = random.choice(free_spots)
        free_spots.remove(chaser_temp)
        chaser_temp.make_chaser(
            rand_chaser(
                chaserImg,
                (
                    random.randint(128, 255),
                    random.randint(128, 255),
                    random.randint(128, 255),
                ),
            )
        )
        chasers.append(chaser_temp)

    draw_grid()

    return (
        player,
        chasers,
        level,
    )


# Function to detect swipes
# -1 is that it was not detected as a swipe or click
# It will return 1 , 2 for horizontal swipe
# If the swipe is vertical will return 3, 4
# If it was a click it will return 0
def getSwipeType(rel):
    x, y = rel if rel else pygame.mouse.get_rel()
    if abs(x) <= minSwipe:
        if y > minSwipe // 2:
            return 3
        elif y < -minSwipe // 2:
            return 4
    elif abs(y) <= minSwipe:
        if x > minSwipe // 2:
            return 1
        elif x < -minSwipe // 2:
            return 2

    return -1


# creates maze and then starts game
async def main(player, chasers, level):
    run = True  # WHILE THIS IS TRUE THE MAIN LOOP WILL RUN

    # DRAW THE GRID
    draw_grid()
    pygame.display.set_caption("Creating Maze...")
    print("Creating Maze...")

    # CREATE THE MAZE
    maze_algorithm()

    make_easy(min(100, 75))  # randomly remove a few walls

    draw_grid()

    pygame.display.set_caption("Hit space to start game.")
    print("Maze Created...Hit space to start game.")
    maze_created = True

    # THE MAIN GUI LOOP
    while run:
        for event in pygame.event.get():
            # IF THE USER HITS THE CROSS BUTTON . CLOSE THE WINDOW
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            # IF THE USER PRESSES ANY KEY PROCEED TO THE FOLLOWING
            if event.type == pygame.KEYDOWN or pygame.MOUSEBUTTONUP:
                if maze_created:  # and event.key == pygame.K_SPACE:
                    run = False
                    break

        await asyncio.sleep(0)
    await game(player, chasers, level)


# all the game logic
async def game(player, chasers, level):
    run = True

    count = 0
    score = 0

    game_over = False
    defeat = False

    pause_play = Button(
        pygame.Rect(
            LENGTH // 2 - min(WIDTH, 50),
            (HEIGHT_BUFFER - min(WIDTH, 50)) / 2,
            min(WIDTH, 50),
            min(WIDTH, 50),
        ),
        BLACK,
        lambda: True,
        **pause_play_button_style,
    )
    paused = False

    restart_button = Button(
        pygame.Rect(
            LENGTH // 2 + min(WIDTH, 50),
            (HEIGHT_BUFFER - min(WIDTH, 50)) / 2,
            min(WIDTH, 50),
            min(WIDTH, 50),
        ),
        BLACK,
        lambda: True,
        **restart_button_style,
    )
    score = 0

    pygame.display.set_caption(f"Level: {len(chasers)}")
    print("Game started.")
    swipe = 0

    while run:
        clock.tick(FPS)
        await asyncio.sleep(0)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                print("Quit via user interruption")
                pygame.quit()
                quit()

            if e.type == pygame.MOUSEMOTION:
                if e.touch:
                    s = getSwipeType(e.rel)
                    if s > 0:
                        swipe = s

            if e.type == pygame.KEYDOWN:
                swipe = 0

            if pause_play.check_event(e):
                paused = not paused
                pause_play.image = play_img if paused else pause_img

            if restart_button.check_event(e):
                return await main(*restart(level))

        pause_play.update(WIN)
        restart_button.update(WIN)

        pygame.display.update()

        if paused:
            continue

        if player:
            payload = player.move(WIN, GRID, swipe=swipe)
            count += 1

            defeat = payload.get("defeat")
            player = payload.get("player")
            score += (
                payload.get("score_gained") if payload.get("score_gained") else 0
            ) * level

            write_text(
                scoreFont, YELLOW, f"Score: {score}", 10, 10, True,
            )
            if score > highscore:
                change_highscore(score)
            write_text(
                scoreFont,
                TURQUOISE,
                f"High Score: {highscore}",
                LENGTH - max(100, scoreFont.size(f"High Score: {highscore}")[0] + 10),
                10,
                True,
            )

        if game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN] or pygame.mouse.get_pressed()[0]:
                print("LEVEL:", level)
                return await main(*restart(level))

        elif score >= (rows * cols) * level:
            write_text(
                pygame.font.Font("freesansbold.ttf", 100),
                PURPLE,
                "You Have Won!",
                LENGTH // 2,
                BREADTH // 2,
                False,
                True,
            )

            pygame.display.set_caption("Hit Enter to Restart.")
            print("Game Over. Hit Enter to Restart.")

            level += 1

            game_over = True

        elif defeat:
            write_text(
                pygame.font.Font("freesansbold.ttf", 100),
                PURPLE,
                "Game Over!",
                LENGTH // 2,
                BREADTH // 2,
                False,
                True,
            )

            pygame.display.set_caption("Hit Enter to Restart.")
            print("Game Over. Hit Enter to Restart.")

            game_over = True

        elif count % 10 == 0:
            for ind, c in enumerate(chasers):
                new_chaser = c.move(WIN, GRID, player).get("chaser")
                if new_chaser:
                    chasers[ind] = new_chaser
            count = 0


if __name__ == "__main__":
    asyncio.run(main(*restart()))
