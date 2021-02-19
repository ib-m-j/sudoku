import sys
import itertools

def displayCellList(list):
    res = "Cell list: "
    for c in list:
        res = res + str(c) + ", "
    return res    

def displaySubunitList(list):
    res = "subunit list:\n"
    for c in list:
        res = res + str(c) + "\n"
    return res    
    


def powerset(iterable, n):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    "this implementation does not include empty set"
    s = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(1,n))


def findRestrictedTo(level, setOfValues, setOfCells):
    res = []
    for c in setOfCells:
        if setOfValues <= c.getBlockedAtLevel(level):
        #if setOfValues <= c.blockedValues:
            res.append(c)
    return setOfCells - set(res)

    
class ActionItem:
    def __init__(self, cells, values, subUnita = None, subUnitb = None):
        #subunit is the core subunit that was used to analyse
        self.subUnit = subUnita
        #othersubunit is a subunit that shares the self.cells with core subunit
        self.otherSubunit = subUnitb
        #cells subset of intersection of self.subUnit and self.otherSubunit
        self.cells  = cells
        #values aare symbols that msut be assigned to cells in self.cells
        self.values = values
        #insertBlocked
        #inferredBlockedValues 
        pass
#self.subUnit and self.otherSubunit null indicates a cell
#that is updated no further action  Set Value

#len(self.cells) = len(self.values) = 1. The cell value can be set
#no further action as the new value will handle restriction updates in later run

#subUnit and otherSubunit not null:  block self.cells with
#complement to self.values
#plus block  complement of cells in otherSubunit with self.values 
# subUnit not Null and otherSubunit null only perform first of
#actions above

# subUnit Null and  otherSubunit not null only perform 2. of actions above


    
    def updateBoard(self):
        if self.size() < 20:
            print("updating now", self.cells[0].key, self.values)
            self.cells[0].setValue(self.values[0])
            return True
        return False

    def __eq__(self, other):
        return (set(self.cells) == set(other.cells)) and\
            (set(self.values) == set(other.values)) and\
            self.subUnit == other.subunit

    def size(self):
        if len(self.cells) == 1:
            if self.subUnit:
                val = 11
            else:
                val = 1
        else: 
            val=len(self.cells)
            if self.subUnit:
                val = val + 100
            elif self.otherSubunit:
                val = val + 10
                
        return val
        
    def __lt__(self, other):
        
        return self.size() < other.size()
    
    def __str__(self):
        if not(self.subUnit) and not(self.otherSubunit):
            #set value directly#
            return "{}: Cell: {} Value = {} {}".format(
                "set value",self.cells[0].key, self.values, self.size())

        else:
            cellsText = ""
            for k in self.cells:
                cellsText = cellsText + str(k.key) + ","
                
            if len(self.cells) == 1 and self.subUnit:
                type = "set value in subunit"
            else:
                type = "constrain"

            if self.subUnit:
                return "{} {}  Cells: {} Values = {} {}".format(
                    type, self.subUnit.id, cellsText, self.values,
                    self.otherSubunit, self.size())
            elif self.otherSubunit:
                #print("found value")
                #print(self.otherSubunit)
                return "{}  Cells: {} Values = {} {} {}".format(
                    type, cellsText, self.values,
                    self.otherSubunit.id, self.size())
            else:
                print("found unknown action")








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
            
#    def insertValue(self, cellKey, v):
#        c = self.cellDict[cellKey]
#        c.setValue(v)
#        #c.value = v
#        #c.blockedValues = set([])
#        #for sub in self.getSubunitsFromCells([c]):
#        #    for c1 in sub.cells:
#        #        if c1 !=  c and not(c1.value):
#        #            print("inserted block", c1, c)
#        #            c1.blockedValues[0] = c1.blockedValues[0].union( set([v]))

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

    def scanCellsForValue(self, level = 0):
        res = []
        for c in self.cells:
            if not(c.value):
                blocked = c.getBlockedAtLevel(level)
                if len(blocked) == len(self.symbols) - 1:
                    res.append(ActionItem([c],list(self.symbols-set(blocked))))
                    #print(str(c), blocked)
                    #a=input()
        return res           

        
#CHECKCHECKCHECK the following uncommenting shoudl go out        
#        res1 = []
#        for c in self.cells:
#            if not(c.value):
#                blocked = []
#                for sub in c.belongsTo:
#                    for newCell in sub.cells:
#                        if newCell.value:
#                            blocked.append(newCell.value)
#                #print(blocked)
#                if len(set(blocked)) == len(self.symbols) -1:
#                    res1.append(ActionItem([c],list(self.symbols-set(blocked))))
#        #resolve this by setting cellc value to "
#        "the last variable in tuple above            "
#        print("Checking res firtst res")
#        for i in res:
#            print( i)
#        print("Now", res1)
#        for i in res1:
#            print (i)
#


    def otherSubunitsFromCells(self, restrictedCells, originSubunit):
        a = list(restrictedCells)
        #print(displayCellList(a))
        res = set(a[0].belongsTo)
        #print(displaySubunitList(res))
        for s in a[1:]:
            res = res.intersection(s.belongsTo)
        #print(displaySubunitList(list(res)))
        #print(displaySubunitList(list( res.difference(set([originSubunit])))))
        if len(res.difference(set([originSubunit]))) == 1:
            #for standard sudoku only possibility is 1 or zero
            #unless len restriced cells is one. Thes have been
            #handled elsewhere
            return res.difference(set([originSubunit])).pop()

        return None
                                     
        

    
    def scanForConstraints(self, level):
        "this calls powerset but does not include the full set"
        "nor does it full set minus one member"
        "the fullset minus one member correspods to what is investigated"
        "in scan cells for value"
        constraintsList = []
        
        for sub in self.subUnits:
            (openCells, remainingSymbols) = sub.getOpenCellsRemainingSymbols()
            #-2 below because -1 handled in scanCellsForValues
            #0 irrelevant handled separately afterwards
            #-1 not -2????
            for subRemainingSymbols in powerset(remainingSymbols,
                                                len(remainingSymbols) - 2):
                restricted = findRestrictedTo(
                    level, set(subRemainingSymbols), openCells)

                newSubunit = self.otherSubunitsFromCells(restricted, sub)
                if len(restricted) == len(subRemainingSymbols):
                    #print("added constraint")
                    constraintsList.append(
                        ActionItem(
                            list(restricted), list(subRemainingSymbols),
                            sub,  newSubunit))
                    #print(constraintsList[-1])
                elif len(restricted) <=3 and newSubunit:
                    #print("foundnew type")
                    #print(str(sub))
                    #print(displayCellList(restricted))
                    #print(str(newSubunit))
                    constraintsList.append(
                        ActionItem(
                            list(restricted), list(subRemainingSymbols),
                            None, newSubunit))
                    #print("newtype")
                    #print(constraintsList[-1])
                    #input()

        return(constraintsList)
                    
    def displayBlockedRow(self, level=0, row=2):
        for sub in self.subUnits:
            if isinstance(sub, Row) and sub.rowNo == row:
                res ="Blocked values level {} cells in row {}".format(level,row)
                for c in sub.cells:
                    res = res + "\ncol {} value: {}. ".format(c.key[0], c.value)
                    sortList = sorted(list(c.getBlockedAtLevel(level)))
                    for symb in sortList:
                        res = res + symb + ", "
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

def createStandardSudoku():
    symbols = set(['1','2','3','4','5','6','7','8','9'])
    allCells = [SudokuCell((i,j)) for j in range(9) for i in range(9)]
    allSubunits =[]

    for i in range(9):
        newRow = Row(i, symbols)
        for cell in allCells:
            if newRow.addCell(cell):
                 cell.addBelongsTo(newRow)
        allSubunits.append(newRow)

    for i in range(9):
        newCol = Col(i, symbols)
        for cell in allCells:
            if  newCol.addCell(cell):
                cell.addBelongsTo(newCol)
        allSubunits.append(newCol)

    for i in range(3):
        for j in range(3):
            newRegion = Region(j, i, symbols)
            for cell in allCells:
                if  newRegion.addCell(cell):
                    cell.addBelongsTo(newRegion)
            allSubunits.append(newRegion)


    return SudokuBoard(allCells, allSubunits, symbols)

                  



class SudokuSubunit():
    def __init__(self, name, symbols):
        self.id = name
        self.cells = []
        self.symbols = symbols

    def getUnusedValues(self, symbols):
        res = set([])
        for c in self.cells:
            if c.value:
                usedV = res.union(set(c.value))
        return symbols - usedV    
        

    def getOpenCellsRemainingSymbols(self):
        openCells = []
        taken = []
        for c in self.cells:
            if not(c.value):
                openCells.append(c)
            else:
                taken.append(c.value)
                
        return (set(openCells), self.symbols - set(taken))
        


    def __str__(self):
        res = self.id
        for c in self.cells:
            res = res + "{}:{} ".format(c.key, c.value)
        return res
    
class Row(SudokuSubunit):
    def __init__(self, no, symbols):
        SudokuSubunit.__init__(self,  "row{}".format(no), symbols)
        self.rowNo = no
                 
    def addCell(self, cell):
        returnValue = False
        if cell.key[1] == self.rowNo:
            self.cells.append(cell)
            returnValue = True

        return returnValue
        
class Col(SudokuSubunit):
    def __init__(self, no, symbols):
        SudokuSubunit.__init__(self,  "col{}".format(no), symbols)
        self.colNo = no

    def addCell(self, cell):
        returnValue = False
        if cell.key[0] == self.colNo:
            self.cells.append(cell)
            returnValue = True

        return returnValue
        

class Region(SudokuSubunit):
    def __init__(self, no1, no2, symbols):
        SudokuSubunit.__init__(self,  "region{}{}".format(no1,no2), symbols)
        self.rowRegion = no2
        self.colRegion = no1

    def addCell(self, cell):
        returnValue = False  
        if cell.key[1] // 3 == self.rowRegion and \
           cell.key[0] // 3 == self.colRegion:
            self.cells.append(cell)
            returnValue = True
        return returnValue


class SudokuCell:
    def __init__(self, key, value = ''):
        self.key=key
        self.value=value
        self.belongsTo = []
        self.blockedValues = {0: set([])}

    def setValue(self, v):
        self.value = v
        self.blockedValues[0] = set([])
        for sub in self.belongsTo:
            #print(sub)
            for c1 in sub.cells:
                if c1 !=  self and not(c1.value):
                    #print("inserted block", str(c1), str(self))
                    c1.blockedValues[0] = c1.blockedValues[0].union( set([v]))

        
    def getBlockedAtLevel(self, level):
        res = set([])
        for lev in range(level + 1):
            if lev in self.blockedValues:
                res = res.union (self.blockedValues[lev])
        return res
        
    def addBelongsTo(self, subUnit):
        self.belongsTo.append(subUnit)

    def __str__(self):
        return "Key: {}, {} ".format(self.key[0], self.key[1])
