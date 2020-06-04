import Pygame.GlobalVariables as GVar
import Pygame.Updater as Updater
import pygame
import pygame.draw
from Pygame.Button import Button
from Pygame.Slider import Slider
from Pygame.TextField import TextField


class CanvasSurface():

    ratio = []
    functionCanvasSurface = None

    def __init__(self):
        self.ratio = (0.85, 0.7) # The ratio of the size of the functionCanvasSurface compared to the main screen

        # Creates a new function canvas surface with 85% width size and 50% height size
        self.functionCanvasSurface = pygame.Surface((GVar.resolution[0] * self.ratio[0], GVar.resolution[1] * self.ratio[1]))

    def update(self):
        if (GVar.isVideoResized):
            self.functionCanvasSurface = pygame.Surface((GVar.resolution[0] * self.ratio[0], GVar.resolution[1] * self.ratio[1])) # If program is resized, change the size of the canvas surface
        
        self.functionCanvasSurface.fill((255, 255, 255)) # Clears the surface with white
        pygame.draw.rect(self.functionCanvasSurface, (0, 0, 0), self.functionCanvasSurface.get_rect(), 1) # Puts a white border in the canvas
        # Do all drawing here



        # Drawing end
        GVar.mainScreenBuffer.blit(self.functionCanvasSurface, [(GVar.resolution[0] / 2) - (GVar.resolution[0] * self.ratio[0] / 2), 50]) # Draws into the main screen buffer in the middle.

class MainSurface():

    interactableList = []

    def __init__(self):
        self.interactableList = [] # Initiates interactableList
        # Adds all of the button
        self.interactableList.append(Button(lambda : print("Button Clicked"), GVar.mainScreenBuffer, [100, 100], "yes", GVar.defFont, [150, 100], (255, 0, 0), True))
        self.interactableList.append(Slider(GVar.mainScreenBuffer, [300, 200], 300))
        self.interactableList.append(TextField(GVar.mainScreenBuffer, 300, [400, 300], GVar.defFont))

    def update(self):
        # Draws buttons and detects any button press
        for interactable in self.interactableList:
            interactable.update()

def initRoom():
    Updater.insertUpdate(CanvasSurface())
    Updater.insertUpdate(MainSurface())