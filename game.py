# MAZE CREATOR USING RANDOMISED DFS AND BACKTRACKING
# PATH GENERATION USING DFS AND BFS (ANY ONE)

import random  # FOR RANDOMISING THE MAZE
import time  # FOR KEEPING TRACK OF HOW MUCH TIME IT TAKES TO GENERATE THE MAZE
from queue import (
    LifoQueue as lifo,
    Queue as fifo,
)  # LIFO- USED FOR BACKTRACKING & DFS, AND FIFO- USED FOR BFS

import pygame  # USE PYGAME TO CREATE THE  GUI
import asyncio
from threading import Thread

pygame.init()

from checkquit import CheckQuit
from constants import *
from cell import Cell, Player
from button import Button

try:
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())
except:
    with open("highscore.txt", "w") as f:
        f.write("0")
        highscore = 0

WIN = pygame.display.set_mode((LENGTH, BREADTH))
clock = pygame.time.Clock()

# LOGIC
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

# LOGIC
# change highscore
def change_highscore(s):
    global highscore
    highscore = s
    with open("highscore.txt", "w") as f:
        f.write(str(highscore))


# LOGIC
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
        curr.show_(WIN, True)
        next.show_(WIN, True)
        pygame.display.update()


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
            current.show(WIN, True)
            pygame.display.update()

        # ---- STEP 2 DONE ---- ALGORITHM IS COMPLETE ----

        # IF ALL CELLS ARE VISITED, ANNOUNCE THE COMPLETION OF MAZE TO BE ABLE TO CONTINUE WITH THE PATH FINDING
        if stack.qsize() == 0:
            all_visited = True
            end_time = time.time()  # END THE TIMER
            # PRINT THE TIME TAKE TO FIND THE PATH
            print(f"Time taken to create the maze : {end_time - start_time}")

            # SAVE AN IMAGE OF THE MAZE
            # pygame.image.save(WIN, 'maze.png')


# GRAPHICS
# show all the cells
def draw_grid(player=None, chasers=[], force=False, fill=False, update=True):
    if fill:
        WIN.fill(BLACK)
    for i in range(rows):
        for j in range(cols):
            GRID[i][j].show_(WIN, force)
    if player:
        player.show_(WIN, force)

    for chaser in chasers:
        chaser.show_(WIN, force)

    # blit_pic(centerPic, (WIDTH * (cols // 4) + wallwidth // 2), (WIDTH * (rows // 4)) + wallwidth // 2)
    write_text(
        scoreFont,
        TURQUOISE,
        f"High Score: {highscore}",
        LENGTH - max(100, scoreFont.size(f"High Score: {highscore}")[0] + 10),
        10,
        True,
    )

    if update:
        pygame.display.update()


# GRAPHICS
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


# function to randomly remove a few walls to make it easy.
def make_easy(difficulty=25):  # difficullty: 25 %
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
                    and 1 in removeProbability
                    and not GRID[i][j - 1].blank
                ):
                    removeWall(GRID[i][j], GRID[i][j - 1])
                if (
                    GRID[i][j].top
                    and 2 in removeProbability
                    and not GRID[i - 1][j].blank
                ):
                    removeWall(GRID[i][j], GRID[i - 1][j])
                if (
                    GRID[i][j].bottom
                    and 3 in removeProbability
                    and not GRID[i + 1][j].blank
                ):
                    removeWall(GRID[i][j], GRID[i + 1][j])


# GRAPHICS
def blit_pic(pic, x, y):
    WIN.blit(pic, (x, y))
    pygame.display.update()


# ??
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

    playerHost = GRID[0][0]
    playerHost.make_player_host()
    player = Player(
        playerHost, 0, 0, width_buffer=WIDTH_BUFFER, height_buffer=HEIGHT_BUFFER
    )

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

    draw_grid(player=player, force=True, fill=True)

    return (
        player,
        chasers,
        level,
    )


# LOGIC
# Function to detect swipes
# -1 is that it was not detected as a swipe or click
# It will return 1 , 2 for horizontal swipe
# If the swipe is vertical will return 3, 4
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


class Logic:
    CHASER_SLOWER = 10
    # MAX_SWIPE_DELAY = 250  # ms

    def __init__(self, data, touch):
        self.data = data
        self.__dict__.update(data)
        self.max_score = self.level * rows * cols
        self.run = True
        self.touch = touch

    async def move_player(self,):
        while self.run:
            clock.tick(FPS)
            await asyncio.sleep(0)

            if self.paused:
                continue

            # on pc, use keys
            if not self.touch:
                self.player.move()

            # on mobile, use touch
            else:
                for move in self.player.get_moves():
                    if move in self.swipes:
                        ind = self.swipes.index(move)
                        self.swipes = self.swipes[ind:]
                        self.player.move(move)

        return

    async def mainloop(self,):
        count = 0
        while self.run:
            clock.tick(FPS)
            await asyncio.sleep(0)

            if self.paused:
                continue

            count += 1

            payload = self.player.forward(GRID)
            defeat = payload.get("defeat")

            if defeat:
                self.defeat = True
                self.run = False
                break

            self.score += (
                payload.get("score_gained") if payload.get("score_gained") else 0
            ) * self.level

            if self.score > highscore:
                change_highscore(self.score)

            if self.score >= self.max_score:
                self.victory = True
                self.run = False
                break

            if count % self.CHASER_SLOWER == 0:
                for ind, c in enumerate(self.chasers):
                    payload = c.move(GRID, self.player.host)
                    new_chaser = payload.get("chaser")
                    defeat = payload.get("defeat")
                    if defeat:
                        self.defeat = True
                        self.run = False
                        break

                    elif new_chaser:
                        self.chasers[ind] = new_chaser

                count = 0

        return

    def stop(self):
        self.game_over = True
        self.run = False


# creates maze and then starts game
async def main(player, chasers, level):
    global FPS
    run = True  # WHILE THIS IS TRUE THE MAIN LOOP WILL RUN

    pygame.display.set_caption("Creating Maze...")
    print("Creating Maze...")

    # CREATE THE MAZE
    maze_algorithm()
    make_easy(75)  # randomly remove a few walls
    draw_grid(player, force=True, fill=True)

    pygame.display.set_caption("Hit space to start game.")
    print("Maze Created...Hit space to start game.")
    maze_created = True
    touch = False

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
                if maze_created:  # and event.key == pygame.K_SPACE:
                    run = False
                    break
            #  IF THE USERS CLICKS ON THE SCREEN PROCEED
            if event.type == pygame.MOUSEBUTTONUP:
                if maze_created:  # and event.key == pygame.K_SPACE:
                    touch = event.touch
                    if touch:
                        FPS = 30
                    run = False
                    break

        await asyncio.sleep(0)
    await game(player, chasers, level, touch)


# all the game logic
async def game(player, chasers, level, touch):
    run = True

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
    pygame.display.set_caption(f"Level: {len(chasers)}")
    print("Game started.")

    data = {
        "swipes": [],
        "paused": False,
        "defeat": False,
        "game_over": False,
        "player": player,
        "chasers": chasers,
        "score": 0,
        "victory": False,
        "level": level,
    }

    logic = Logic(data, touch)
    main_logic = Thread(
        target=asyncio.run, name="main-logic", args=(logic.mainloop(),), daemon=True
    )
    player_logic = Thread(
        target=asyncio.run,
        name="player-logic",
        args=(logic.move_player(),),
        daemon=True,
    )

    main_logic.start()
    player_logic.start()

    while run:
        clock.tick(FPS)
        await asyncio.sleep(0)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                print("Quit via user interruption")
                logic.stop()
                pygame.quit()
                quit()

            if e.type == pygame.MOUSEMOTION:
                if e.touch:
                    logic.swipes.append(getSwipeType(e.rel))

            if pause_play.check_event(e):
                paused = not paused
                logic.paused = paused
                pause_play.image = play_img if paused else pause_img

            if restart_button.check_event(e):
                logic.stop()
                return await main(*restart(level))

        pause_play.update(WIN)
        restart_button.update(WIN)
        write_text(
            scoreFont, YELLOW, f"Score: {logic.score}", 10, 10, True,
        )

        draw_grid(player=player, chasers=chasers, update=False)

        if logic.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN] or pygame.mouse.get_pressed()[0]:
                return await main(*restart(level))

        elif paused:
            continue

        elif logic.victory:
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
            logic.stop()

        elif logic.defeat:
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
            logic.stop()

        pygame.display.update()


if __name__ == "__main__":
    asyncio.run(main(*restart()))
