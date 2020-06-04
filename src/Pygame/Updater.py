objList = []

def updateAll():
    for obj in objList:
        obj.update()

def insertUpdate(obj):
    objList.append(obj)

def deleteUpdate(obj):
    objList.remove(obj)