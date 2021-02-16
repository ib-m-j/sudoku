import core
import userinterface
import sys
import itertools


def printS(x):
    toPrint = sorted(list(x))
    print(toPrint)

def printActionPoints(a):
    
    res = ""
    for x in a:
        if x[0] == "setValue":
            res = res + "{} cell: {} Value = {}\n".format(x[0],x[1].key,x[2])
        elif x[0] =="Restriction":
            cells = [c.key for c in x[2]]
            cellsText = ""
            for k in cells:
                cellsText = cellsText + str(k) + ","
            res = res + "Restriction subunit: {}, Cells: {} values: {}\n".format(
                x[1].id,cellsText,x[3])
    print( res)
    

class ActionItem:
    #insertBlocked
    #inferredBlockedValues 
    pass



        
def run():
    mainBoard = core.createStandardSudoku()
    

    #while developing
    initValues ={(0,2):"4",(0,5):"3",\
                 (1,0):"6",(1,1):"3",(1,5):"7", \
                 (2,0):"8",(2,5):"2",(2,7):"5", \
                 (3,0):"4",(3,2):"9",\
                 (4,2):"2",(4,3):"9",(4,5):"5",(4,6):"8",\
                 (5,6):"6",(5,8):"3",\
                 (6,1):"7",(6,3):"2",(6,8):"5",\
                 (7,3):"7",(7,7):"3",(7,8):"1",\
                 (8,3):"4",(8,6):"9"}

    fixedInit ={}
    for (k,v) in initValues.items():
        fixedInit[k[1],k[0]] = v
    #    for c in mainBoard.cells:
    #        if (c.key[1], c.key[0]) in initValues:
    #            c.setValue(initValues[(c.key[1], c.key[0])])
    #
    for (cellKey, value) in fixedInit.items():
        mainBoard.insertValue(cellKey, value)
    
    print(mainBoard)
    #print(mainBoard.displayBlockedRow())
    foundValues = 0
    for c in mainBoard.cells:
        if c.value:
            foundValues += 1

    print(foundValues)
    #print(mainBoard.subUnits[0])
    #print(mainBoard.subUnits[0].getUnusedValues(symbols))

    

    while foundValues < 81:
        actionPoints = mainBoard.scanCellsForValue()
        actionPoints.extend(mainBoard.scanForConstraints())
        printActionPoints(actionPoints)
        print(mainBoard)
        updateActions = []
        blockedValues = []
        
        foundValues =81
    
if __name__ == '__main__':
    run()
    #cells = userinterface.getBoard(cellKeys)
    #allSubunits = []
    
