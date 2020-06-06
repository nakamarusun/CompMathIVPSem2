
class ToggleList:
    # This class controls a collection of toggle buttons. Letting only one to be activated.

    toggleList = []

    activeButton = None # Returns the currently active button.

    funcWhenChanged = None # Runs the function when a new button is toggled

    def __init__(self, toggleList, activeButton, funcWhenChanged):
        self.toggleList = toggleList
        self.activeButton = activeButton
        self.funcWhenChanged = funcWhenChanged
        for i in toggleList: # Deactivates every button
            i.pressed = False
        self.activeButton.pressed = True # Activates the specified button

    def update(self):
        # Detects any changes when any other toggle buttons is pressed other than the current active button.
        for toggle in self.toggleList:
            # if (toggle == self.activeButton):
            #     continue
            # if (toggle.pressed == True):
            #     self.activeButton.toggle()
            #     self.activeButton = toggle
            #     self.activeButton.toggle()
            #     self.funcWhenChanged()
            #     break
            if (toggle.pressed == False and toggle == self.activeButton):
                toggle.pressed = True
                toggle.redrawButton()
                continue
            if (toggle == self.activeButton):
                continue
            elif (toggle.pressed == True):
                self.activeButton.pressed = False
                self.activeButton.color = self.activeButton.initColor
                self.activeButton.redrawButton()
                self.activeButton = toggle
                self.funcWhenChanged()
                break