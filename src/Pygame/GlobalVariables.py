import pygame.font

pygame.font.init()

resolution = [800, 600]
defFont = pygame.font.Font(pygame.font.get_default_font(), 14)

mainScreenBuffer = None

isVideoResized = False

def update():
    isVideoResized = False