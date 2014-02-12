from board import Board
import datetime

SAVE_IMAGE = False

SIMULATIONS = 3
N_START = 3
N_END = 16

def main():   
    total_turns = 0
    start_dt = datetime.datetime.now()
    nturns = {}

    print "Simulating %d to %d %d times..." % (N_START, N_END, SIMULATIONS)
    for simulation in range(0, SIMULATIONS):
        for board_size in range(N_START, N_END + 1):
            b = Board(board_size)

            b.simulate()

            turns = b.getTurns()
            total_turns += turns
            if SAVE_IMAGE:
                image = b.renderImage()
                image.save("output.png")

            if board_size in nturns:
                nturns[board_size] += turns
            else:
                nturns[board_size] = turns

        print "finished simulation %d" % simulation
    
    for n, total in nturns.items():
        print "Avg for %d is %f" % (n, float(total) / float(SIMULATIONS))

    end_dt = datetime.datetime.now()
    delta = end_dt - start_dt 
    print "Simulation completed in %ds with %d turns (%f turns/s)" % (delta.seconds, total_turns, (delta.microseconds * 1000000) / float(total_turns))

if __name__ == "__main__":
    main()
