__author__ = 'rsimpson'

class Player():
    def setup(self, _opponent, _pieces):
        # name of player's opponent
        self.opponent = _opponent
        # all of player's pieces
        self.myPieces = _pieces
        # player's pieces that can be moved
        self.moveablePieces = self.myPieces[:]

    def __init__(self, _myName):
        # name of this player - either X or O
        self.name = _myName
        # initialize the rest of the values
        if _myName == 'X':
            self.setup('O', ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L'])
        else:
            self.setup('X', ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'])

    def updateStacks(self, _board):
        '''
        We need to keep track of which pieces are on the board and can be moved
        '''
        # reset list of pieces that can be moved
        self.moveablePieces = self.myPieces[:]
        # reset list of pieces that are on board or can be moved
        self.onBoard = []
        # go through each square on the board
        for square in _board.board:
            # if there is more than one piece in this square
            if len(square) > 1:
                # for all the items beneath the top item in the stack...
                for p in range(0, len(square) - 1):
                    # if the piece is in our list of moveable pieces...
                    if square[p] in self.moveablePieces:
                        # take it out
                        self.moveablePieces.remove(square[p])

    def move(self, _board):
        '''
        Players can make the following moves on each turn:
        * Put a gobblet from an external stack onto an empty space on the board
        * Move a gobblet on the board to another empty square as long as that gobblet is visible (i.e., not covered)
        * Move a gobblet on the board to cover a smaller gobblet

        Moves are a tuple defined as (piece, square), where:
        * piece is 'A'..'L' or 'a'..'l' (depending on whether the player is X or O
        * square is 0..15
        '''
        # update the list of pieces that can be moved
        self.updateStacks(_board)
        # Which piece will be moved?
        prompt = 'Choose a piece ' + str(self.moveablePieces) + ':'
        # get input from keyboard
        piece = raw_input(prompt)
        # keep asking until we get valid input
        while piece not in self.moveablePieces:
            print "That piece can't be moved"
            # get input from keyboard
            piece = raw_input(prompt)
        # Which square will the piece be moved to?
        # get input from keyboard
        square = int(raw_input("Choose a square: "))
        # keep seeking input until we get an integer that corresponds to a legal move on the board
        while (not _board.isLegalMove(piece, int(square), True)):
            # get input from keyboard
            square = int(raw_input("Choose a square: "))
        # return the move
        return (piece, int(square))


