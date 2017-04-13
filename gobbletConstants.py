# define the size of the board (NxN)
BOARD_LENGTH = 4
BOARD_SIZE = BOARD_LENGTH * BOARD_LENGTH

# define pieces owned by X and O
X_PIECES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
Y_PIECES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']

# define small, medium and large pieces - for use when comparing the size of pieces
SMALL_PIECES = ['A', 'B', 'C', 'D', 'a', 'b', 'c', 'd']
MEDIUM_PIECES = ['E', 'F', 'G', 'H', 'e', 'f', 'g', 'h']
LARGE_PIECES = ['I', 'J', 'K', 'L', 'i', 'j', 'k', 'l']

# how many turns does each player get before we declare a draw?
TURN_LIMIT = 50

# define the maximum positive number returned by the evaluation function
BIG_POSITIVE_NUMBER = 10000
BIG_NEGATIVE_NUMBER = -1 * BIG_POSITIVE_NUMBER
POSITIVE_INFINITY = BIG_POSITIVE_NUMBER * 10
NEGATIVE_INFINITY = -POSITIVE_INFINITY