__author__ = 'rsimpson'

from gobbletPlayer import *

import random

class Machine(Player):
    def __init__(self, _name):
        # call constructor for parent class
        Player.__init__(self, _name)

    def chooseRandomly(self, _moves):
        """
        Given a list of potential moves, pick one at random and return it
        """
        # pick a move randomly
        moveIndex = random.randint(0, len(_moves) - 1)
        # send it back
        return _moves[moveIndex]

    def randomMove(self, _board):
        # get all open spaces
        possibleMoves = _board.possibleNextMoves()
        # pick a move randomly
        move = self.chooseRandomly(possibleMoves)
        # return the move chosen by the player
        return move

    def move(self, _board):
        return self.randomMove(_board)


