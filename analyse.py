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
    

def describeActionPoints(actionPoints):
    desc = {}
    for a in actionPoints:
        if a.size() in desc:
            desc[a.size()] = desc[a.size()] + 1
        else:
            desc[a.size()] = 1

    keys = list(desc.keys())
    keys.sort()
    print("ActionPoints Overview")
    for (k,v) in desc.items():
        print("Size = {}, number of items {}".format(k,v))




    
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
    #basic algorithm: for each subunit take set UNUSED af all unused symbols.
    #for each subset of UNUSED (candidateSet)
    #check if the values therein are restricted
    #to som subset of the free cells in subunit (restrictionSet).
    #For each of these cases register a corresponding action.
    #
    #Use following definitions:
    #restrictionComplementSet is the set of cells unassignedin the subunit that
    #are not in restrictionSet
    #
    #candidateComplementSet is the set of unused symbols in the subunit
    #that are not in the candidateSet
    #
    #
    #If restrictionSet contains 1 element (UpdateValue1) or
    #restrictionComplementSet contains
    #one element (UpdateValue2) the value of the corresponding cell can be set.
    #Action UpdateValue1 or 2 as described.
    #UpdateValue1 
    #updateValue2 also requires an
    #Blocking2 (see below). This is not done as the corresponding
    #gets handled automatically ata later registration.
    #
    #
    #If the restrictionSet is same size as size candidateSet we 
    #found a split. This means that the
    #values of the restrictionSet is equal to  the candidateSet values and
    #the values of the restrictionComplementSet is equal
    #to the candidateComplementSet
    #This is handled by action updateSplit.
    #
    #updateSlit consists of registration of a number of blockings:
    #(Blocking1): restrictionSet is blocked for values in
    #candidateComplementSet.
    #(Blocking2) If another subunit contains restrictionSet,
    #update the relative complement
    #with blockings from candidateSet
    #Special case: if restrictionSet is same size as candidateSet
    #but restricktionComplementSet is empty, there is no Blocking1 but
    #Blocking2 is still relevant
    #
    #
    #Finally if restrictionSet is larger than candidateSet there is still
    #the possibility of a Blocking2 action.
    #
    #After rigistering all actions, sort action list
    #first UpdateValue1 then UpdateValue2. Then follow actions
    #sorted by size of restrictionSet
    #
    #Go through actionList, perform all uptaeValue1 or updateValue2 actions.
    #If some action was done here. start all over by registering new actionList.
    #If no update1 or update 2 actions are done do one new action and
    #start over with new actionList.
    #end when all cells filles out or actionList stable.
    #
    
    mainBoard = core.createStandardSudoku()
    


    fixedInit ={}
    for (k,v) in easyValues.items():
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
    remainingValues = mainBoard.findRemaining()

    difficulty = []
    while remainingValues > 0:
        inserted = False
        print("Starting round")
        #below does a scanning with candidateSet containing 1 element
        #and restrictionSet sixe of unused symbols minus 1.
        #doing separately avoids registering everything three
        #times and the corresponding SetBlocked2 gets done
        #automatically in later phase.
        actionPoints = mainBoard.scanCellsForValue()
        actionPoints.extend(mainBoard.scanForConstraints(0))

        #print(mainBoard)
        #print("Remaining values: ", remainingValues)

        #actionPoints.sort()
        #for a in actionPoints:
        #        print(a.__str__())

        #describeActionPoints(actionPoints)
        difficulty.append(sum(map(lambda x: x.size() < 12, actionPoints)))
        #a=input()
        
                
        updated = 0
        for x in actionPoints:
            if x.size() < 12:
                updated = updated + x.updateBoard()
                #print("\nUpdated with {}".format(x.__str__()))
                #print(mainBoard)

        remainingValues = mainBoard.findRemaining()

        if updated == 0 and remainiingValues > 0:
            print("Did not finish properly")
            break

    print("finished with")
    print(mainBoard)

    print(difficulty)
        
                
if __name__ == '__main__':
    run()
    #cells = userinterface.getBoard(cellKeys)
    #allSubunits = []
    
