import Pygame.GlobalVariables as GVar
import pygame

class TextLabel:

    coords = [0, 0]
    surfaceToDraw = None
    text = ""
    font = None

    textColor = (0, 0, 0)

    surface = None

    def __init__(self, surface, text, coords, font=GVar.defFont, textColor=(0, 0, 0)):
        self.coords = coords
        self.surfaceToDraw = surface
        self.text = text
        self.font = font

        self.textColor = textColor

        self.redrawSurface()

    def redrawSurface(self):
        self.surface = pygame.Surface(self.font.size(self.text), pygame.SRCALPHA) # Recreate surface with the text size
        self.surface.blit(self.font.render(self.text, True, self.textColor), [0, 0]) # Renders the text to surface

    def changeText(self, newText):
        self.text = newText
        self.redrawSurface()

    def update(self):
        self.surfaceToDraw.blit(self.surface, self.coords)