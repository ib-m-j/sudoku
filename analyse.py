import userinterface


cellKeys = [(i,j) for i in range(8) for j in range(8)]


class SudokuSubunit:
    pass

class SudokuCell:
    def __init__(key, value):
        self.key=key
        self.value=value

    


if __name__ == '__main__':
    print("start")
    cells = userinterface.getBoard(cellKeys)
    print(cells)
