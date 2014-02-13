from board import Board
import argparse, datetime

parser = argparse.ArgumentParser(description = "RITtaire3D simulator")
parser.add_argument("-n", metavar="N", dest="n", type=int, 
        help="Runs one simulation with board size n")
parser.add_argument("-o", dest="save_image", action="store_true",
        help="Outputs a graphical representation of the board (saves to output.png)")
parser.add_argument("-s", metavar="N", dest="start", type=int, 
        help="Begin simulated range at this board size (inclusive).")
parser.add_argument("-e", metavar="N", dest="end", type=int, 
        help="End simulated range at this board size (inclusive).")
parser.add_argument("-t", metavar="t", dest="simulations", type=int, 
        help="Simulate this range t times.")

def main():   
    args = parser.parse_args()
    if args.start != None and args.end != None:
        n_start = args.start
        n_end = args.end
    elif args.n != None:
        n_start = args.n
        n_end = args.n

    simulations = 1
    if args.simulations != None:
        simulations = args.simulations

    if (args.start == None or args.end == None) and args.n == None:
        parser.print_help()
        return

    total_turns = 0
    start_dt = datetime.datetime.now()
    nturns = {}

    if n_start == n_end:
        print "Running size n=%d for %d simulations" % (n_start, simulations)
    else:
        print "Running range %d to %d for %d simulations..." % (n_start, n_end, simulations)
    print

    for simulation in range(0, simulations):
        for board_size in range(n_start, n_end + 1):
            b = Board(board_size)

            b.simulate()

            turns = b.getTurns()
            total_turns += turns
            if args.save_image:
                image = b.renderImage()
                image.save("output.png")

            if board_size in nturns:
                nturns[board_size] += turns
            else:
                nturns[board_size] = turns

        print "Finished simulation %d" % simulation
    
    for n, total in nturns.items():
        print "\nAvg for %d is %f" % (n, float(total) / float(simulations))

    end_dt = datetime.datetime.now()
    delta = end_dt - start_dt 
    print "Simulation completed in %ds with %d turns (%f turns/s)" % (delta.seconds, total_turns, (delta.microseconds * 1000000) / float(total_turns))

if __name__ == "__main__":
    main()
