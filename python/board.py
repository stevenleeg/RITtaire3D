import random

class Board:
    def __init__(self, n):
        """
        Initializes a n by n by n board as a 3D array
        """
        self.board = []
        self.remaining = []
        self.n = n

        for x in range(0, n):
            self.board.append([])
            for y in range(0, n):
                self.board[x].append([])
                for z in range(0, n):
                    self.board[x][y].append(0)
                    self.remaining.append((x, y, z))

    def roll(self):
        """
        Selects a random element from the non-selected items
        """
        i = random.randrange(0, len(self.remaining))
        return self.remaining.pop(i)
    
    def getPoint(self, x, y, z):
        """
        Returns the data at point x, y, z on the board
        """
        return self.board[x][y][z]
    
    def setPoint(self, x, y, z, val):
        """
        Sets a point on the board
        """
        self.board[x][y][z] = val

    def runTurn(self):
        """
        Rolls the die and places a piece on the selected place within
        the board. Returns true if there is a win after this turn, false
        otherwise
        """
        point = self.roll()
        self.setPoint(point[0], point[1], point[2], 1)

        return self.checkWin(point)

    def getTurns(self):
        """
        Returns the number of turns made on this board
        """
        return self.n^3 - len(self.remaining)

    def checkWin(self, point):
        """
        Given a point, this checks to see if there is a win around it
        """
        # TODO
        return False

    def __str__(self):
        """
        Ideally I'll get a scipy 3D representation going, but for now this
        will have to do. This special function lets you do print(my_board)
        and have it come out looking pretty.
        """
        string = ""
        for x, val in enumerate(self.board):
            for y, val in enumerate(self.board[x]):
                for z, val in enumerate(self.board[x][y]):
                    string += "(%d, %d, %d): %d\n" % (x, y, z, self.board[x][y][z])

        return string
