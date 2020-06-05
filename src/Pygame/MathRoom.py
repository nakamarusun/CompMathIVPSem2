import Pygame.GlobalVariables as GVar
import Pygame.Updater as Updater
import pygame
import pygame.draw
from Pygame.Button import Button
from Pygame.Slider import Slider
from Pygame.TextField import TextField
from Pygame.TextLabel import TextLabel
from Pygame.ToggleButton import ToggleButton
import MathUtil


class CanvasSurface():

    ratio = []
    functionCanvasSurface = None

    function = lambda self, x : 2*x - 4
    y0 = 2
    until = 5
    h = 0.1

    xArr = [] # The x plot in the graph.
    yArr = [] # The y plot in the graph.

    yMax = 0 
    yMin = 0

    def __init__(self):
        self.ratio = (0.85, 0.7) # The ratio of the size of the functionCanvasSurface compared to the main screen
        self.updateFunction()
        self.redrawSurface()

    def updateFunction(self):
        self.xArr, self.yArr = MathUtil.IVP.compute(self.function, self.h, self.until, self.y0)
        self.yMax = max(self.yArr) + 1
        self.yMin = min(self.yArr) - 1
        # print(self.xArr, "\n", self.yArr)
        print(self.yMin, "\n", self.yMax)

    def redrawSurface(self):
        # Creates a new function canvas surface with 85% width size and 50% height size
        self.functionCanvasSurface = pygame.Surface((GVar.resolution[0] * self.ratio[0], GVar.resolution[1] * self.ratio[1]))
        self.functionCanvasSurface.fill((255, 255, 255)) # Clears the surface with white
        pygame.draw.rect(self.functionCanvasSurface, (0, 0, 0), self.functionCanvasSurface.get_rect(), 1) # Puts a white border in the canvas
        # Do all drawing here

        pointBefore = [ 0, self.ratio[1] * GVar.resolution[1] * (1 - MathUtil.invLerp(self.yArr[0], self.yMin, self.yMax)) ] # Sets the first dot of the graphic
        for i in range(len(self.xArr) - 1):
            pointAfter = [ MathUtil.invLerp(self.xArr[i + 1], self.xArr[0], self.xArr[-1]) * GVar.resolution[0] * self.ratio[0], ( 1 - MathUtil.invLerp(self.yArr[i + 1], self.yMin, self.yMax)) * GVar.resolution[1] * self.ratio[1] ] # Counts the current dot.
            pygame.draw.line(self.functionCanvasSurface, (0, 0, 0), pointBefore, pointAfter, 2) # Draws line from the previous dot to the dot after it
            pygame.draw.circle(self.functionCanvasSurface, (230, 120, 0), (round(pointBefore[0]), round(pointBefore[1])), 4) # Draws the dot in each of the delta x's
            pointBefore = pointAfter # Sets the previous dot to the current dot.

    def drawNumbers(self):
        yNumbers = (self.yMax - self.yMin) / 10
        counter = self.yMin
        for i in range(10):
            GVar.mainScreenBuffer.blit(GVar.defFont.render(str(round(counter, 3)) + " -", True, (0, 0, 0)),
            [((1 - self.ratio[0])/2 * GVar.resolution[0]) - 40, (((0.1 + self.ratio[1]) * GVar.resolution[1]) - (MathUtil.invLerp(counter, self.yMin, self.yMax) * (GVar.resolution[1] * self.ratio[1])) - 7)])
            counter += yNumbers

        xNumbers = (self.xArr[-1] - self.xArr[0]) / 10
        counter = self.xArr[0]
        for i in range(11):
            GVar.mainScreenBuffer.blit(GVar.defFont.render("|" + str(round(counter, 3)), True, (0, 0, 0)),
            [((1 - self.ratio[0])/2 * GVar.resolution[0]) + (MathUtil.invLerp(counter, self.xArr[0], self.xArr[-1]) * GVar.resolution[0] * self.ratio[0]) - 3, ((0.1 + self.ratio[1]) * GVar.resolution[1])])
            counter += xNumbers

    def update(self):
        if (GVar.isVideoResized):
            self.redrawSurface() # If program is resized, change the size of the canvas surface

        # Drawing end
        GVar.mainScreenBuffer.blit(self.functionCanvasSurface, [(GVar.resolution[0] / 2) - (GVar.resolution[0] * self.ratio[0] / 2), GVar.resolution[1] * 0.1]) # Draws into the main screen buffer in the middle.
        self.drawNumbers()

class MainSurface():

    interactableList = []

    deltaXSlider = None
    untilXSlider = None

    deltaXTextField = None
    untilXTextField = None

    functionTextField = None

    initialYTextField = None

    calculateButton = None

    eulerToggle = None
    rungeKuttaToggle = None

    def __init__(self):
        self.redrawAll()

        # Samples
        # self.interactableList.append(Button(lambda : print("Button Clicked"), GVar.mainScreenBuffer, [100, 100], "yes", GVar.defFont, [150, 100], (255, 0, 0), True))
        # self.interactableList.append(Slider(GVar.mainScreenBuffer, [300, 200], 300))
        # self.interactableList.append(TextField(lambda : print("Enter Clicked"), GVar.mainScreenBuffer, 300, [400, 300], GVar.defFont))
        
    def redrawAll(self):
        self.interactableList = []

        # Sliders
        self.deltaXSlider = Slider(GVar.mainScreenBuffer, [GVar.resolution[0] * 0.075, GVar.resolution[1] * 0.84], GVar.resolution[0] * 0.3, 0.5, (191, 233, 245), (141, 202, 235))
        self.interactableList.append(self.deltaXSlider) # Delta X Slider
        self.untilXSlider = Slider(GVar.mainScreenBuffer, [GVar.resolution[0] * 0.075, GVar.resolution[1] * 0.91], GVar.resolution[0] * 0.3, 0.2, (252, 215, 251), (220, 141, 235), (142, 47, 189), (185, 51, 222))
        self.interactableList.append(self.untilXSlider) # Until X Slider

        # Slider Text
        self.interactableList.append(TextLabel(GVar.mainScreenBuffer, "Delta X:", [GVar.resolution[0] * 0.075, GVar.resolution[1] * 0.82])) # Delta X Text
        self.interactableList.append(TextLabel(GVar.mainScreenBuffer, "Until X:", [GVar.resolution[0] * 0.075, GVar.resolution[1] * 0.89])) # Until X Text

        # Slider TextField
        self.deltaXTextField = TextField(self.renewXSlider,
         GVar.mainScreenBuffer, 65, [GVar.resolution[0] * 0.4, GVar.resolution[1] * 0.84 - 3], GVar.defFont)
        self.interactableList.append(self.deltaXTextField) # Delta X TextField
        self.untilXTextField = TextField(self.renewUntilX,
         GVar.mainScreenBuffer, 65, [GVar.resolution[0] * 0.4, GVar.resolution[1] * 0.91 - 3], GVar.defFont)
        self.interactableList.append(self.untilXTextField) # Until X TextField

        # Function Text
        self.interactableList.append(TextLabel(GVar.mainScreenBuffer, "Function:", [GVar.resolution[0] * 0.51, GVar.resolution[1] * 0.84 - 2], GVar.defFont18Bold))

        # Function TextField
        self.functionTextField = TextField(lambda : print("Pressed"),
         GVar.mainScreenBuffer, GVar.resolution[0] * 0.285, [GVar.resolution[0] * 0.64, GVar.resolution[1] * 0.84 - 9], GVar.defFont18)
        self.interactableList.append(self.functionTextField)

        # Initial y Text
        self.interactableList.append(TextLabel(GVar.mainScreenBuffer, "y(0):", [GVar.resolution[0] * 0.51, GVar.resolution[1] * 0.91 - 2], GVar.defFont18))

        # Initial y TextField
        self.initialYTextField = TextField(lambda : print("Pressed"),
         GVar.mainScreenBuffer, GVar.resolution[0] * 0.075, [GVar.resolution[0] * 0.56, GVar.resolution[1] * 0.91 - 9], GVar.defFont18)
        self.interactableList.append(self.initialYTextField)

        # Calculate Button
        self.calculateButton = Button(lambda : print("Calculated"),
         GVar.mainScreenBuffer, [GVar.resolution[0] * 0.83, GVar.resolution[1] * 0.91 - 9], "CALCULATE", GVar.defFont, [GVar.resolution[0] * 0.095, 29], (219, 42, 110), True, (227, 64, 145))
        self.interactableList.append(self.calculateButton)

        # Toggle buttons for calculation Methods
        self.eulerToggle = ToggleButton(lambda : print("Calculated"),
         GVar.mainScreenBuffer, [GVar.resolution[0] * 0.65, GVar.resolution[1] * 0.91 - 9], "Euler", GVar.defFont, [GVar.resolution[0] * 0.085, 29/2], (144, 62, 237), True, (116, 57, 227), (219, 22, 104))
        self.interactableList.append(self.eulerToggle)
        self.rungeKuttaToggle = ToggleButton(lambda : print("Calculated"),
         GVar.mainScreenBuffer, [GVar.resolution[0] * 0.65 + GVar.resolution[0] * 0.085, GVar.resolution[1] * 0.91 - 9], "RungeKutta", GVar.defFont, [GVar.resolution[0] * 0.085, 29/2], (144, 62, 237), True, (116, 57, 227), (219, 22, 104))
        self.interactableList.append(self.rungeKuttaToggle)

    def update(self):
        # Do all checks here

        if (self.deltaXSlider.dragged):
            self.deltaXTextField.text = str(round(self.deltaXSlider.value, 3))
        # End actions

        if (GVar.isVideoResized):
            self.redrawAll()
        # Draws buttons and detects any button press
        for interactable in self.interactableList:
            interactable.update()

    def renewXSlider(self):
        try:
            self.deltaXSlider.value = MathUtil.clamp(float(self.deltaXTextField.text), 0.0, 1.0)
        except:
            self.deltaXSlider.value = 0.5
            self.deltaXTextField.text = 0.5
        self.deltaXSlider.updateSliderPos()
        self.deltaXSlider.redrawSurface()

    def renewUntilX(self):
        try:
            self.untilXSlider.value = MathUtil.clamp(float(self.untilXTextField.text), 0.0, 1.0)
        except:
            self.untilXSlider.value = 0.5
            self.untilXTextField.text = 0.5
        self.untilXSlider.updateSliderPos()
        self.untilXSlider.redrawSurface()

def initRoom():
    Updater.insertUpdate(CanvasSurface())
    Updater.insertUpdate(MainSurface())