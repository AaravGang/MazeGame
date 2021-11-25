import pygame

# A FUNCTION TO CHECK IF THE USER WANTS TO QUIT PYGAME
def CheckQuit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Quit via user interruption")
            pygame.quit()
            quit()
