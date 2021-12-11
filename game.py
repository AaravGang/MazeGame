# MAZE CREATOR USING RANDOMISED DFS AND BACKTRACKING
# PATH GENERATION USING DFS AND BFS (ANY ONE)

import random  # FOR RANDOMISING THE MAZE
import time  # FOR KEEPING TRACK OF HOW MUCH TIME IT TAKES TO GENERATE THE MAZE
from queue import (
    LifoQueue as lifo,
)  # LIFO- USED FOR BACKTRACKING & DFS, AND FIFO- USED FOR BFS

import pygame  # USE PYGAME TO CREATE THE  GUI

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
            for col in range(rows):
                grid[row].append(Cell(row, col, height_buffer=BUFFER_HEIGHT))
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


# empty off some space in the middle
def make_blank(size=2):
    for i in range(rows // (2 * size), rows - (rows // (2 * size))):
        for j in range(rows // (2 * size), rows - (rows // (2 * size))):
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
        for j in range(rows):
            GRID[i][j].show(WIN)

    # blit_pic(centerPic, (WIDTH * (rows // 4) + wallwidth // 2), (WIDTH * (rows // 4)) + wallwidth // 2)
    write_text(scoreFont, TURQUOISE, f"High Score: {highscore}", 100, 60, True)

    pygame.display.update()


def write_text(font, color, text, x, y, fill=True):
    text = font.render(text, True, color)
    textRect = text.get_rect()

    textRect.center = (x, y)
    if fill:
        WIN.fill(BLACK, textRect)
    WIN.blit(text, textRect)
    pygame.display.flip()


# function to randomly remove a few walls to make it easy.
def make_easy():
    for i in range(1, rows - 1):
        for j in range(1, rows - 1):
            if not GRID[i][j].blank:
                # 1 in 4 chance to remove each wall
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
def restart(level=1):
    setup(create=False, grid=GRID)

    player = GRID[0][0]
    player.make_player(player_img=playerR)

    chasers = []

    while len(chasers) < level:
        chaser_temp = GRID[random.randint(rows // 2, rows - 1)][
            random.randint(rows // 2, rows - 1)
        ]
        if chaser_temp in chasers:
            continue
        chaser_temp.make_chaser()
        chasers.append(chaser_temp)

    draw_grid()

    return (
        player,
        chasers,
        level,
    )


# creates maze and then starts game
def main(player, chasers, level):
    maze_created = False
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
                if event.key == pygame.K_RETURN and not maze_created:
                    pygame.display.set_caption("Creating Maze...")
                    print("Creating Maze...")

                    # CREATE THE MAZE
                    maze_algorithm()

                    make_easy()  # randomly remove a few walls

                    pygame.display.set_caption(
                        "Maze Created...Hit space to start game."
                    )
                    print("Maze Created...Hit space to start game.")
                    maze_created = True

                elif maze_created and event.key == pygame.K_SPACE:
                    run = False
                    break

    game(player, chasers, level)


# all the game logic
def game(player, chasers, level):
    run = True
    player.show(WIN)
    for c in chasers:
        c.show(WIN)

    pygame.display.update()

    speed = 10
    count = 0
    score = 0

    game_over = False
    defeat = False

    pause_play = Button(
        pygame.Rect(300, 30, 50, 50), BLACK, lambda: True, **pause_play_button_style
    )
    paused = False

    restart_button = Button(
        pygame.Rect(500, 30, 50, 50), BLACK, lambda: True, **restart_button_style
    )
    score = 0

    pygame.display.set_caption(f"Maze Game. Level: {len(chasers)}")
    print("Game started.")

    while run:
        clock.tick(speed)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                print("Quit via user interruption")
                pygame.quit()
                quit()

            if pause_play.check_event(e):
                paused = not paused
                pause_play.image = play_img if paused else pause_img

            if restart_button.check_event(e):
                return main(*restart(level))

        pause_play.update(WIN)
        restart_button.update(WIN)
        pygame.display.update()

        if paused:
            continue

        if player:
            payload = player.move(WIN, GRID)
            count += 1

            defeat = payload.get("defeat")
            player = payload.get("player")
            score += (
                payload.get("score_gained") if payload.get("score_gained") else 0
            ) * level

            write_text(scoreFont, YELLOW, f"Score: {score}", 100, 30, True)
            if score > highscore:
                change_highscore(score)
            write_text(scoreFont, TURQUOISE, f"High Score: {highscore}", 100, 60, True)

        if game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                print(level)
                return main(*restart(level))

        elif score >= (rows * rows) * level:
            write_text(
                pygame.font.Font("freesansbold.ttf", 100),
                PURPLE,
                "You Have Won!",
                LENGTH // 2,
                BREADTH // 2,
                False,
            )

            pygame.display.set_caption("Game Over. Hit Enter to Restart.")
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
            )

            pygame.display.set_caption("Game Over. Hit Enter to Restart.")
            print("Game Over. Hit Enter to Restart.")

            game_over = True

        elif count % 5 == 0:
            for ind, c in enumerate(chasers):
                new_chaser = c.move(WIN, GRID, player).get("chaser")
                if new_chaser:
                    chasers[ind] = new_chaser


if __name__ == "__main__":
    main(*restart())
