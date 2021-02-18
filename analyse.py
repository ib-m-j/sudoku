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
            res = res + "{} cellis: {} Value = {}\n".format(x[0],x[1].key,x[2])
        elif x[0] =="Restriction":
            cells = [c.key for c in x[2]]
            cellsText = ""
            for k in cells:
                cellsText = cellsText + str(k) + ","
            res = res + \
            "Restriction subunit: {}, Cells: {} values: {}\n".format(
                x[1].id,cellsText,x[3])
    print( res)
    

#while developing
hardValues ={(0,2):"4",(0,5):"3",\
             (1,0):"6",(1,1):"3",(1,5):"7", \
             (2,0):"8",(2,5):"2",(2,7):"5", \
             (3,0):"4",(3,2):"9",\
             (4,2):"2",(4,3):"9",(4,5):"5",(4,6):"8",\
             (5,6):"6",(5,8):"3",\
             (6,1):"7",(6,3):"2",(6,8):"5",\
             (7,3):"7",(7,7):"3",(7,8):"1",\
             (8,3):"4",(8,6):"9"}


easyValues ={
    (0,1):"7",(0,3):"3",(0,5):"9",(0,7):"2",\
    (1,0):"5",(1,3):"6",(1,5):"1",(1,8):"7",\
    (2,2):"1",(2,6):"9",\
    (3,0):"9",(3,3):"1",(3,4):"6",(3,5):"3",(3,8):"2",\
    (4,2):"2",(4,6):"6",\
    (5,0):"3",(5,3):"2",(5,4):"8",(5,5):"5",(5,8):"1",\
    (6,2):"8",(6,6):"7",\
    (7,0):"6",(7,3):"9",(7,5):"7",(7,8):"8",\
    (8,1):"9",(8,3):"5",(8,5):"8",(8,7):"1" }

mediumValues ={
    (0,0):"3",(0,5):"1",(0,6):"9",(0,8):"5",\
    (1,3):"6",\
    (2,0):"8",(2,2):"9",(2,4):"3",(2,6):"1",\
    (3,0):"5",(3,3):"7",(3,5):"3",(3,7):"2",\
    (4,2):"4",(4,6):"3",\
    (5,1):"3",(5,3):"4",(5,5):"5",(5,8):"7",\
    (6,2):"7",(6,4):"5",(6,6):"4",(6,8):"2",\
    (7,5):"4",\
    (8,0):"6",(8,2):"2",(8,3):"9",(8,8):"8" }




        
def run():
    mainBoard = core.createStandardSudoku()
    


    fixedInit ={}
    for (k,v) in mediumValues.items():
        fixedInit[k[1],k[0]] = v
    #    for c in mainBoard.cells:
    #        if (c.key[1], c.key[0]) in initValues:
    #            c.setValue(initValues[(c.key[1], c.key[0])])
    #
    #for (cellKey, value) in fixedInit.items():
    #    mainBoard.insertValue(cellKey, value)
    #

    for c in mainBoard.cells:
        if c.key in fixedInit:
            c.setValue(fixedInit[c.key])

    print(mainBoard)
    print(mainBoard.displayBlockedRow(level = 0))
    #print(mainBoard.subUnits[0])
    #print(mainBoard.subUnits[0].getUnusedValues(symbols))

    foundValues = 0
    for c in mainBoard.cells:
        if c.value:
            foundValues += 1

    print(foundValues)

    while foundValues < 81:
        inserted = False
        print("Starting ronund")
        for level in range(1): 
            actionPoints = mainBoard.scanCellsForValue()
            actionPoints.extend(mainBoard.scanForConstraints(level))
            
        for a in actionPoints:
            print(a)
            #printActionPoints(actionPoints)
        for x in actionPoints:
            x.updateBoard()
                
            print("\nUpdated with {}".format(x.__str__()))
            print(mainBoard)
        a = input()
        if a == "a": 
            foundValues =81
    
if __name__ == '__main__':
    run()
    #cells = userinterface.getBoard(cellKeys)
    #allSubunits = []
    
