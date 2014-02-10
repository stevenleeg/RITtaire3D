import random

class Board:
    def __init__(self, n):
        """
        Initializes a n by n by n board as a 3D array
        """
        self.board = []
        self.remaining = []
        self.directions = []
        self.n = n

        self.generateDirectionalConstants()

        for x in range(0, n):
            self.board.append([])
            for y in range(0, n):
                self.board[x].append([])
                for z in range(0, n):
                    self.board[x][y].append(0)
                    self.remaining.append((x, y, z))

    def generateDirectionalConstants(self):
        """
        Generates a list of tuples for every possible direction we
        could go in. Eg, the direction straight up would be (0, 1, 0)
        """
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    if x == 0 and y == 0 and z == 0:
                        break
                    self.directions.append((x, y, z))

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
        return self.n**3 - len(self.remaining)

    def validPoint(self, point):
        """
        Checks to see if a point is valid on the current board. 
        Returns True/False.
        """
        for coord in point:
            if coord >= self.n or coord < 0:
                return False

        return True
    
    def onEdge(self, point):
        for coord in point:
            if coord == (self.n - 1) or coord == 0:
                return True

    def checkWin(self, point):
        """
        Given a point, this checks to see if there is a win around it
        """
        remaining = {}
        complete_lines = []
        for direction in self.directions:
            remaining[direction] = None

        while len(remaining) != 0:
            for direction, check_point in remaining.items():
                # For the first point
                if check_point == None: 
                    check_point = point

                next_point = (check_point[0] + direction[0],
                              check_point[1] + direction[1],
                              check_point[2] + direction[2])

                # If the point is invalid then we're done here
                if not self.validPoint(next_point):
                    del(remaining[direction])
                    continue

                # We should keep following this line
                if self.getPoint(*next_point) == 1:
                    remaining[direction] = next_point

                    # If it's on the edge, we have 1/2 of a complete line
                    if self.onEdge(next_point):
                        complete_lines.append(direction)

                        # Check for a win
                        opposite = tuple([d * -1 for d in direction])
                        if opposite in complete_lines:
                            return True

                        del(remaining[direction])
                else:
                    del(remaining[direction])

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
