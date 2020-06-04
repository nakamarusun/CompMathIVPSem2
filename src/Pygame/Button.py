import pygame
import Pygame.GlobalVariables as GVar

buttonList = []

# Function to draw a rounded rectangle
def AAfilledRoundedRect(surface,rect,color,radius=0.4):

    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect         = pygame.Rect(rect)
    color        = pygame.Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = pygame.Surface(rect.size, pygame.SRCALPHA)

    circle       = pygame.Surface([min(rect.size)*3]*2,pygame.SRCALPHA)
    pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=pygame.BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=pygame.BLEND_RGBA_MIN)

    return surface.blit(rectangle,pos)

class Button:

    text = ""
    size = []
    color = []
    coords = []
    font = None
    surfaceToDraw = None

    surface = None

    def __init__(self, surface, coords, text, font, size, color):
        self.text = text
        self.size = size
        self.color = color
        self.coords = coords
        self.font = font
        self.surfaceToDraw = surface

        self.redrawButton()

    def redrawButton(self):
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        AAfilledRoundedRect(self.surface, self.surface.get_rect(), self.color, 0.3) # Draws button rectangle.
        textSurf = self.font.render(self.text, True, (255, 255, 255))
        self.surface.blit(textSurf, ((self.size[0] / 2) - (textSurf.get_rect().width / 2), (self.size[1] / 2) - (textSurf.get_rect().height / 2))) # Draws text in the middle

    def update(self):
        self.surfaceToDraw.blit(self.surface, self.coords) # Draw to screen