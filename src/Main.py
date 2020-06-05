import MathUtil
import sys
import pygame
import pygame.display
import pygame.draw
import Pygame.GlobalVariables as GVar
from time import time, sleep

# Initialize the pygame engine.
pygame.init()

GVar.mainScreenBuffer = pygame.display.set_mode(GVar.resolution, pygame.RESIZABLE)

# Sets caption in the title bar
pygame.display.set_caption("Initial Value Problems Visualization")

import Pygame.Updater as Updater
import Pygame.MathRoom as MathRoom

# Initialize main room in the display
MathRoom.initRoom()

fpsLock = 60

while True:

    startTime = time()

    # Update global variables
    GVar.update()

    # Preliminary event getter
    GVar.events = pygame.event.get() # Puts into variable for easy access by other files
    for event in GVar.events:
        # Quit event
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Resize event
        if event.type == pygame.VIDEORESIZE:
            GVar.isVideoResized = True
            GVar.resolution = [MathUtil.clamp(event.w, 400, 20000), MathUtil.clamp(event.h, 300, 20000 )]
            GVar.mainScreenBuffer = pygame.display.set_mode(GVar.resolution, pygame.RESIZABLE)

    # Clears the mainScreen Buffer
    GVar.mainScreenBuffer.fill( (255, 255, 255) )

    # Main operations
    Updater.updateAll()

    # End of main operations

    # Updates the display
    pygame.display.flip()

    # Function to lock fps to 60, to save lots of processing power
    deltaFrame = (time() - startTime) # Time to process one frame
    # print(1/deltaFrame if deltaFrame != 0 else "inf") # Uncomment to show fps
    oneFrame = (1 / fpsLock) - deltaFrame if (1 / fpsLock) - deltaFrame > 0 else 0 # Clamps sleep value not to be below 0
    if (oneFrame != 0):
        pygame.time.wait(round(oneFrame * 1000))

    GVar.framesSinceStart += 1 # Adds frames since start by 1