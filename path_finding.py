from queue import Queue as fifo
from checkquit import CheckQuit

# path finding - bfs is ideal for maze
def bfs(start_cell, end_cell, grid):
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
        neighbours = root.get_unsearched_neighbour(grid, searched)
        if neighbours:
            for n in neighbours:
                searched.append(n)
                track[n] = root
                Q.put(n)
