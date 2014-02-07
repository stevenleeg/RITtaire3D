from board import Board
import datetime

N_START = 1
N_END = 40

def main():   
    total_turns = 0
    start_dt = datetime.datetime.now()
    for n in range(N_START, N_END):
        print "Simulating at n=%d..." % n
        b = Board(n)
        while len(b.remaining) > 0:
            if b.runTurn():
                break

        turns = b.getTurns()
        total_turns += turns
        if b.remaining == 0:
            print "Done! No win for n=%d" % n
            #print b
        else:
            print "Done! Finished after %d turns" % turns
            #print b

    end_dt = datetime.datetime.now()
    delta = end_dt - start_dt 
    print "Simulation completed in %ds with %d turns (%f turns/s)" % (delta.seconds, total_turns, (delta.microseconds * 1000000) / float(total_turns))

if __name__ == "__main__":
    main()
