__author__ = 'rsimpson'


"""
I started with minimax code that I found here:
http://callmesaint.com/python-minimax-tutorial/
That code was written by Matthew Griffin

Then I added in code I got from here:
https://inventwithpython.com/tictactoe.py
That code was written by Al Sweigart


Then I started adding my own code
"""
from gobbletConstants import *
from gobbletMachine import *
import copy

DEPTHLIMIT = 2

class AlphaBetaMachine(Machine):
    def __init__(self, _name):
        # call constructor for parent class
        Machine.__init__(self, _name)


    def Three_In_A_Row(self, _board, _pieces):
        # the unique combinations of how a player can have 3 pieces in a row, col, or diagonal
        # each number in the tuple correspond to a square on the game board
        combos = [(0,1,2), (0,1,3), (0,2,3), (1,2,3),               # row 1
                  (4,5,6), (4,5,7), (4,6,7), (5,6,7),               # row 2
                  (8,9,10), (8,9,11), (9,10,11), (9,10,11),         # row 3
                  (12,13,14), (12,13,15), (12,14,15), (13,14,15),   # row 4
                  (0,4,8), (0,4,12), (0,8,12), (4,8,12),            # col 1
                  (1,5,9), (1,5,13), (1,9,13), (5,9,13),            # col 2
                  (2,6,10), (2,6,14), (2,10,14), (6,10,14),         # col 3
                  (3,7,11), (3,7,15), (3,11,15), (7,11,15),         # col 4
                  (0,5,10), (0,5,15), (0,10,15), (5,10,15),         # diagonal top left to right bottom
                  (3,6,9), (3,6,12), (3,9,12), (6,9,12)]            # diagonal top right to bottom left

        # set the number of rows captured to 0
        In_A_Row = 0
        # each tuple is a combination of how to  get 3 in a row, column, or diagonal
        for c in combos:
            # if the list pieces in the square designated by combos has at least 1 piece each
            if len(_board.board[c[0]]) > 0 and len(_board.board[c[1]]) > 0 and len(_board.board[c[2]]) > 0:
                # if each of the 3 pieces in those squares belongs to the player
                if _board.board[c[0]][-1] in _pieces and _board.board[c[1]][-1] in _pieces and _board.board[c[2]][-1] in _pieces:
                    # the player has captured a row
                    In_A_Row += 1
        # return the amount of rows captured
        return In_A_Row

    def Killer(self, _board, p1, p2):
        # each unique combo of getting 3 in a row, with the 4th square being
        # taken by the opponent
        combos = [(0,1,2,3), (0,1,3,2), (0,2,3,1), (1,2,3,0),                   # row 1
                  (4,5,6,7), (4,5,7,6), (4,6,7,5), (5,6,7,4),                   # row 2
                  (8,9,10,11), (8,9,11,10), (9,10,11,8), (9,10,11,8),           # row 3
                  (12,13,14,15), (12,13,15,14), (12,14,15,13), (13,14,15,12),   # row 4
                  (0,4,8,12), (0,4,12,8), (0,8,12,4), (4,8,12,0),               # col 1
                  (1,5,9,13), (1,5,13,9), (1,9,13,5), (5,9,13,1),               # col 2
                  (2,6,10,14), (2,6,14,10), (2,10,14,6), (6,10,14,2),           # col 3
                  (3,7,11,15), (3,7,15,11), (3,11,15,7), (7,11,15,3),           # col 4
                  (0,5,10,15), (0,5,15,10), (0,10,15,5), (5,10,15,0),           # diagonal top left to right bottom
                  (3,6,9,12), (3,6,12,9), (3,9,12,6), (6,9,12,3)]               # diagonal top right to bottom left
        # set the number of rows captured to 0
        death = 0
        # each tuple is a combination of how to  get 3 in a row, column, or diagonal, the 4th number
        # in the tuple being the opponents piece
        for c in combos:
            # if the list of pieces in the square designated by combos has at least 1 piece in it
            if len(_board.board[c[0]]) > 0 and len(_board.board[c[1]]) > 0 and len(_board.board[c[2]]) > 0 \
                    and len(_board.board[c[3]]) > 0:
                # if each of the 3 pieces in those squares belongs to the player
                if _board.board[c[0]][-1] in p1 and _board.board[c[1]][-1] in p1 and\
                                _board.board[c[2]][-1] in p1:
                    # save the opponents piece in this row
                    Opponents_Piece = _board.board[c[3]][-1]
                    # loop through the players pieces
                    for piece in p1:
                    # check to see if the player has other pieces on the board that are moveable
                        square = _board.onBoard(piece)
                        # if there is, save it
                        if square == True:
                            board_piece = square
                            # now, make sure that this moveable piece is a different piece from the 3 in a row
                            if board_piece != _board.board[c[0]][-1] and board_piece != _board.board[c[1]][-1]:
                                if board_piece != _board.board[c[2]][-1]:
                                    # determine if the opponents piece is smaller than the player's piece
                                    # found else where on the board
                                    killer = _board.isSmaller(Opponents_Piece, board_piece)
                                    # if the opponents piece is smaller, the player would win if the player
                                    # gobbles up the opponent's piece in the row
                                    if killer == True:
                                        death += 1
        # return the value
        return death


    def Side_Control(self, _board, _pieces):
        # determine if a player has 2 pieces on a side of the board, as in the top middle, side middle on
        # either side, or bottom middle pieces
        combos = [(1,2), (4,8), (7,11), (13,14)]
        # the number of sides a player is holding
        Side_Pieces = 0
        # loop through the tuples in the combos list
        for c in combos:
            # if both squares in the tuple have pieces on them
            if len(_board.board[c[0]]) > 0 and len(_board.board[c[1]]) > 0:
                # and the top pieces of both squares is the players pieces
                if _board.board[c[0]][-1] in _pieces and _board.board[c[1]][-1] in _pieces:
                    # add this side to the players sides captured counted
                    Side_Pieces += 1

        return Side_Pieces



    def BiggerThan(self, _board, p1, p2):
        # This functions is used to determine if the player has more bigger pieces in play than
        # the opponent
        bigger = 0
        # loop through the pieces that the player has
        for pieces in p1:
            # determines if the current piece is in place on the board and is moveable
            square1 = _board.onBoard(pieces)
            # if the piece is on the board and moveable, save it to piece1
            if square1 == True:
                piece1 = pieces
            # if not, end this loops and continue at the next piece in the list
            else:
                continue
            # loop through the pieces that the opponent has
            for piece in p2:
                # determine if the current piece is in place on the board and is moveable
                square2 = _board.onBoard(piece)
                # if the piece is on the board and moveable, save it to piece2
                if square2 == True:
                    piece2 = piece
                    # if not, end this loop and continue to the next piece
                else:
                    continue
                # check to see if piece one is small than piece two
                isSmall = _board.isSmaller(piece1, piece2)
                # if piece 1 is bigger than piece two
                if isSmall == False:
                    # add 1 to number of bigger pieces
                    bigger += 1
        # return the amount of pieces that are bigger on the board
        return bigger

    def Eaten(self, _board, _pieces):
        # this function is used to determine how many pieces the player has gobbled
        hiding = 0
        # loop through opponents pieces
        for piece in _pieces:
            # if the piece is hidden
            hidden = _board.isHidden(piece)
            # add 1 to the hidden pieces count
            if hidden == True:
                hiding += 1
        # return the amount of pieces hidden
        return hiding

    def Board_Control(self, _board, p1, p2):
        # This function is used to see who has more moveable pieces on the board
        p1_pieces = 0
        p2_pieces = 0
        # loop through the players pieces
        for pieces in p1:
            # if the piece is on the board and moveable
            square1 = _board.onBoard(pieces)
            # add 1 to the players pieces count
            if square1 == True:
                p1_pieces += 1
        # loop through the opponents pieces
        for piece in p2:
            # if the piece is on the board and moveable
            square2 = _board.onBoard(piece)
            # add 1 to the opponents pieces
            if square2 == True:
                p2_pieces += 1
        # if the players has more pieces than the opponent on the board
        if p1_pieces > p2_pieces:
            # return the players piece count
            return p1_pieces
        # else return 0
        else:
            return 0

    def evaluationFunction(self, _board):
        # set the score for this state to 0
        score = 0

        # Test to see if the player can beat its opponent in a row. If a row, col, or diaginal, has 4 pieces,
        # 3 being the players, and the last is the opponent's, check to see if the player has a piece in play
        # that is larger than the opponents. If there is, that piece could be moved into place for the win.
        score += 1500 * self.Killer(_board, self.myPieces, self.name)
        score -= 1500 * self.Killer(_board, self.name, self.myPieces)

        # Test to see if there are 3 pieces in a row, col or in the 2 diagonals, adding points for the
        # player, and subtracting points for the opponent
        score += 500 * self.Three_In_A_Row(_board, self.myPieces)
        score -= 500 * self.Three_In_A_Row(_board, self.name)

        # players gain points for how many pieces they have gobbled up
        # if more pieces are gobbled up, that means the opponent has less pieces to use
        score += 100 * self.Eaten(_board, self.name)
        score -= 100 * self.Eaten(_board, self.myPieces)

        # if a player has more bigger pieces on the board, that means they can eat
        # more smaller pieces and increase their score
        score += 70 * self.BiggerThan(_board, self.myPieces, self.name)
        score -= 70 * self.BiggerThan(_board, self.name, self.myPieces)

        # Gain points for having more movable pieces on the board then the opponent
        score += 40 * self.Board_Control(_board, self.myPieces, self.name)
        score += 40 * self.Board_Control(_board, self.name, self.myPieces)

        # Gain points for the number of sides under a players control
        score += 20 * self.Side_Control(_board, self.myPieces)
        score -= 20 * self.Side_Control(_board, self.name)

        # return the calculated score for this state
        return score


    def atTerminalState(self, _board, _depth):
        """
        Checks to see if we've reached a terminal state. Terminal states are:
           * somebody won
           * we have a draw
           * we've hit the depth limit on our search
        Returns a tuple (<terminal>, <value>) where:
           * <terminal> is True if we're at a terminal state, False if we're not
           * <value> is the value of the terminal state
        """
        global DEPTHLIMIT
        # Yay, we won!
        if _board.isWinner(self.myPieces):
            # Return a positive number
            return (True, BIG_POSITIVE_NUMBER)
        # Darn, we lost!
        elif _board.isWinner(_board.opponentPieces(self.name)):
            # Return a negative number
            return (True, BIG_NEGATIVE_NUMBER)
        # if we've hit our depth limit
        elif (_depth >= DEPTHLIMIT):
            # use the evaluation function to return a value for this state
            return (True, self.evaluationFunction(_board))
        return (False, 0)

    def alphaBetaMax(self, _board, _depth = 0, _alpha = NEGATIVE_INFINITY, _beta = POSITIVE_INFINITY):
        '''
        This is the MAX half of alpha-beta pruning. Here is the algorithm:

        int alphaBetaMax( int alpha, int beta, int depthleft ) {
           if ( depthleft == 0 ) return evaluate();
           for ( all moves) {
              score = alphaBetaMin( alpha, beta, depthleft - 1 );
              if( score >= beta )
                 return beta;   // fail hard beta-cutoff
              if( score > alpha )
                 alpha = score; // alpha acts like max in MiniMax
           }
           return alpha;
        }
        '''
        #
        # At a terminal state
        #
        # check to see if we are at a terminal state - someone won or we hit our search limit
        terminalTuple = self.atTerminalState(_board, _depth)
        # if we are at a terminal state
        if terminalTuple[0] == True:
            # return the value of this state
            return (0, terminalTuple[1])
        #
        # Not at a terminal state, so search further...
        #
        # get all my legal moves
        possibleMoves = _board.possibleNextMoves(self.myPieces)
        # pick a random move as a default
        bestMove = random.choice(possibleMoves)
        # loop through all possible moves
        for m in possibleMoves:
            if (_depth == 0):
                print 'considering ' + str(m) + '...'
            # keep a copy of the old board
            oldBoard = copy.deepcopy(_board.board)
            # make the move - move is a tuple: (piece, square)
            _board.makeMove(m[0], m[1])
            # get the minimax vaue of the resulting state - returns a tuple (move, score)
            (mv, score) = self.alphaBetaMin(_board, _depth+1, _alpha, _beta)
            # undo the move
            _board.board = copy.deepcopy(oldBoard)
            # compare score to beta - can we prune?
            if (score >= _beta):
                return (mv, _beta)
            # compare score to alpha - have we found a better move?
            if (score > _alpha):
                # keep the better move
                bestMove = m
                # update alpha
                _alpha = score
        # return the best move we found
        return (bestMove, _alpha)

    def alphaBetaMin(self, _board, _depth, _alpha, _beta):
        '''
        This is the MIN half of alpha-beta pruning. Here is the general algorithm:

        int alphaBetaMin( int alpha, int beta, int depthleft ) {
           if ( depthleft == 0 ) return -evaluate();
           for ( all moves) {
              score = alphaBetaMax( alpha, beta, depthleft - 1 );
              if( score <= alpha )
                 return alpha; // fail hard alpha-cutoff
              if( score < beta )
                 beta = score; // beta acts like min in MiniMax
           }
           return beta;
        }
        '''
        #
        # At a terminal state
        #
        # check to see if we are at a terminal state - someone won or we hit our search limit
        terminalTuple = self.atTerminalState(_board, _depth)
        # if we are at a terminal state
        if terminalTuple[0] == True:
            # return the value of this state
            return (0, terminalTuple[1])
        #
        # Not at a terminal state, so search further...
        #
        # get all my opponent's legal moves
        possibleMoves = _board.possibleNextMoves(_board.opponentPieces(self.name))
        # pick a random move as a default
        bestMove = random.choice(possibleMoves)
        # consider all possible moves
        for m in possibleMoves:
            # keep a copy of the old board
            oldBoard = copy.deepcopy(_board.board)
            # make the move
            _board.makeMove(m[0], m[1])
            # get the minimax vaue of the resulting state - returns a tuple (move, score)
            (mv, score) = self.alphaBetaMax(_board, _depth+1, _alpha, _beta)
            # undo the move
            _board.board = copy.deepcopy(oldBoard)
            # compare score to alpha - can we prune?
            if (score <= _alpha):
                return (m, _alpha)
            # compare score to the best move we found so far
            if (score < _beta):
                _beta = score
        # send back the best move we found
        return (bestMove, _beta)

    def move(self, _board):
        m = self.alphaBetaMax(_board)[0]
        print "move = " + str(m)
        return m

