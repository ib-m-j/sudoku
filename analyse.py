import userinterface
import sys


class SudukoSubunit():
    def __init__(self, name):
        self.id = name
        self.cells = []

    def __str__(self):
        res = self.id
        for c in self.cells:
            res = res + "{}:{} ".format(c.key, c.value)
        return res
    
class Row(SudukoSubunit):
    def __init__(self, no):
        SudukoSubunit.__init__(self,  "row{}".format(no))
        self.rowNo = no
        
    def addCell(self, cell):
        returnValue = False
        if cell.key[1] == self.rowNo:
            self.cells.append(cell)
            returnValue = True

        return returnValue
        
class Col(SudukoSubunit):
    def __init__(self, no):
        SudukoSubunit.__init__(self,  "col{}".format(no))
        self.colNo = no
    
    def addCell(self, cell):
        returnValue = False
        if cell.key[0] == self.colNo:
            self.cells.append(cell)
            returnValue = True

        return returnValue
        

class Region(SudukoSubunit):
    def __init__(self, no1, no2):
        SudukoSubunit.__init__(self,  "region{}{}".format(no1,no2))
        self.rowRegion = no2
        self.colRegion = no1

    def addCell(self, cell):
        returnValue = False
        if cell.key[1] // 3 == self.rowRegion and cell.key[0] // 3 == self.colRegion:
            self.cells.append(cell)
            returnValue = True
        return returnValue


class SudukoCell:
    def __init__(self, key, value = ''):
        self.key=key
        self.value=value
        self.belongsTo = []
        self.blockedValues = {}
        self.inferredBlocks = []

    def setValue(self, v):
        self.value = v
    

    def addBelongsTo(self, subUnit):
        self.belongsTo.append(subUnit)

        
def run():

    allCells = [SudukoCell((i,j)) for j in range(9) for i in range(9)]
    symbols = ['1','2','3','4','5','6','7','8','9']

    #while developing
    initValues ={(0,2):"4",(0,5):"3",\
                 (1,0):"6",(1,1):"3",(1,5):"7", \
                 (2,0):"8",(2,5):"2",(2,7):"5", \
                 (3,0):"4",(3,2):"9",\
                 (4,2):"2",(4,3):"9",(4,5):"5",(4,6):"8",\
                 (5,2):"6",(5,8):"3",\
                 (6,1):"7",(6,3):"2",(6,8):"5",\
                 (7,3):"7",(7,7):"2",(7,8):"5",\
                 (8,3):"4",(8,6):"9"}

    for c in allCells:
        if (c.key[1], c.key[0]) in initValues:
            c.setValue(initValues[(c.key[1], c.key[0])])



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


    foundValues = 0
    for c in allCells:
        if c.value:
            foundValues += 1

    print(foundValues)
    while foundValues < 81:
        updateActions = []
        blockedValues = []
        for c in allCells[30:32]:
            print("cell", c.key)
            for subUnit in c.belongsTo:
                print(subUnit.id)
                for c in subUnit.cells:
                    if c.value:
                        blockedValues.append(c.value)
            print(set(blockedValues))

        
        foundValues =81
    
if __name__ == '__main__':
    run()
    #cells = userinterface.getBoard(cellKeys)
    #allSubunits = []
    
