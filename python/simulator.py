from board import Board

def main():
    # Create the board
    b = Board(3)

    # Do three places
    b.place()
    b.place()
    b.place()

    # Display it
    print(b)

if __name__ == "__main__":
    main()
