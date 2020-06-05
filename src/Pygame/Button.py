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
    initColor = (255, 255, 255)
    color = (255, 255, 255)
    coords = []
    font = None
    surfaceToDraw = None
    funcToRun = None

    hoverAnim = False
    hoverColor = (0, 0, 0)

    surface = None

    _updated = False

    hovered = False

    pressed = False

    def __init__(self, funcToRun, surface, coords, text, font, size, color, hoverAnim=False, hoverColor=(0, 0, 0)):
        self.text = text
        self.size = size
        self.initColor = color
        self.coords = coords
        self.font = font
        self.surfaceToDraw = surface
        self.hoverColor = hoverColor
        self.funcToRun = funcToRun
        self.hoverAnim = hoverAnim

        self.color = color
        
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)

        self.redrawButton()

    def redrawButton(self):
        self.surface.fill((255, 255, 255, 0))
        AAfilledRoundedRect(self.surface, self.surface.get_rect(), self.color, 0.3) # Draws button rectangle.
        textSurf = self.font.render(self.text, True, (255, 255, 255))
        self.surface.blit(textSurf, ((self.size[0] / 2) - (textSurf.get_rect().width / 2), (self.size[1] / 2) - (textSurf.get_rect().height / 2))) # Draws text in the middle

    def update(self):

        self._updated = False

        if (self.hoverAnim or GVar.mouseStateSingle[0] == 1):
            # Checks if mouse hovers over the button
            mousePos = GVar.mousePos
            if ((mousePos[0] > self.coords[0] and mousePos[0] < (self.coords[0] + self.size[0])) and (mousePos[1] > self.coords[1] and mousePos[1] < (self.coords[1] + self.size[1]))):
                if (not self.hovered):
                    self._updated = True
                self.hovered = True

                if (GVar.mouseStateSingle[0] == 1):
                    # Do action when clicked
                    self.funcToRun()
                    self.pressed = not self.pressed
            else:
                if (self.hovered):
                    self._updated = True
                self.hovered = False

        # Do on hover actions
        if (self.hoverAnim):
            if (self._updated and self.hovered):
                self.color = self.hoverColor
                self.redrawButton()

            elif (self._updated and (not self.hovered)):
                self.color = self.initColor
                self.redrawButton()

        self.surfaceToDraw.blit(self.surface, self.coords) # Draw to screen