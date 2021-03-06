import pygame
import pygame.font

pygame.font.init()

resolution = [800, 600]
# defFont = pygame.font.Font(pygame.font.get_default_font(), 12)
defFont = pygame.font.SysFont("Calibri", 14, False, False, None)
defFontBold = pygame.font.SysFont("Calibri", 14, True, False, None)
defFont18 = pygame.font.SysFont("Calibri", 18, False, False, None)
defFont24 = pygame.font.SysFont("Calibri", 24, False, False, None)
defFont18Bold = pygame.font.SysFont("Calibri", 18, True, False, None)

defFont24Bold = pygame.font.SysFont("Calibri", 24, True, False, None)

mainScreenBuffer = None
isVideoResized = False

mousePos = [0, 0]
mouseState = [0, 0, 0]
mouseStateSingle = [0, 0, 0]

events = []

framesSinceStart = 0

divisionByZero = False

def update():

    global mousePos
    global mouseState
    global mouseStateSingle
    global isVideoResized
    global divisionByZero

    isVideoResized = False
    divisionByZero = False
    mousePos = pygame.mouse.get_pos()

    tempMouseState = pygame.mouse.get_pressed()
    # Get mouseStateSingle
    for i in range(len(tempMouseState)):
        if (tempMouseState[i] == 1 and mouseState[i] == 0):
            mouseStateSingle[i] = 1
        else:
            mouseStateSingle[i] = 0

    mouseState = tempMouseState