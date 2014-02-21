from board import Board
import argparse, datetime, multiprocessing

BLOCK_SIZE = 4

parser = argparse.ArgumentParser(description = "RITtaire3D simulator")
parser.add_argument("-n", metavar="N", dest="n", type=int,
    help="Runs one simulation with board size n")
parser.add_argument("-i", dest="save_image", action="store_true",
    help="Outputs a graphical representation of the board (to output.png)")
parser.add_argument("--ascii", dest="ascii", action="store_true",
    help="Outputs an ASCII representation of each board being simulated")
parser.add_argument("-o", dest="output", action="store_true",
    help="Writes data output to file")
parser.add_argument("-s", metavar="N", dest="start", type=int,
    help="Begin simulated range at this board size (inclusive).")
parser.add_argument("-e", metavar="N", dest="end", type=int,
    help="End simulated range at this board size (inclusive).")
parser.add_argument("-t", metavar="t", dest="simulations", type=int,
    help="Simulate this range t times.")

def runSimulation(s, board_size, g_stats):
    stats = {
        "turns": 0,
        "min": -1,
        "max": -1,
        "win_types": [0, 0, 0]
    }

    for sim in range(0, s + 1):
        board = Board(board_size)

        board.simulate()
        turns = board.getTurns()
        stats["turns"] += board.getTurns()
        if turns > stats["max"]:
            stats["max"] = turns
        if turns < stats["max"]:
            stats["min"] = turns

        stats["win_types"][board.win_type] += 1

    g_stats[board_size] = stats

    print "Finished simulations for n=%d" % board_size

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

    if n_start == n_end:
        print "Running size n=%d for %d simulations" % (n_start, simulations)
    else:
        print "Running range %d to %d for %d simulations..." % (
            n_start, n_end, simulations)
    print

    # Run the simulations
    simulations_left = range(0, simulations)
    pool = multiprocessing.Pool()
    manager = multiprocessing.Manager()
    stats = manager.dict()
    for board_size in range(n_start, n_end):
        pool.apply_async(runSimulation, (simulations, board_size, stats))

    pool.close()
    pool.join()

    # Calculate averages
    out_str = ""
    total_turns = 0
    out_str += "--- Results after %d simulations ---\n" % simulations
    for board_size, stat in stats.items():
        out_str += "Stats for n=%d\n" % board_size
        out_str += "\tAvg:          %f\n" % (float(stat["turns"]) / float(simulations))
        out_str += "\tMax:          %d\n" % stat["max"]
        out_str += "\tMin:          %d\n" % stat["min"]
        out_str += "\t3D diag wins: %d\n" % stat["win_types"][0]
        out_str += "\t2D diag wins: %d\n" % stat["win_types"][1]
        out_str += "\tAxis wins:    %d\n" % stat["win_types"][2]
        out_str += "\n"
        total_turns += stat["turns"]

    # More benchmarks
    end_dt = datetime.datetime.now()
    delta = end_dt - start_dt
    out_str +="Simulation completed in %ds with %d turns (%f turns/s)\n" % (
        delta.seconds, total_turns,
        (delta.microseconds * 1000000) / float(total_turns))

    print
    print out_str
    if(args.output != None):
        with open("output.txt", "w") as f:
            f.write(out_str)
        print "\nWrote output to output.txt"

if __name__ == "__main__":
    main()
