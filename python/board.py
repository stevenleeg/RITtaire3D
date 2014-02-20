try:
    from PIL import Image, ImageDraw
except ImportError:
    pass
import random

class Board:
    """
    Represents a board of RITtaire3D
    """
    WIN_DIAG3D = 0
    WIN_DIAG2D = 1
    WIN_AXIS   = 2

    def __init__(self, n):
        """
        Initializes a n by n by n board as a 3D array
        """
        self.board = []
        self.remaining = []
        self.directions = []
        self.n = n
        self.winning_line = []
        self.win_type = 0

        self.generateDirectionalConstants()

        for x in range(0, n):
            self.board.append([])
            for y in range(0, n):
                self.board[x].append([])
                for z in range(0, n):
                    self.board[x][y].append(False)
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
                        continue

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
        self.setPoint(point[0], point[1], point[2], True)

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
        """
        Calculates whether or not this point is on an edge of the cube
        """
        for coord in point:
            if coord == (self.n - 1) or coord == 0:
                return True

    def generateWinStats(self, direction, point):
        """
        Generates the winning line given a direction and a point,
        also determins what kind of win this was (diag, x, y, etc.)
        """
        self.win_type = list(direction).count(0)

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
            streak = -1
            while cont and self.validPoint(point):
                # Streak is over :(
                if self.getPoint(*point) != True:
                    cont = False
                    continue

                streak += 1
                point = (point[0] + direction[0],
                         point[1] + direction[1],
                         point[2] + direction[2])

            point = (point[0] - direction[0],
                     point[1] - direction[1],
                     point[2] - direction[2])
            complete_lines[direction] = streak
            opposite = tuple([d * -1 for d in direction])
            if streak == (self.n - 1):
                self.generateWinStats(opposite, point)
                return True
            elif(opposite in complete_lines and
                    streak + complete_lines[opposite] == (self.n - 1)):
                self.generateWinStats(opposite, point)
                return True

        return False

    def simulate(self):
        """
        Runs through a complete simulation of the game, stopping
        only if there is a win or the entire board is full
        """
        while len(self.remaining) > 0:
            if self.runTurn():
                break

    def __str__(self):
        """
        Ideally I'll get a scipy 3D representation going, but for now this
        will have to do. This special function lets you do print(my_board)
        and have it come out looking pretty.
        """
        string = "Board size: %d\n" % self.n
        string += "Turns:      %d" % self.getTurns()
        current_z = 0
        for z in range(0, self.n):
            string += "\n"
            for y in range(0, self.n):
                for x in range(0, self.n):
                    if (x, y, z) in self.winning_line:
                        string += "[x] "
                    elif(self.board[x][y][z] == 1):
                        string += "[o] "
                    else:
                        string += "[ ] "
                string += "\n"

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
                    ry = (z * self.n * SQUARE_SIZE) + (y * SQUARE_SIZE) \
                        + (z * SQUARE_SIZE)

                    color = (238, 238, 238)
                    if (x, y, z) in self.winning_line:
                        color = (0, 180, 255)
                    elif val == 1:
                        color = (81, 81, 81)

                    d.rectangle((rx, ry, rx+SQUARE_SIZE, ry+SQUARE_SIZE),
                            fill=color,
                            outline=(255, 255, 255))
        del d

        return image
