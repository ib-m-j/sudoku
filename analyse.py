import userinterface
import sys

class ActionItem:
    #insertBlocked
    #inferredBlockedValues 
    pass

class SudokuBoard:
    def __init__(self, cells, subUnits, symbols):
        self.cells = cells
        self.subUnits = subUnits
        self.symbols = symbols
        self.updates = []
        self.cellDict = {}
        for c in cells:
            self.cellDict[c.key] = c
        self.actionItems = []

    #def actionItems = []
            
    def insertValue(self, cellKey, v):
        c = self.cellDict[cellKey]
        c.value = v
        c.blockedValues = set([])
        for sub in self.getSubunitsFromCells([c]):
            for c1 in sub.cells:
                if c1 !=  c and not(c1.value):
                   # print("inserted block", c1, c)
                    c1.blockedValues = c1.blockedValues.union( set([v]))

    def getSubunitsFromCells(self, cells):
    #finds subuinits that contain all c's in cells    
        res = []
        for sub in self.subUnits:
            #print(set(cells))
            #print(set(sub.cells))
            #exit(0)    
            if set(cells) <=  set(sub.cells):
                res = res + [sub]
        return res

    def scanForConstraints(self):
        for sub in self.subUnits:
            openCells = []
            for c in sub.cells:
                if c.value:
                    openCells.append(c)
    XXXXXXXXXXXXXXX



    def displayBlockedRow(self, row=2):
        for sub in self.subUnits:
            if isinstance(sub, Row) and sub.rowNo == row:
                res ="blocked by row {}\n".format(row)
                for c in sub.cells:
                    sortList = sorted(list(c.blockedValues))
                    for symb in sortList:
                        res = res + symb + ", "
                    res = res + "\n"
                res = res + "\n"    

        return res

    def __str__(self):
        res = "Board\n"
        for sub in self.subUnits:
            if isinstance(sub, Row):
                res = res + sub.id + ':   '
                for c in sub.cells:
                    if c.value:
                        add = " {} ".format(c.value)
                    else:
                        add = " _ "
                    res = res + add
                res = res + '\n'
        return res
    
                  



class SudokuSubunit():
    def __init__(self, name):
        self.id = name
        self.cells = []

    def getUnusedValues(self):
        res = set([])
        usedV = set([]).union([c.value for c in self.cells])
        return symbols - usedV    
        
    def __str__(self):
        res = self.id
        for c in self.cells:
            res = res + "{}:{} ".format(c.key, c.value)
        return res
    
class Row(SudokuSubunit):
    def __init__(self, no):
        SudokuSubunit.__init__(self,  "row{}".format(no))
        self.rowNo = no
        
    def addCell(self, cell):
        returnValue = False
        if cell.key[1] == self.rowNo:
            self.cells.append(cell)
            returnValue = True

        return returnValue
        
class Col(SudokuSubunit):
    def __init__(self, no):
        SudokuSubunit.__init__(self,  "col{}".format(no))
        self.colNo = no
    
    def addCell(self, cell):
        returnValue = False
        if cell.key[0] == self.colNo:
            self.cells.append(cell)
            returnValue = True

        return returnValue
        

class Region(SudokuSubunit):
    def __init__(self, no1, no2):
        SudokuSubunit.__init__(self,  "region{}{}".format(no1,no2))
        self.rowRegion = no2
        self.colRegion = no1

    def addCell(self, cell):
        returnValue = False
        if cell.key[1] // 3 == self.rowRegion and cell.key[0] // 3 == self.colRegion:
            self.cells.append(cell)
            returnValue = True
        return returnValue


class SudokuCell:
    def __init__(self, key, value = ''):
        self.key=key
        self.value=value
        self.belongsTo = []
        self.blockedValues = set([])
        self.inferredBlockedValues = []

    def setValue(self, v):
        self.value = v
    

    def addBelongsTo(self, subUnit):
        self.belongsTo.append(subUnit)

symbols = set(['1','2','3','4','5','6','7','8','9'])

        
def run():

    allCells = [SudokuCell((i,j)) for j in range(9) for i in range(9)]


    allSubunits =[]

    for i in range(9):
        newRow = Row(i)
        for cell in allCells:
            if newRow.addCell(cell):
                 cell.addBelongsTo(newRow)
        allSubunits.append(newRow)

    for i in range(9):
        newCol = Col(i)
        for cell in allCells:
            if  newCol.addCell(cell):
                cell.addBelongsTo(newCol)
        allSubunits.append(newCol)

    for i in range(3):
        for j in range(3):
            newRegion = Region(j, i)
            for cell in allCells:
                if  newRegion.addCell(cell):
                    cell.addBelongsTo(newRegion)
            allSubunits.append(newRegion)


    mainBoard = SudokuBoard(allCells, allSubunits, symbols)

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
    #    for c in allCells:
    #        if (c.key[1], c.key[0]) in initValues:
    #            c.setValue(initValues[(c.key[1], c.key[0])])
    #
    for (cellKey, value) in fixedInit.items():
        mainBoard.insertValue(cellKey, value)
    
    #print(mainBoard)
    #print(mainBoard.displayBlockedRow())
    foundValues = 0
    for c in allCells:
        if c.value:
            foundValues += 1

    print(foundValues)
    print(mainBoard.subUnits[0])
    print(mainBoard.subUnits[0].getUnusedValues())

    

    while foundValues < 81:
        mainBoard.scanForConstraints()
        updateActions = []
        blockedValues = []
        
        foundValues =81
    
if __name__ == '__main__':
    run()
    #cells = userinterface.getBoard(cellKeys)
    #allSubunits = []
    
