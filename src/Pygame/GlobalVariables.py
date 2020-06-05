import pygame
import pygame.font

pygame.font.init()

resolution = [800, 600]
# defFont = pygame.font.Font(pygame.font.get_default_font(), 12)
defFont = pygame.font.SysFont("Calibri", 14, False, False, None)

mainScreenBuffer = None
isVideoResized = False

mousePos = [0, 0]
mouseState = [0, 0, 0]
mouseStateSingle = [0, 0, 0]

events = []

framesSinceStart = 0

def update():

    global mousePos
    global mouseState
    global mouseStateSingle

    isVideoResized = False
    mousePos = pygame.mouse.get_pos()

    tempMouseState = pygame.mouse.get_pressed()
    # Get mouseStateSingle
    for i in range(len(tempMouseState)):
        if (tempMouseState[i] == 1 and mouseState[i] == 0):
            mouseStateSingle[i] = 1
        else:
            mouseStateSingle[i] = 0

    mouseState = tempMouseState