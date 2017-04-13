__author__ = 'rsimpson'

from gobbletConstants import *
from gobbletPlayer import *
from gobbletAlphaBeta import *
from gobbletKindaSmart import *

class Board(object):
    # Used as a container for the Game
    def __init__(self, _p1, _p2):
        # keep a pointer to the first player (either a person or machine)
        self.p1 = _p1
        # keep a pointer to the second player (either a person or machine)
        self.p2 = _p2
        # start with an empty 4x4 board
        # each space on the board is a stack (implemented as a list)
        self.board = [[] for x in range(BOARD_SIZE)]

    def opponentPieces(self, _myName):
        '''
        I use this to get the set of pieces a player can use during a move
        '''
        # If I am player 1...
        if (self.p1.name == _myName):
            # send back player 2's pieces
            return self.p2.myPieces
        else:
            # otherwise send back player 1's pieces
            return self.p1.myPieces

    def positionOnBoard(self, _piece):
        '''
        This function returns the square in which a piece is located. The function
        returns -1 if the piece is not on the board
        '''
        # go through each square on the board
        for square in range(0, len(self.board)):
            # if there is at least one piece in this square
            if len(self.board[square]) > 0:
                # if the top piece matches...
                if self.board[square][-1] == _piece:
                    # return the index of the square
                    return square
        # otherwise, it's not on the board so return -1
        return -1

    def makeMove(self, _piece, _square):
        """
        Move a piece to a square - we assume the move has already been checked for legality
        """
        # find out if the piece is already on the board
        currentPosition = self.positionOnBoard(_piece)
        # remove the piece from its current position
        if (currentPosition >= 0):
            self.board[currentPosition].pop()
        # put the piece on the top of the stack in the new position
        self.board[_square].append(_piece)

    def undoMove(self, _square):
        """
        Remove (pop) the last item added to a square - I use this to undo a move
        """
        # make sure square is in bounds and there is at least one piece in that square
        if (_square in range(0, BOARD_SIZE)) and (len(self.board[_square]) > 0):
            # take the piece off the top of the stack and return it
            return self.board[_square].pop()

    def drawBoard(self):
        # Pretty-print the board.
        # we only print the top piece in each square
        for row in range(0, BOARD_LENGTH):
            for col in range(0, BOARD_LENGTH):
                square = row * BOARD_LENGTH + col
                # first row - empty square
                if len(self.board[square]) == 0 and col == 0:
                    print '\t',
                # first row - something in square
                elif len(self.board[square]) > 0 and col == 0:
                    print ' ' + self.board[square][-1] + '\t',
                # other row - something in square
                elif len(self.board[square]) > 0:
                    print '| ' + self.board[square][-1] + '\t',
                # other row - empty square
                else:
                    print '|\t',
            if row < BOARD_LENGTH - 1:
                print('\n-----------------')
        print ''

    def isWinner(self, _pieces):
        # Given a player's set of pieces, this function returns True if that player has won.
        #
        # four in a row
        #
        # for each row in the board...
        for row in range(0, BOARD_LENGTH):
            # start out assuming we have a winner
            foundWinner = True
            # for each column in this row...
            for col in range(0, BOARD_LENGTH):
                # get the index of the stack
                square = row * BOARD_LENGTH + col
                # if the stack is empty or the thing at the top of the stack is not your piece
                if (len(self.board[square]) == 0) or (self.board[square][-1] not in _pieces):
                    # this isn't a winner
                    foundWinner = False
                    # move on to next row
                    break
            # did we find a winner?
            if foundWinner:
                return True
        #
        # four in a column
        #
        # for each column in the board...
        for col in range(0, BOARD_LENGTH):
            # start out assuming we have a winner
            foundWinner = True
            # for each row in this column...
            for row in range(0, BOARD_LENGTH):
                # get the index of the stack
                square = row * BOARD_LENGTH + col
                # if the stack is empty or the thing at the top of the stack is not your piece
                if (len(self.board[square]) == 0) or (self.board[square][-1] not in _pieces):
                    # this isn't a winner
                    foundWinner = False
                    # move on to next row
                    break
            # did we find a winner?
            if foundWinner:
                return True
        #
        # four in a diagonal - left to right
        #
        # start out assuming we have a winner
        foundWinner = True
        # for each square on the left to right diagonal (0, 0), (1, 1), ...
        for sq in range(0, BOARD_LENGTH):
            # get the index of the stack
            square = sq * BOARD_LENGTH + sq
            # if the stack is empty or the thing at the top of the stack is not your piece
            if (len(self.board[square]) == 0) or (self.board[square][-1] not in _pieces):
                # this isn't a winner
                foundWinner = False
                # move on to next row
                break
        # did we find a winner?
        if foundWinner:
            return True
        #
        # four in a diagonal - right to left
        #
        # start out assuming we have a winner
        foundWinner = True
        # for each square on the left to right diagonal (0, 0), (1, 1), ...
        for sq in range(BOARD_LENGTH - 1, -1, -1):
            # get the index of the stack
            square = sq * BOARD_LENGTH + sq
            # if the stack is empty or the thing at the top of the stack is not your piece
            if (len(self.board[square]) == 0) or (self.board[square][-1] not in _pieces):
                # this isn't a winner
                foundWinner = False
                # move on to next row
                break
        # did we find a winner?
        return foundWinner

    def isSmaller(self, _piece1, _piece2):
        '''
        Return True if piece1 is smaller than piece2. If piece1 is the same size, or bigger than,
        piece2 then return False.
        '''
        if _piece1 in SMALL_PIECES and ((_piece2 in MEDIUM_PIECES) or (_piece2 in LARGE_PIECES)):
            return True
        elif _piece1 in MEDIUM_PIECES and _piece2 in LARGE_PIECES:
            return True
        return False

    def onBoard(self, _piece):
        '''
        We need to keep track of which pieces are on the board and can be moved
        '''
        # go through each square on the board
        for square in self.board:
            # if there is at least one piece in this square AND
            # the piece on top of the stack for this square is the piece we are looking for...
            if len(square) > 0 and square[-1] == _piece:
                # we can move it...
                return True
        # otherwise, the piece is not on the board in a moveable position
        return False

    def isHidden(self, _piece):
        '''
        We need to keep track of which pieces are on the board and underneath other pieces -
        which means they can't be moved
        '''
        # go through each square on the board
        for square in self.board:
            # if there are at least two pieces in this square...
            if (len(square) > 1):
                # look at all the pieces under the top piece...
                for p in range(0, len(square) - 1):
                    # if this is the piece we're looking for...
                    if square[p] == _piece:
                        # then it's hidden
                        return True
        # otherwise, the piece is not on the board or is in a moveable position
        return False

    def isLegalMove(self, _piece, _square, _printMessage = False):
        '''
        A move is legal if:
        * the square exists and
        * the square is empty or
        * the square is occupied by a smaller piece
        '''
        # make sure move is in bounds
        if not _square in range(0, BOARD_SIZE):
            if _printMessage:
                print "That square isn't on the board"
            return False
        # return false if the piece being moved is actually hidden under another piece on
        # the board
        # self.board is a list of stacks;
        # self.board[square] is a stack of gobblets in that square
        # self.board[square][-1] is the item at the end (top) of the stack
        if self.isHidden(_piece):
            if _printMessage:
                print "You are trying to move a piece that is underneath another piece"
            return False
        # return true if the square is empty
        if len(self.board[_square]) == 0:
            return True
        # if the square is occupied, check whether the piece in the square is smaller than
        # the piece being moved to the square
        if not self.isSmaller(self.board[_square][-1], _piece):
            if _printMessage:
                print "You are trying to put a piece on top of a piece that is the same size or larger"
            return False
        # check whether the piece is already on the board (pieces not on the board
        # need to be moved to an empty square)
        if not self.onBoard(_piece):
            if _printMessage:
                print "Pieces that are not on the board can only be placed in empty squares"
            return False
        # otherwise, it's legal
        return True

    def possibleNextMoves(self, _pieces):
        '''
        This function is used by the machine players to generate a list of all possible legal
        next moves.
        _pieces = list of all a player's pieces
        _onBoard = list of all a player's pieces that are on the board
        '''
        # start with an empty list of possible next moves
        possibleMoves = []
        # for every piece that can be moved...
        for piece in _pieces:
            # and all the squares on the board...
            for square in range(0, BOARD_SIZE):
                # if it's a legal move
                if self.isLegalMove(piece, square):
                    # add it to the list of possible moves
                    possibleMoves.append((piece, square))
        return possibleMoves


def switchPlayer(player, p1, p2):
    """
    Alternate between the two players
    """
    # if player one just went...
    if (player is p1):
        # switch to player two
        return p2
    # otherwise, player two just went...
    else:
        # so switch to player one
        return p1


def main():
    print("Welcome to Gobblet")
    # create the player objects
    #p1 = Player('X')
    p1 = KindaSmartMachine('X')
    #p2 = Player('O')
    p2 = AlphaBetaMachine('O')
    #p2 = KindaSmartMachine('O')
    # create the game board
    myBoard = Board(p1, p2)
    # keep track of how many turns we've had
    turnCount = 0
    # start with player 1
    player = p1
    # loop until we get a win or a draw
    while (True):
        # display the board
        myBoard.drawBoard()
        # say which player goes next
        print("Your move, " + player.name)
        # get the player's move - tuple of (piece, square)
        move = player.move(myBoard)
        # perform the player's move - tuple of (piece, square)
        myBoard.makeMove(move[0], move[1])
        # if we have a winner...
        if myBoard.isWinner(player.myPieces):
            # display the board
            myBoard.drawBoard()
            # say who won
            print(player.name + " won!")
            print "Number Of Turns: %d" % turnCount
            # break out of the loop
            break
        # if the board is full, then it's a draw
        elif turnCount > TURN_LIMIT * 2:
            # display the board
            myBoard.drawBoard()
            # say we have a tie
            print('The game is a tie!')
            print "Number Of Turns: %d" % turnCount
            # break out of the loop
            break
        else:
            # otherwise, switch players and repeat
            player = switchPlayer(player, p1, p2)
            # increment the turn count
            turnCount += 1


if __name__ == "__main__":
    main()

