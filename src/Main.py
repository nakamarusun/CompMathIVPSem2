import MathUtil
import sys
import pygame
import pygame.display
import pygame.draw

pygame.init()

resolution = [800, 600]
mainScreenBuffer = pygame.display.set_mode(resolution, pygame.RESIZABLE)

pygame.display.set_caption("Initial Value Problems Visualization")

from Pygame.Updater import updateAll

while True:

    # Preliminary event getter
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            resolution = [event.w, event.h]
            mainScreenBuffer = pygame.display.set_mode(resolution, pygame.RESIZABLE)

    # Clears the mainScreen Buffer
    mainScreenBuffer.fill( (255, 255, 255) )

    # Main operations
    updateAll()




    # End of main operations

    # Updates the display
    pygame.display.flip()