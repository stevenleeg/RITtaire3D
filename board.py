import random

class Board:
    def __init__(self, n):
        """
        Initializes a n by n by n board as a 3D array
        """
        self.board = []
        self.n = n

        for x in range(0, n):
            self.board.append([])
            for y in range(0, n):
                self.board[x].append([])
                for z in range(0, n):
                    self.board[x][y].append(0)

    def roll(self):
        """
        Simulates 3 rolls of the die and returns a tuple with the
        results
        """
        # TODO: This is naive. Need to make this take placed points into account
        x = random.randrange(self.n)
        y = random.randrange(self.n)
        z = random.randrange(self.n)

        return (x, y, z)
    
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

    def place(self):
        """
        Rolls the die and places a piece on the selected place within
        the board.
        """
        current = 1
        point = self.roll() 
        # TODO: We won't have to do this when we have a smarter die
        while current != 0:
            point = self.roll()
            current = self.getPoint(*point)

        self.setPoint(point[0], point[1], point[2], 1)

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
