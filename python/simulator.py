from board import Board

N_START = 1
N_END = 4


def main():   
    for n in range(N_START, N_END):
        print "Simulating at n=%d..." % n
        b = Board(n)
        while len(b.remaining) > 0:
            if b.runTurn():
                break

        if b.remaining == 0:
            print "Done! No win for n=%d" % n
        else:
            print "Done! Finished after %d turns" % b.getTurns()

if __name__ == "__main__":
    main()
