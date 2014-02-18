from board import Board
import argparse, datetime

parser = argparse.ArgumentParser(description = "RITtaire3D simulator")
parser.add_argument("-n", metavar="N", dest="n", type=int,
    help="Runs one simulation with board size n")
parser.add_argument("-o", dest="save_image", action="store_true",
    help="Outputs a graphical representation of the board (to output.png)")
parser.add_argument("--ascii", dest="ascii", action="store_true",
    help="Outputs an ASCII representation of each board being simulated")
parser.add_argument("-s", metavar="N", dest="start", type=int,
    help="Begin simulated range at this board size (inclusive).")
parser.add_argument("-e", metavar="N", dest="end", type=int,
    help="End simulated range at this board size (inclusive).")
parser.add_argument("-t", metavar="t", dest="simulations", type=int,
    help="Simulate this range t times.")

def main():
    """
    Main function for the simulator. This parses the command line arguments
    and runs through the simulations, calculating statistics afterwards.
    """
    # Parse arguments
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

    if (args.start != None or args.end != None) and args.n != None:
        print "You cannot specify a range and a single board size!\n"
        parser.print_help()
        return

    if args.save_image and (args.simulations > 1 or args.n == None):
        print "You can only output images for single simulation runs\n"
        parser.print_help()
        return

    # Benchmarks
    total_turns = 0
    start_dt = datetime.datetime.now()
    stats = {}

    if n_start == n_end:
        print "Running size n=%d for %d simulations" % (n_start, simulations)
    else:
        print "Running range %d to %d for %d simulations..." % (
            n_start, n_end, simulations)
    print

    # Run throught the simulations
    for simulation in range(0, simulations):
        for board_size in range(n_start, n_end + 1):
            board = Board(board_size)

            board.simulate()

            turns = board.getTurns()
            total_turns += turns
            if board_size not in stats:
                stats[board_size] = {
                    "turns": 0,
                    "min": -1,
                    "max": -1,
                    "win_types": [0, 0, 0],
                }

            # Add to number of turns for board size
            stats[board_size]["turns"] += turns

            # Is this the max/min number of turns we've dealt with?
            if turns > stats[board_size]["max"]:
                stats[board_size]["max"] = turns
            if turns < stats[board_size]["min"] or stats[board_size]["min"] == -1:
                stats[board_size]["min"] = turns

            # Add to the win type
            stats[board_size]["win_types"][board.win_type] += 1

            if args.ascii:
                print board
            if simulations == 1:
                if args.save_image:
                    image = board.renderImage()
                    image.save("output.png")
                print "Finished board size %d" % board_size

        print "Finished simulation %d" % (simulation + 1)

    # Calculate averages
    print
    print "--- Results after %d simulations ---" % simulations
    for board_size, stat in stats.items():
        print "Stats for n=%d" % board_size
        print "\tAvg:          %f" % (float(stat["turns"]) / float(simulations))
        print "\tMax:          %d" % stat["max"]
        print "\tMin:          %d" % stat["min"]
        print "\t3D diag wins: %d" % stat["win_types"][0]
        print "\t2D diag wins: %d" % stat["win_types"][1]
        print "\tAxis wins:    %d" % stat["win_types"][2]
        print

    # More benchmarks
    end_dt = datetime.datetime.now()
    delta = end_dt - start_dt
    print "Simulation completed in %ds with %d turns (%f turns/s)" % (
        delta.seconds, total_turns,
        (delta.microseconds * 1000000) / float(total_turns))

if __name__ == "__main__":
    main()
