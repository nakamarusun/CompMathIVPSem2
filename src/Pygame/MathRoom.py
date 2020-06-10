import Pygame.GlobalVariables as GVar
import Pygame.Updater as Updater
import pygame
import pygame.draw
from Pygame.Button import Button
from Pygame.Slider import Slider
from Pygame.TextField import TextField
from Pygame.TextLabel import TextLabel
from Pygame.ToggleButton import ToggleButton
from Pygame.ToggleList import ToggleList
import MathUtil
import math
import string
from time import time

class CanvasSurface():

    ratio = []
    functionCanvasSurface = None

    # DEFAULT VALUES
    function = "x**2 - 4*y"
    y0 = 1
    until = 5
    h = 0.1

    # Both is in miliseconds
    calculationTime = 0 # Time to calculate the actual values
    drawingTime = 0 # Time to draw the graph

    # 0 = Euler
    # 1 = 4th Order Runge Kutta
    functionMode = 0

    finalValue = "[0, 0]"

    xArr = [] # The x plot in the graph.
    yArr = [] # The y plot in the graph.

    yMax = 0 
    yMin = 0

    def __init__(self):
        self.ratio = (0.85, 0.7) # The ratio of the size of the functionCanvasSurface compared to the main screen
        self.updateFunction()
        self.redrawSurface()

    def updateFunction(self):
        start = time()
        self.xArr, self.yArr = MathUtil.IVP.compute(self.function, self.h, self.until, self.y0, self.functionMode)
        self.yMax = max(self.yArr)
        self.yMin = min(self.yArr)
        range = self.yMax - self.yMin
        self.yMax += range * 0.05
        self.yMin -= range * 0.05
        self.calculationTime = time() - start
        # print(self.xArr, "\n\n", self.yArr)
        # print(self.yMin, "\n", self.yMax)
        self.finalValue = "[" + str(round(self.xArr[-1], 6)) + " " + str(round(self.yArr[-1], 6)) + "]"

    def redrawSurface(self):
        try:
            self.updateFunction()
        except OverflowError:
            mainSurface.functionError = "Resulting number too large !"
            self.finalValue = "[~, ~]"
        # Creates a new function canvas surface with 85% width size and 50% height size
        self.functionCanvasSurface = pygame.Surface((GVar.resolution[0] * self.ratio[0], GVar.resolution[1] * self.ratio[1]))
        self.functionCanvasSurface.fill((255, 255, 255)) # Clears the surface with white
        pygame.draw.rect(self.functionCanvasSurface, (0, 0, 0), self.functionCanvasSurface.get_rect(), 1) # Puts a white border in the canvas
        # Do all drawing here
        start = time()
        # Draws the actual value

        # Draws the actual IVP Function
        pointBefore = [ 0, self.ratio[1] * GVar.resolution[1] * (1 - MathUtil.invLerp(self.yArr[0], self.yMin, self.yMax)) ] # Sets the first dot of the graphic
        for i in range(len(self.xArr) - 1):
            pointAfter = [ MathUtil.invLerp(self.xArr[i + 1], self.xArr[0], self.xArr[-1]) * GVar.resolution[0] * self.ratio[0], ( 1 - MathUtil.invLerp(self.yArr[i + 1], self.yMin, self.yMax)) * GVar.resolution[1] * self.ratio[1] ] # Counts the current dot.
            pygame.draw.aaline(self.functionCanvasSurface, (0, 0, 0), pointBefore, pointAfter, 2) # Draws line from the previous dot to the dot after it

            # pygame.draw.circle(self.functionCanvasSurface, (230, 120, 0), (round(pointBefore[0]), round(pointBefore[1])), 4) # Draws the dot in each of the delta x's, non antialiased circle

            pygame.gfxdraw.aacircle(self.functionCanvasSurface, round(pointBefore[0]), round(pointBefore[1]), 4, (230, 120, 0)) # Draws circle anti-aliased outline.
            pygame.gfxdraw.filled_circle(self.functionCanvasSurface, round(pointBefore[0]), round(pointBefore[1]), 4, (230, 120, 0)) # Draws circle

            pointBefore = pointAfter # Sets the previous dot to the current dot.

        pygame.draw.circle(self.functionCanvasSurface, (230, 120, 0), (round(pointBefore[0]), round(pointBefore[1])), 4) # Draws the last dot
        self.drawingTime = time() - start

    def drawNumbers(self):
        # Draws the number in the y axis, 20 numbers
        yNumbers = (self.yMax - self.yMin) / 20
        counter = self.yMin
        for i in range(20):
            GVar.mainScreenBuffer.blit(GVar.defFont.render(str(round(counter, 3)) + " -", True, (0, 0, 0)),
            [((1 - self.ratio[0])/2 * GVar.resolution[0]) - 40, (((0.1 + self.ratio[1]) * GVar.resolution[1]) - (MathUtil.invLerp(counter, self.yMin, self.yMax) * (GVar.resolution[1] * self.ratio[1])) - 7)])
            counter += yNumbers

        # Draws the number in the x axis, 10 numbers
        xNumbers = (self.xArr[-1] - self.xArr[0]) / 10
        counter = self.xArr[0]
        for i in range(10 + 1):
            GVar.mainScreenBuffer.blit(GVar.defFont.render("|" + str(round(counter, 3)), True, (0, 0, 0)),
            [((1 - self.ratio[0])/2 * GVar.resolution[0]) + (MathUtil.invLerp(counter, self.xArr[0], self.xArr[-1]) * GVar.resolution[0] * self.ratio[0]) - 3, ((0.1 + self.ratio[1]) * GVar.resolution[1])])
            counter += xNumbers

    def update(self):
        if (GVar.isVideoResized):
            self.redrawSurface() # If program is resized, change the size of the canvas surface

        # Drawing end
        GVar.mainScreenBuffer.blit(self.functionCanvasSurface, [(GVar.resolution[0] / 2) - (GVar.resolution[0] * self.ratio[0] / 2), GVar.resolution[1] * 0.1]) # Draws into the main screen buffer in the middle.
        GVar.mainScreenBuffer.blit(GVar.defFont.render("calc: " + str(self.calculationTime) + " ms", True, (0, 150, 0)), [GVar.resolution[0] * 0.06, GVar.resolution[1] * 0.05]) # Prints calculation time
        GVar.mainScreenBuffer.blit(GVar.defFont.render("draw: " + str(self.drawingTime) + " ms", True, (0, 150, 0)), [GVar.resolution[0] * 0.06, GVar.resolution[1] * 0.075]) # Prints draw time
        GVar.mainScreenBuffer.blit(GVar.defFontBold.render("Final value: " + self.finalValue, True, (0, 0, 0)), [GVar.resolution[0] * 0.75, GVar.resolution[1] * 0.075]) # Prints the final value
        self.drawNumbers()

    def setFunctionMode(self, mode):
        self.functionMode = mode

class MainSurface():

    interactableList = []

    # Interactable object list
    deltaXSlider = None
    untilXSlider = None

    deltaXTextField = None
    untilXTextField = None

    functionTextField = None

    initialYTextField = None

    calculateButton = None

    eulerToggle = None
    rungeKuttaToggle = None

    algorithmToggleList = None

    functionError = None # If the inputted function by the user cannot be parsed / produces an error, print this message.

    def __init__(self):
        self.redrawAll()

        # Samples
        # self.interactableList.append(Button(lambda : print("Button Clicked"), GVar.mainScreenBuffer, [100, 100], "yes", GVar.defFont, [150, 100], (255, 0, 0), True))
        # self.interactableList.append(Slider(GVar.mainScreenBuffer, [300, 200], 300))
        # self.interactableList.append(TextField(lambda : print("Enter Clicked"), GVar.mainScreenBuffer, 300, [400, 300], GVar.defFont))
        
    def redrawAll(self):
        self.interactableList = []

        # Sliders
        self.deltaXSlider = Slider(GVar.mainScreenBuffer, [GVar.resolution[0] * 0.075, GVar.resolution[1] * 0.84], GVar.resolution[0] * 0.3, canvasSurface.h/2, (191, 233, 245), (141, 202, 235))
        self.interactableList.append(self.deltaXSlider) # Delta X Slider
        self.untilXSlider = Slider(GVar.mainScreenBuffer, [GVar.resolution[0] * 0.075, GVar.resolution[1] * 0.91], GVar.resolution[0] * 0.3, canvasSurface.until/20, (252, 215, 251), (220, 141, 235), (142, 47, 189), (185, 51, 222))
        self.interactableList.append(self.untilXSlider) # Until X Slider

        # Slider Text
        self.interactableList.append(TextLabel(GVar.mainScreenBuffer, "Delta X:", [GVar.resolution[0] * 0.075, GVar.resolution[1] * 0.82])) # Delta X Text
        self.interactableList.append(TextLabel(GVar.mainScreenBuffer, "Until X:", [GVar.resolution[0] * 0.075, GVar.resolution[1] * 0.89])) # Until X Text

        # Slider TextField
        self.deltaXTextField = TextField(self.renewXSlider,
         GVar.mainScreenBuffer, 65, [GVar.resolution[0] * 0.4, GVar.resolution[1] * 0.84 - 3], GVar.defFont, initText=str(canvasSurface.h))
        self.interactableList.append(self.deltaXTextField) # Delta X TextField
        self.untilXTextField = TextField(self.renewUntilX,
         GVar.mainScreenBuffer, 65, [GVar.resolution[0] * 0.4, GVar.resolution[1] * 0.91 - 3], GVar.defFont, initText=str(canvasSurface.until))
        self.interactableList.append(self.untilXTextField) # Until X TextField

        # Function Text
        self.interactableList.append(TextLabel(GVar.mainScreenBuffer, "Function(y'):", [GVar.resolution[0] * 0.51, GVar.resolution[1] * 0.84 - 2], GVar.defFont18Bold))

        # Function TextField
        self.functionTextField = TextField(self.calculate,
         GVar.mainScreenBuffer, GVar.resolution[0] * 0.285, [GVar.resolution[0] * 0.64, GVar.resolution[1] * 0.84 - 9], GVar.defFont18, initText=canvasSurface.function)
        self.interactableList.append(self.functionTextField)

        # Initial y Text
        self.interactableList.append(TextLabel(GVar.mainScreenBuffer, "y(0):", [GVar.resolution[0] * 0.51, GVar.resolution[1] * 0.91 - 2], GVar.defFont18))

        # Initial y TextField
        self.initialYTextField = TextField(self.renewY0,
         GVar.mainScreenBuffer, GVar.resolution[0] * 0.075, [GVar.resolution[0] * 0.56, GVar.resolution[1] * 0.91 - 9], GVar.defFont18, initText=str(canvasSurface.y0))
        self.interactableList.append(self.initialYTextField)

        # Calculate Button
        self.calculateButton = Button(self.calculate,
         GVar.mainScreenBuffer, [GVar.resolution[0] * 0.83, GVar.resolution[1] * 0.91 - 9], "CALCULATE", GVar.defFont, [GVar.resolution[0] * 0.095, 29], (219, 42, 110), True, (227, 64, 145))
        self.interactableList.append(self.calculateButton)

        # Toggle buttons for calculation Methods
        self.eulerToggle = ToggleButton(lambda : canvasSurface.setFunctionMode(0),
         GVar.mainScreenBuffer, [GVar.resolution[0] * 0.65, GVar.resolution[1] * 0.91 - 9], "Euler", GVar.defFont, [GVar.resolution[0] * 0.085, 29/2], (144, 62, 237), True, (116, 57, 227), (219, 22, 104))
        self.interactableList.append(self.eulerToggle)
        self.rungeKuttaToggle = ToggleButton(lambda : canvasSurface.setFunctionMode(1),
         GVar.mainScreenBuffer, [GVar.resolution[0] * 0.65 + GVar.resolution[0] * 0.085, GVar.resolution[1] * 0.91 - 9], "4th RK", GVar.defFont, [GVar.resolution[0] * 0.085, 29/2], (144, 62, 237), True, (116, 57, 227), (219, 22, 104))
        self.interactableList.append(self.rungeKuttaToggle)

        # Toggle button controller
        self.algorithmToggleList = ToggleList([self.eulerToggle, self.rungeKuttaToggle], self.eulerToggle, self.changeFunctionMode)
        self.interactableList.append(self.algorithmToggleList)

    def update(self):
        # Do all checks here

        # If the delta x slider is dragged
        if (self.deltaXSlider.dragged):
            self.deltaXTextField.text = str(round(MathUtil.clamp(self.deltaXSlider.value * 2, 0.01, math.inf), 3))
            canvasSurface.redrawSurface()

        # If the until slider is dragged
        if (self.untilXSlider.dragged):
            self.untilXTextField.text = str(round(self.untilXSlider.value * 20, 3))
            canvasSurface.redrawSurface()
        
        try:
            canvasSurface.h = float(self.deltaXTextField.text)
        except:
            pass
        try:
            canvasSurface.until = float(self.untilXTextField.text)
        except:
            pass

        # End actions

        if (GVar.isVideoResized):
            self.redrawAll()

        # Draws buttons and detects any button press
        for interactable in self.interactableList:
            interactable.update()

        # Checks if there is any division by zero
        if (GVar.divisionByZero):
            GVar.mainScreenBuffer.blit(GVar.defFont24Bold.render("ERROR, DIVISION BY ZERO. CHANGE VALUE", True, (255, 0, 0)), [20, 20])

        # Checks if there is any function error
        if (self.functionError != None):
            GVar.mainScreenBuffer.blit(GVar.defFont24Bold.render(self.functionError, True, (255, 0, 0)), [20, 50])


    def renewXSlider(self):
        try:
            if (float(self.deltaXTextField.text) < 0.01):
                self.deltaXTextField.text = "0.01"
            self.deltaXSlider.value = MathUtil.clamp(float(self.deltaXTextField.text) / 2, 0.0, 1.0)
        except:
            self.deltaXSlider.value = 0.1
            self.deltaXTextField.text = "0.1"
        self.deltaXSlider.updateSliderPos()
        self.deltaXSlider.redrawSurface()
        canvasSurface.redrawSurface()

    def renewUntilX(self):
        try:
            self.untilXSlider.value = MathUtil.clamp(float(self.untilXTextField.text) / 20, 0.0, 1.0)
        except:
            self.untilXSlider.value = 5
            self.untilXTextField.text = "5"
        self.untilXSlider.updateSliderPos()
        self.untilXSlider.redrawSurface()
        canvasSurface.redrawSurface()

    def renewY0(self):
        try:
            canvasSurface.y0 = float(self.initialYTextField.text)
        except:
            self.initialYTextField.text = "5"
            canvasSurface.y0 = 5
        canvasSurface.redrawSurface()

    def calculate(self):
        fun = self.functionTextField.text # Checks the function inputted by the user

        allowedCharacters = "1234567890+-/*x^ ()ey." # Sets a library of allowed characters
        # Checks if there is a character outside the allowed ones.
        errorParse = False
        for char in fun:
            if (char not in allowedCharacters):
                self.functionError = "Illegal character in function text field"
                errorParse = True
                break

        if (errorParse): return

        # Parses the text to real equation
        # Strips any whitespace
        newFun = ""
        for char in fun:
            if (char != " "):
                newFun += char

        i = 0
        while i < len(newFun):
            try:
                if ((newFun[i] in (string.digits + "e)") and (newFun[i+1] == "x" or newFun[i+1] == "y" or newFun[i+1] == "e")) or ((newFun[i] == "x" or newFun[i] == "y") and newFun[i+1] == "(")): # Adds asterisk to numbers, e and ")" with no asterisk, and x or y with "("
                    newFun = newFun[:i + 1] + "*" + newFun[i + 1:]
                elif (newFun[i] == "^"):
                    newFun = newFun[:i] + "**" + newFun[i + 1:] # Changes ^ to double asterisk
                if (newFun[i] == "e"):
                    newFun = newFun[:i] + "math.e" + newFun[i + 1:] # Changes e to actual variable
            except:
                pass
            i += 1

        # Tries to calculate with the new function. If fail, throw error
        try:
            x = 2 # Bogus values to check whether function works correctly
            y = 3
            eval(newFun)
        except:
            self.functionError = "Function Error"
            return

        # At this point, the function is done parsing. Sets all of the function.
        canvasSurface.function = newFun # Sets the function as the new function
        self.functionError = None # Sets that no error has happened

        canvasSurface.redrawSurface()
        print(canvasSurface.xArr)
        print(canvasSurface.yArr)

    def changeFunctionMode(self):
        canvasSurface.redrawSurface()
        canvasSurface.update()

canvasSurface = CanvasSurface()
mainSurface = MainSurface()

def initRoom():
    Updater.insertUpdate(canvasSurface)
    Updater.insertUpdate(mainSurface)