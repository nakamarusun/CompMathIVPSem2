import Pygame.GlobalVariables as GVar
import Pygame.Updater as Updater
import pygame
import pygame.draw
from Pygame.Button import Button
from Pygame.Slider import Slider
from Pygame.TextField import TextField
from Pygame.TextLabel import TextLabel
from Pygame.ToggleButton import ToggleButton


class CanvasSurface():

    ratio = []
    functionCanvasSurface = None

    def __init__(self):
        self.ratio = (0.85, 0.7) # The ratio of the size of the functionCanvasSurface compared to the main screen
        self.redrawSurface()

    def redrawSurface(self):
        # Creates a new function canvas surface with 85% width size and 50% height size
        self.functionCanvasSurface = pygame.Surface((GVar.resolution[0] * self.ratio[0], GVar.resolution[1] * self.ratio[1]))
        self.functionCanvasSurface.fill((255, 255, 255)) # Clears the surface with white
        pygame.draw.rect(self.functionCanvasSurface, (0, 0, 0), self.functionCanvasSurface.get_rect(), 1) # Puts a white border in the canvas
        # Do all drawing here

    def update(self):
        if (GVar.isVideoResized):
            self.redrawSurface() # If program is resized, change the size of the canvas surface

        # Drawing end
        GVar.mainScreenBuffer.blit(self.functionCanvasSurface, [(GVar.resolution[0] / 2) - (GVar.resolution[0] * self.ratio[0] / 2), GVar.resolution[1] * 0.1]) # Draws into the main screen buffer in the middle.

class MainSurface():

    interactableList = []

    def __init__(self):
        self.redrawAll()

        # Samples
        # self.interactableList.append(Button(lambda : print("Button Clicked"), GVar.mainScreenBuffer, [100, 100], "yes", GVar.defFont, [150, 100], (255, 0, 0), True))
        # self.interactableList.append(Slider(GVar.mainScreenBuffer, [300, 200], 300))
        # self.interactableList.append(TextField(lambda : print("Enter Clicked"), GVar.mainScreenBuffer, 300, [400, 300], GVar.defFont))
        
    def redrawAll(self):
        self.interactableList = []

        # Sliders
        self.interactableList.append(Slider(GVar.mainScreenBuffer, [GVar.resolution[0] * 0.075, GVar.resolution[1] * 0.84], GVar.resolution[0] * 0.3, 50, (191, 233, 245), (141, 202, 235))) # Delta X Slider
        self.interactableList.append(Slider(GVar.mainScreenBuffer, [GVar.resolution[0] * 0.075, GVar.resolution[1] * 0.91], GVar.resolution[0] * 0.3, 20, (252, 215, 251), (220, 141, 235), (142, 47, 189), (185, 51, 222))) # Until X Slider

        # Slider Text
        self.interactableList.append(TextLabel(GVar.mainScreenBuffer, "Delta X:", [GVar.resolution[0] * 0.075, GVar.resolution[1] * 0.82])) # Delta X Text
        self.interactableList.append(TextLabel(GVar.mainScreenBuffer, "Until X:", [GVar.resolution[0] * 0.075, GVar.resolution[1] * 0.89])) # Until X Text

        # Slider TextField
        self.interactableList.append(TextField(lambda : print("Pressed"),
         GVar.mainScreenBuffer, 65, [GVar.resolution[0] * 0.4, GVar.resolution[1] * 0.84 - 3], GVar.defFont)) # Delta X TextField
        self.interactableList.append(TextField(lambda : print("Pressed"),
         GVar.mainScreenBuffer, 65, [GVar.resolution[0] * 0.4, GVar.resolution[1] * 0.91 - 3], GVar.defFont)) # Until X TextField

        # Function Text
        self.interactableList.append(TextLabel(GVar.mainScreenBuffer, "Function:", [GVar.resolution[0] * 0.51, GVar.resolution[1] * 0.84 - 2], GVar.defFont18Bold))

        # Function TextField
        self.interactableList.append(TextField(lambda : print("Pressed"),
         GVar.mainScreenBuffer, GVar.resolution[0] * 0.285, [GVar.resolution[0] * 0.64, GVar.resolution[1] * 0.84 - 9], GVar.defFont18))

        # Initial y Text
        self.interactableList.append(TextLabel(GVar.mainScreenBuffer, "y(0):", [GVar.resolution[0] * 0.51, GVar.resolution[1] * 0.91 - 2], GVar.defFont18))

        # Initial y TextField
        self.interactableList.append(TextField(lambda : print("Pressed"),
         GVar.mainScreenBuffer, GVar.resolution[0] * 0.075, [GVar.resolution[0] * 0.56, GVar.resolution[1] * 0.91 - 9], GVar.defFont18))

        # Calculate Button
        self.interactableList.append(Button(lambda : print("Calculated"),
         GVar.mainScreenBuffer, [GVar.resolution[0] * 0.8, GVar.resolution[1] * 0.91 - 9], "CALCULATE", GVar.defFont, [GVar.resolution[0] * 0.125, 29], (219, 42, 110), True, (227, 64, 145)))



    def update(self):
        if (GVar.isVideoResized):
            self.redrawAll()
        # Draws buttons and detects any button press
        for interactable in self.interactableList:
            interactable.update()

def initRoom():
    Updater.insertUpdate(CanvasSurface())
    Updater.insertUpdate(MainSurface())