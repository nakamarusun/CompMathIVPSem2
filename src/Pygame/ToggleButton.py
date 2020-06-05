import pygame
import Pygame.GlobalVariables as GVar
from Pygame.Button import AAfilledRoundedRect, Button

buttonList = []

# Function to draw a rounded rectangle
class ToggleButton(Button):

    toggleColor = (125, 125, 125)

    toggled = False

    def __init__(self, funcToRun, surface, coords, text, font, size, color, hoverAnim=False, hoverColor=(0, 0, 0), toggleColor=(125, 125, 125)):
        self.toggleColor = toggleColor
        super().__init__(funcToRun, surface, coords, text, font, size, color, hoverAnim, hoverColor)

    def update(self):
        super().update()
        if (self.pressed):
            self.color = self.toggleColor
            self.redrawButton()

    def isToggled(self):
        return self.pressed