__author__ = 'rsimpson'

from gobbletMachine import *
import copy
import random

class KindaSmartMachine(Machine):
    def __init__(self, name):
        # call constructor for parent class
        Machine.__init__(self, name)

    def blockingMove(self, _myMoves, _square):
        '''
        Return the first available move that takes the given square
        '''
        # loop through all our available moves
        for move in _myMoves:
            # does this move take the target square?
            if (move[1] == _square):
                # pick it
                return move
        # no move takes the square, so send back a random move
        return random.choice(_myMoves)

    def kindOfSmart(self, _board):
        # get all my legal moves
        myPossibleMoves = _board.possibleNextMoves(self.myPieces)
        #
        # First, check if we can win in the next move
        #
        # loop through all possible moves
        for move in myPossibleMoves:
            # keep a copy of the old board
            oldBoard = copy.deepcopy(_board.board)
            # make the move - move is a tuple: (piece, square)
            _board.makeMove(move[0], move[1])
            # check to see whether this move wins
            if _board.isWinner(self.myPieces):
                # undo the move
                _board.board = copy.deepcopy(oldBoard)
                # return the winning move
                return move
            else:
                # undo the move
                _board.board = copy.deepcopy(oldBoard)
        #
        # Then, check if opponent can win in the next move and block them
        #
        # get all my opponent's legal moves
        yourPossibleMoves = _board.possibleNextMoves(_board.opponentPieces(self.name))
        # loop through all possible moves
        for move in yourPossibleMoves:
            # keep a copy of the old board
            oldBoard = copy.deepcopy(_board.board)
            # make the move - move is a tuple: (piece, square)
            _board.makeMove(move[0], move[1])
            # check to see whether this move wins for the opponent
            if _board.isWinner(_board.opponentPieces(self.name)):
                # undo the move
                _board.board = copy.deepcopy(oldBoard)
                # return a legal blocking move
                return self.blockingMove(myPossibleMoves, move[1])
            else:
                # undo the move
                _board.board = copy.deepcopy(oldBoard)
        #
        # Pick a move randomly
        #
        return random.choice(myPossibleMoves)

    def move(self, _board):
        m = self.kindOfSmart(_board)
        print "move = " + str(m)
        return m

