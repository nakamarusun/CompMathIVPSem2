def f(x: float):
    return 2 * x + 6

def compute(f, h: float, until: float, y0):

    xVal = [0]
    yVal = [y0]

    curX = 0
    curY = y0

    for i in range(int(until / h)):
        curX += h
        x = curX
        curY = curY + (h * eval(f))
        xVal.append(curX)
        yVal.append(curY)

    return [xVal, yVal]