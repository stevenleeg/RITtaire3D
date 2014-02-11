from board import Board
import datetime

N_START = 3
N_END = 4

def main():   
    total_turns = 0
    start_dt = datetime.datetime.now()

    for board_size in range(N_START, N_END):
        print "Simulating at n=%d..." % board_size
        b = Board(board_size)

        while len(b.remaining) > 0:
            if b.runTurn():
                break

        turns = b.getTurns()
        total_turns += turns
        if len(b.remaining) == 0:
            print "Done! No win for n=%d" % board_size
        else:
            print b
            print "Done! Finished after %d turns" % turns

    end_dt = datetime.datetime.now()
    delta = end_dt - start_dt 
    print "Simulation completed in %ds with %d turns (%f turns/s)" % (delta.seconds, total_turns, (delta.microseconds * 1000000) / float(total_turns))

if __name__ == "__main__":
    main()
