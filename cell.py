from constants import *
import random
from path_finding import bfs

# Class Cell. Every element in the grid is a Cell
class Cell:
    def __init__(self, row, col, width_buffer=0, height_buffer=0):
        self.row = row  # ROW NUMBER
        self.col = col  # COLUMN NUMBER
        self.y = row * WIDTH + height_buffer  # POSITION X COORDINATE
        self.x = col * WIDTH + width_buffer  # POSITION Y COORDINATE

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

        # is this cell the player or the chaser?
        self.playerHost = False
        self.chaserHost = False
        self.point = True
        self.chaserImg = None

        self._show = False

    def reinit(self):
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
        self.chaserImg = None
        self._show = False

    # THIS FUNCTION CHECKS ALL UNVISITED NEIGHBOURS OF A CELL AND RETURNS A RANDOM ONE IF IT DOES
    def get_neighbour(self, grid):
        neighbours = (
            []
        )  # A LIST NEIGHBOURS. TO TEMPORARILY STORE ALL NEIGHBOURS OF A GIVEN CELL

        # THIS PART IS FOR THE MAZE MAKING...HERE THE NEIGHBOURS OF A GIVEN CELL ARE THOSE CELLS WHICH SURROUND IT (TOP,BOTTOM,LEFT,RIGHT)
        # AND ARE NOT YET VISITED
        # WALLS IN BETWEEN NEIGHBOURS ARE NOT CONSIDERED
        # IF THE GIVEN CELL IS NOT THE IN FIRST ROW AND HAS A NON VISITED NEIGHBOUR ABOVE IT, APPEND IT TO NEIGHBOURS
        if (
            0 < self.row
            and not grid[self.row - 1][self.col].visited
            and not grid[self.row - 1][self.col].blank
        ):
            neighbours.append(grid[self.row - 1][self.col])  # top

        # IF THE GIVEN CELL IS NOT THE IN LAST ROW AND HAS A NON VISITED NEIGHBOUR BELOW IT, APPEND IT TO NEIGHBOURS
        if (
            rows - 1 > self.row
            and not grid[self.row + 1][self.col].visited
            and not grid[self.row + 1][self.col].blank
        ):
            neighbours.append(grid[self.row + 1][self.col])  # bottom

        # IF THE GIVEN CELL IS NOT THE IN FIRST COLUMN AND HAS A NON VISITED NEIGHBOUR TO THE LEFT OF IT, APPEND IT TO NEIGHBOURS
        if (
            0 < self.col
            and not grid[self.row][self.col - 1].visited
            and not grid[self.row][self.col - 1].blank
        ):
            neighbours.append(grid[self.row][self.col - 1])  # left

        # IF THE GIVEN CELL IS NOT THE IN LAST COLUMN AND HAS A NON VISITED NEIGHBOUR TO THE RIGHT OF IT, APPEND IT TO NEIGHBOURS
        if (
            cols - 1 > self.col
            and not grid[self.row][self.col + 1].visited
            and not grid[self.row][self.col + 1].blank
        ):
            neighbours.append(grid[self.row][self.col + 1])  # right

        # IF THERE ARE ANY NEIGHBOURS FOR A GIVEN CELL, THEN RETURN A RANDOM ONE, TO RANDOMISE THE FORMATION OF THE MAZE
        if len(neighbours) > 0:
            return neighbours[random.randint(0, len(neighbours) - 1)]
        # IF THERE ARE NO NEIGHBOURS THAT ARE UNVISITED RETURN FALSE
        return False

    # get all unsearched neighbors for path finding
    def get_unsearched_neighbour(self, grid, searched):
        neighbours = (
            []
        )  # A LIST NEIGHBOURS. TO TEMPORARILY STORE ALL NEIGHBOURS OF A GIVEN CELL

        # THIS PART IS FOR THE PATH FINDING...HERE THE NEIGHBOURS OF A CELL ARE THOSE THAT SURROUND IT
        # AND ARE NOT YET SEARCHED
        # AND THERE MUST BE NO WALL BETWEEN THE TWO NEIGHBOURS

        # IF THERE IS A RIGHT NEIGHBOUR THAT SATISFIES THE CONDITIONS APPEND IT
        if not self.right and grid[self.row][self.col + 1] not in searched:
            neighbours.append(grid[self.row][self.col + 1])  # right

        # IF THERE IS A BOTTOM NEIGHBOUR THAT SATISFIES THE CONDITIONS APPEND IT
        if not self.bottom and grid[self.row + 1][self.col] not in searched:
            neighbours.append(grid[self.row + 1][self.col])  # bottom

        # IF THERE IS A LEFT NEIGHBOUR THAT SATISFIES THE CONDITIONS APPEND IT
        if not self.left and grid[self.row][self.col - 1] not in searched:
            neighbours.append(grid[self.row][self.col - 1])  # left

        # IF THERE IS A TOP NEIGHBOUR THAT SATISFIES THE CONDITIONS APPEND IT
        if not self.top and grid[self.row - 1][self.col] not in searched:
            neighbours.append(grid[self.row - 1][self.col])  # top

        if len(neighbours) > 0:
            return neighbours

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

    # make it a chaser
    def make_chaser(self, img):
        self.chaserHost = True
        self.chaserImg = img

    # make player
    def make_player_host(self):
        self.playerHost = True

    # HIGHLIGHT ANY CELL FOR DEBUGGING
    def highlight(self, win):
        pygame.draw.rect(win, self.highlight_color, (self.x, self.y, WIDTH, WIDTH), 0)
        pygame.display.update()

    # logic to move player or chaser
    def move(self, grid, player_host):

        if self.playerHost and self.chaserHost:
            return {"defeat": True}  # game over

        # logic for moving chaser
        elif self.chaserHost:
            new_chaser = bfs(self, player_host, grid)

            # dont want both chasers to merge
            if not new_chaser.chaserHost:
                self.chaserHost = False
                new_chaser.make_chaser(self.chaserImg)
                self.chaserImg = None
                self.show()
                new_chaser.show()

                return {"chaser": new_chaser}
            return {"chaser": self}

    def show_(self, win, force=False):
        if self._show or force:
            # DRAW A RECTANGLE WITH THE DIMENSIONS OF THE CELL, TO COLOR IT
            pygame.draw.rect(win, self.color, (self.x, self.y, WIDTH, WIDTH), 0)

            # DRAW RIGHT, LEFT, TOP, BOTTOM WALLS
            if self.right:  # RIGHT
                pygame.draw.line(
                    win,
                    self.line_color,
                    (self.x + WIDTH, self.y),
                    (self.x + WIDTH, self.y + WIDTH),
                    width=wallwidth,
                )
            if self.left:  # LEFT
                pygame.draw.line(
                    win,
                    self.line_color,
                    (self.x, self.y),
                    (self.x, self.y + WIDTH),
                    width=wallwidth,
                )
            if self.top:  # TOP
                pygame.draw.line(
                    win,
                    self.line_color,
                    (self.x, self.y),
                    (self.x + WIDTH, self.y),
                    width=wallwidth,
                )
            if self.bottom:  # BOTTOM
                pygame.draw.line(
                    win,
                    self.line_color,
                    (self.x, self.y + WIDTH),
                    (self.x + WIDTH, self.y + WIDTH),
                    width=wallwidth,
                )

            # draw appropriate images
            if self.point:
                pygame.draw.circle(
                    win, KHAKI, (self.x + WIDTH // 2, self.y + WIDTH // 2), pointRadius
                )
            if self.chaserHost:
                win.blit(self.chaserImg, (self.x + WIDTH // 4, self.y + WIDTH // 4))

            self._show = False

    # THIS FUNCTION SHOWS THE CELL ON PYGAME WINDOW
    def show(self):
        self._show = True


# Player
class Player(Cell):
    def __init__(self, host, row, col, width_buffer, height_buffer):
        super().__init__(row, col, width_buffer, height_buffer)
        self.direction = 1
        self.host = host
        self.playerImg = playerR

    def forward(
        self, grid,
    ):

        score_inc = 0

        if self.host.point:
            self.host.point = False
            score_inc += 1

        self.host.show()

        if self.host.chaserHost:
            return {"defeat": True}

        self.host.playerHost = False
        new_host = self.host

        if self.direction == 1 and not self.host.right:
            new_host = grid[self.row][self.col + 1]
        elif self.direction == 2 and not self.host.left:
            new_host = grid[self.row][self.col - 1]
        elif self.direction == 3 and not self.host.bottom:
            new_host = grid[self.row + 1][self.col]
        elif self.direction == 4 and not self.host.top:
            new_host = grid[self.row - 1][self.col]

        self.change_host(new_host)
        new_host.make_player_host()
        new_host.show()
        self.show()

        return {"score_gained": score_inc}

    def change_host(self, host):
        self.host = host
        self.x, self.y = host.x, host.y
        self.row, self.col = host.row, host.col

    def move(self, move=0):
        # logic for moving player
        if (move == 1) and not self.host.right:
            self.direction = 1
            self.playerImg = playerR

        elif (move == 2) and not self.host.left:
            self.direction = 2
            self.playerImg = playerL

        elif (move == 3) and not self.host.bottom:
            self.direction = 3
            self.playerImg = playerD

        elif (move == 4) and not self.host.top:
            self.direction = 4
            self.playerImg = playerU

    def get_moves(self):
        if not self.host.right:
            yield 1
        if not self.host.left:
            yield 2
        if not self.host.bottom:
            yield 3
        if not self.host.top:
            yield 4

    def show_(self, win, force=False):
        if self._show or force:
            win.blit(self.playerImg, (self.x + WIDTH // 4, self.y + WIDTH // 4))
            self._show = False

