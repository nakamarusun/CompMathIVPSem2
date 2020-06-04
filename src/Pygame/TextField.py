import pygame
import Pygame.GlobalVariables as GVar
import math
from MathUtil import clamp
from time import time

class TextField:

    coords = [0, 0]
    length = 0
    font = None
    surfaceToDraw = None
    backgroundColor = (255, 255 ,255)
    textColor = (0, 0, 0)
    size = [0, 0] # Size of the text field

    margin = [0, 0] # Margin of the text compared to the rest of the text of the field

    text = "" # Text inside of the field
    cursorPos = 0 # The position of the typing cursor

    _active = False # Whether you can type on the textfield or not.

    cursorBlinkSpeed = 1000 # Cursor blink speed in miliseconds

    textPosition = 0 # First character position in the text field, to make the text wrapping work.

    xCursorPos = 0 # Position of the cursor in the x axis

    def __init__(self, surface, length, coords, font, backgroundColor=(240, 240, 240), textColor=(0, 0, 0), margin=[5,5]):

        self.length = length
        self.coords = coords
        self.font = font
        self.backgroundColor = backgroundColor
        self.surfaceToDraw = surface
        self.textColor = textColor
        self.margin = margin

        self.cursorPos = 0
        
        self.size = [length, self.font.get_height() + margin[1]*2]

        self.surface = pygame.Surface(self.size) # Draws surface
        
        self.redrawSurface()

    def redrawSurface(self):

        self.surface.fill(self.backgroundColor) # Clears the surface to be the background color
        pygame.draw.rect(self.surface, (0, 0, 0), self.surface.get_rect(), 1) # Puts a black border in the textField
        self.surface.blit(self.font.render(self.text, True, self.textColor), [self.margin[0] + self.textPosition, self.margin[1]]) # puts the text

    def update(self):

        if (GVar.mouseStateSingle[0] == 1):
            mousePos = GVar.mousePos
            if ((mousePos[0] > self.coords[0] and mousePos[0] < (self.coords[0] + self.size[0])) and (mousePos[1] > self.coords[1] and mousePos[1] < (self.coords[1] + self.size[1]))):
                # If mouse is clicked, and mouse is in the bounds of the textfield
                self._active = True
                # Where the mouse clicks, translate into cursor position
            else:
                self._active = False

        if (self._active):

            blink = bool((time() // (self.cursorBlinkSpeed / 1000)) % 2)

            # If the textfield is active, then listen for keyboard strokes
            for event in GVar.events:
                if (event.type == pygame.KEYDOWN):
                    if (event.unicode == '\x08'): # If the unicode is backspace then
                        if (len(self.text) != 0): # Checks if there is something in the text
                            self.text = self.text[0:self.cursorPos-1] + self.text[self.cursorPos:] # Deletes the text based on where the cursor position is.
                            self.cursorPos -= 1
                    elif (event.key == pygame.K_LEFT): # Moves cursor to the left
                        self.cursorPos = clamp(self.cursorPos - 1, 0, len(self.text))
                        # self.textPosition = clamp(0, -math.inf, 0)
                    elif (event.key == pygame.K_RIGHT): # Moves cursor to the right
                        self.cursorPos = clamp(self.cursorPos + 1, 0, len(self.text))
                    elif (event.unicode != ''): # If unicode is not empty then
                        self.text += event.unicode
                        self.cursorPos += 1
                    blink = True # Sets blink to true if any key is pressed
            

            # Moves the text location in the x axis, based on the cursor relative position in the text field.
            if (self.xCursorPos > self.length * 0.75):
                self.textPosition -= self.font.size("B")[0]
            elif (self.xCursorPos < self.length * 0.25):
                self.textPosition += self.font.size("B")[0]
                self.textPosition = clamp(self.textPosition, -math.inf, 0)

            self.xCursorPos = self.font.size(self.text[:self.cursorPos])[0] + self.textPosition # Cursor coordinates based on cursorPos and the absolute text position

            self.redrawSurface() # Redraw the surface with text.

            # Draws the cursor based on where the position is.
            if (blink):
                pygame.draw.line(self.surface, self.textColor, [self.xCursorPos + self.margin[0], self.margin[1]], [self.xCursorPos + self.margin[0], self.margin[1] + self.font.get_height()], 2)


        self.surfaceToDraw.blit(self.surface, self.coords) # Draw to screen