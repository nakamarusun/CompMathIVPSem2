import Pygame.GlobalVariables as GVar
import math

class IVP:

    @staticmethod
    def f(x: float):
        # Function for testing
        return 2 * x + 6

    @staticmethod
    def compute(f: str, h: float, until: float, y0, functionMode=0):

        # Sets initial values
        xVal = [0]
        yVal = [y0]

        # Sets the current value it is working with
        curX = 0
        curY = y0

        functionEval = eval("lambda x, y : " + f) # Converts the specified string to a python mathematical formula. It is of utmost importance for the string to be python-compliant, so that it doesn't run into any errors.

        chosenFunction = IVP.euler # Default is euler

        if (functionMode == 0):
            chosenFunction = IVP.euler
        elif (functionMode == 1):
            chosenFunction = IVP.rk4

        for i in range(int(until / h)):
            # Calculates the next y value based on the chosen algorithm
            curY = chosenFunction(curX, curY, h, functionEval)
            curX += h # Adds the current x by the specified h
            # Appends to array
            xVal.append(curX)
            yVal.append(curY)

        return [xVal, yVal]
        
    @staticmethod
    def euler(x, y, h, f):
        return y + (h * f(x, y))

    @staticmethod
    def rk4(x, y, h, f):
        k1 = f(x, y)
        k2 = f(x + 1/2*h, y + 1/2*h*k1)
        k3 = f(x + 1/2*h, y + 1/2*h*k2)
        k4 = f(x + h, y + k3*h)

        return y + (1/6 * (k1 + 2*k2 + 2*k3 + k4)) * h

def clamp(val, min, max):
    # Clamps a value to not exceed the min or max value.
    if (val < min):
        return min
    elif (val > max):
        return max
    return val

def getWidthResolutionRatio(ratio):
    return GVar.resolution[0] * ratio

def getLengthResolutionRatio(ratio):
    return GVar.resolution[1] * ratio

def lerp(val, min, max):
    # Linear Interpolation, gets a value from a specified ratio from min to max
    return (min + val * (max - min))

def invLerp(val, min, max):
    # Inverse Linear Interpolation, to get a ratio of the value from the min to the max
    try:
        return ((val - min) / (max - min))
    except:
        GVar.divisionByZero = True
        return 0

# import numpy as np

# def eulerOp(f, x, y0):
#     n = x.size
#     y = np.zeros((n))
#     y[0] = y0
#     dx = x[1] - x[0]
#     for i in range(n - 1):
#         print(f(x[i], y[i]))
#         y[i+1] = y[i] + dx * f(x[i], y[i])
#     return y

# f = lambda x, y: -2*x**3+12*x**2-20*x+8.5
# y0 = 1
# x = np.linspace(0, 1, 11)
# print(eulerOp(f, x, y0))
# print(IVP.compute("-2*x**3+12*x**2-20*x+8.5", 0.1, 1.0, 1, 0))