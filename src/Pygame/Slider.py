import pygame
import pygame.gfxdraw
from MathUtil import clamp
import Pygame.GlobalVariables as GVar
from time import time

class Slider:

    surface = None
    coords = [0, 0]
    surfaceToDraw = None
    length = 0
    lineColor = (0, 0, 0)
    sliderColor = (0, 0, 0)
    sliderColorInit = (0, 0, 0)
    sliderDraggedColor = (0, 0, 0)
    lineColorFilled = (0, 0, 0)

    surfHeight = 20

    sliderPos = 0 # Position of the slider in the x axis, relative to value.
    sliderRadius = 10

    value = 0

    _dragged = False

    def __init__(self, surface, coords, length, initValue=50, lineColor=(220, 220, 230), lineColorFilled=(165, 198, 230), sliderColor=(46, 119, 230), sliderDraggedColor=(58, 158, 240)):
        self.coords = coords
        self.surfaceToDraw = surface
        self.length = length
        self.lineColor = lineColor
        self.sliderColorInit = sliderColor
        self.sliderDraggedColor = sliderDraggedColor
        self.sliderColor = sliderColor
        self.lineColorFilled = lineColorFilled

        self.value = clamp(initValue, 0, 100)
        self.sliderPos = round((initValue / 100 * length) + self.sliderRadius)

        self.surface = pygame.Surface([self.length + (self.sliderRadius * 2) + 2, self.surfHeight + 2], pygame.SRCALPHA) # Draws surface

        self.redrawSurface()

    def redrawSurface(self):
        self.surface.fill((255, 255, 255, 0)) # Clears surface
        pygame.draw.line(self.surface, self.lineColor, (self.sliderRadius, self.surfHeight/2), (self.length + self.sliderRadius, self.surfHeight/2), 4) # Draws slider line
        pygame.draw.line(self.surface, self.lineColorFilled, (self.sliderRadius, self.surfHeight/2), (self.sliderPos, self.surfHeight/2), 4) # Draws slider line filler
        pygame.gfxdraw.aacircle(self.surface, round(self.sliderPos), self.surfHeight//2, self.sliderRadius, self.sliderColor) # Draws circle anti-aliased outline.
        pygame.gfxdraw.filled_circle(self.surface, round(self.sliderPos), self.surfHeight//2, self.sliderRadius, self.sliderColor) # Draws circle

    def getValue(self):
        return value

    def update(self):
        
        if (GVar.mouseState[0] == 1):
            # Checks whether the mouse cursor is at the slider's "ball"
            if (((self.coords[0] + self.sliderPos - self.sliderRadius) < GVar.mousePos[0] and (self.coords[0] + self.sliderPos + self.sliderRadius) > GVar.mousePos[0]) and 
             (self.coords[1] + (self.surfHeight/2) - self.sliderRadius) < GVar.mousePos[1] and (self.coords[1] + (self.surfHeight/2) + self.sliderRadius) > GVar.mousePos[1] ):
                self._dragged = True
        elif (self._dragged):
            self._dragged = False
            self.sliderColor = self.sliderColorInit
            self.redrawSurface()

        if (self._dragged):
            self.sliderPos = clamp(GVar.mousePos[0] - self.coords[0], self.sliderRadius, self.length + self.sliderRadius)
            self.value = (self.sliderPos - self.sliderRadius) / self.length
            self.sliderColor = self.sliderDraggedColor
            self.redrawSurface()


        self.surfaceToDraw.blit(self.surface, self.coords)