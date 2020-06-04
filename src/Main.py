import MathUtil
import sys
import pygame
import pygame.display
import pygame.draw
import Pygame.GlobalVariables as GVar

# Initialize the pygame engine.
pygame.init()

GVar.mainScreenBuffer = pygame.display.set_mode(GVar.resolution, pygame.RESIZABLE)

# Sets caption in the title bar
pygame.display.set_caption("Initial Value Problems Visualization")

import Pygame.Updater as Updater
import Pygame.MathRoom as MathRoom

# Initialize main room in the display
MathRoom.initRoom()

while True:

    # Update global variables
    GVar.update()

    # Preliminary event getter
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            GVar.isVideoResized = True
            GVar.resolution = [event.w, event.h]
            GVar.mainScreenBuffer = pygame.display.set_mode(GVar.resolution, pygame.RESIZABLE)

    # Clears the mainScreen Buffer
    GVar.mainScreenBuffer.fill( (255, 255, 255) )

    # Main operations
    Updater.updateAll()


    # End of main operations

    # Updates the display
    pygame.display.flip()