CSC200-project1
===============

This is the repository our group (House Tyrell) used for CSC 200 at the University of Rochester. The code here was written to assist in solving a hypothetical game, RITtaire3D (we were told the game was a challenge made for us by our neighboring school, RIT).

RITtaire3D is essentially a game of bingo played on a 3-dimensional cube of size n by n by n. The game is played by rolling 3 n-sided dice and placing a marker in the corresponding place on the board. Victory is achieved by getting an n-in-a-row line on the board.

## Simulator
The `python` directory contains the simulator we used to study this game and verify our theoretical results. It is a simple python program that can simulate many games on many different sized boards at a time. It is parallelized using Python's `multiprocessing` library, allowing for many game sizes to be simulated at the same time via a worker pool if you have a multi-core machine.
