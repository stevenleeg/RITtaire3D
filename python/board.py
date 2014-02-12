from PIL import Image, ImageDraw
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
        self.winning_line = []

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

    def generateWinningLine(self, direction, point):
        """
        Generates a winning line given a direction and a point
        """
        while self.validPoint(point):
            self.winning_line.append(point)
            point = (point[0] + direction[0],
                     point[1] + direction[1],
                     point[2] + direction[2])


    def checkWin(self, first_point):
        """
        Given a point, this checks to see if there is a win around it
        """
        complete_lines = {}
        for direction in self.directions:
            point = first_point
            cont = True
            s = -1
            while cont and self.validPoint(point):
                # Streak is over :(
                if self.getPoint(*point) != 1:
                    cont = False
                    continue

                s += 1
                point = (point[0] + direction[0],
                         point[1] + direction[1],
                         point[2] + direction[2])

            point = (point[0] - direction[0],
                     point[1] - direction[1],
                     point[2] - direction[2])
            complete_lines[direction] = s
            opposite = tuple([d * -1 for d in direction])
            if s == (self.n - 1):
                self.generateWinningLine(opposite, point)
                return True
            elif opposite in complete_lines and s + complete_lines[opposite] == (self.n - 1):
                self.generateWinningLine(opposite, point)
                return True

        return False

    def simulate(self):
        while len(self.remaining) > 0:
            if self.runTurn():
                break

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
    
    def renderImage(self):
        """
        This returns a PIL image of a graphical representation of the board.
        """
        SQUARE_SIZE = 30

        width = (self.n * SQUARE_SIZE) + 1
        height = ((self.n * SQUARE_SIZE) * self.n) + (self.n * SQUARE_SIZE) + 1

        image = Image.new("RGB", (width, height), color=(255, 255, 255))
        d = ImageDraw.Draw(image)

        for x, val in enumerate(self.board):
            for y, val in enumerate(self.board[x]):
                for z, val in enumerate(self.board[x][y]):
                    rx = x * SQUARE_SIZE
                    ry = (z * self.n * SQUARE_SIZE) + (y * SQUARE_SIZE) + (z * SQUARE_SIZE)

                    color = (238, 238, 238)
                    if (x, y, z) in self.winning_line:
                        color = (0, 180, 255)
                    elif val == 1:
                        color = (81, 81, 81)
                    d.rectangle((rx, ry, rx+SQUARE_SIZE, ry+SQUARE_SIZE), fill=color, outline=(255, 255, 255))

        del d

        return image
