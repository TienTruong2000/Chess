import Board_v2 as Board
import Pieces_v2 as Pieces
import copy


class Players:
    def __init__(self, color, pieces=None):
        self.color = color
        self.pieces = pieces
        self.score = 0
        self.board = Board.Board()
        self.old_square = None  # if player click then remember the old square
        self.moving_piece = None  # if player is moving a piece
        self.opponent = None

    def getPossibleMove(self, piece):
        def KnightMove():
            for pos in occupant.getMove(L_shape=True):
                # get all possible L_shape Move
                square = self.board.findSquare(pos)
                if square.occupant is None:
                    possible_moves.append(square)
                elif square.occupant not in self.pieces:
                    possible_eats.append(square)

        def getMove(action, condition):
            def pawnMoveCondition(moves):
                is_block = False
                for pos in moves:
                    if is_block:
                        break
                    square = self.board.findSquare(pos)
                    if square.occupant is None:
                        possible_moves.append(square)
                    else:
                        is_block = True

            def pawnEatCondition(moves):
                is_block = False
                for pos in moves:
                    if is_block:
                        break
                    square = self.board.findSquare(pos)
                    if square.occupant is None:
                        is_block = True
                    else:
                        if square.occupant in self.pieces:
                            is_block = True
                        else:
                            possible_eats.append(square)
                            is_block = True

            def piecesMoveCondition(moves):
                is_block = False  # check if that direction is blocked by a friendly piece
                for pos in moves:
                    if is_block:
                        break
                    square = self.board.findSquare(pos)
                    if square.occupant is None:
                        possible_moves.append(square)
                    else:
                        if square.occupant in self.pieces:
                            is_block = True
                        else:
                            possible_eats.append(square)
                            is_block = True

            # get possible square in piece's movement
            for direction, step in getattr(occupant, action).items():
                moves = occupant.getMove(direction, step)  # get possible move to the 'direction'
                # choose suitable square based on their movement condition
                choose = eval(condition)
                choose(moves)

        occupant: Pieces = piece
        possible_moves = []  # posible move
        possible_eats = []  # possible opponet pieces to eat
        if type(occupant) is Pieces.Knight:
            KnightMove()
        elif type(occupant) is Pieces.Pawn:
            getMove('move', 'pawnMoveCondition')
            getMove('eat', 'pawnEatCondition')
        else:
            getMove('move', 'piecesMoveCondition')
        possible_moves.extend(possible_eats)
        return possible_moves

    def removePiece(self, piece):
        for index, p in enumerate(self.pieces):
            if p == piece:
                self.pieces.pop(index)
                return


class Human(Players):
    def __init__(self, color):
        Players.__init__(self, color, [])

    def click(self, pos: tuple) -> Pieces:
        # if player click a piece then remove that piece on the board
        # and player remember the selected piece and the old square
        # return the moving piece
        square = self.board.findSquare(pos)
        if square.occupant is None or square.occupant not in self.pieces:
            return None
        self.moving_piece = square.occupant
        self.old_square = square
        square.occupant = None
        return self.moving_piece

    def drop(self, pos):
        # decide if the pos is legal
        # true: return the old square and the new square
        # false: return the old square
        next_square = self.board.findSquare(pos)
        # check if the player click on the old square again
        if next_square == self.old_square:
            self.old_square = None
            return next_square, next_square
        else:
            # check if the next square is not the same color
            if next_square.occupant not in self.pieces:
                possible_move = self.getPossibleMove(self.moving_piece)
                # check if the next square is legal move
                if next_square in possible_move:
                    return self.old_square, next_square
            return self.old_square, self.old_square


import random


def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("{} finnished in {}".format(func.__name__, end - start))
        return result

    return wrapper


class Bot(Players):
    def __init__(self, color, game=None):
        Players.__init__(self, color, [])
        self.game = game

    #@timer
    def chooseMove(self):
        max = float('-inf')
        max_old_square = []
        max_new_square = []
        a = []
        b = []
        c = []
        for piece in self.pieces:
            possible_move = self.getPossibleMove(piece)
            for move in possible_move:
                new_game = copy.deepcopy(self.game)
                old_square = self.board.findSquare(piece.pos)
                new_square = move
                self.simulate(old_square.pos, new_square.pos, new_game)
                point = self.minimax(new_game, 0)
                #a.append(old_square)
                #b.append(new_square)
                #c.append(point)
                if max < point:
                    max = point
                    max_old_square = [old_square]
                    max_new_square = [new_square]
                elif max == point:
                    max_old_square.append(old_square)
                    max_new_square.append(new_square)
        index = random.randint(0, len(max_old_square) - 1)
        return max_old_square[index], max_new_square[index]

    def simulate(self, old_pos, next_pos, game):
        old_square = game.board.findSquare(old_pos)
        next_square = game.board.findSquare(next_pos)
        # remember bot moving piece
        game.moving_piece = old_square.occupant
        # delete moving piece on board
        old_square.occupant = None
        # move the piece
        game.checkPawn()
        if next_square.occupant is not None:  # check if the player eat a piece
            game.opponent.removePiece(next_square.occupant)
            game.turn.score += next_square.occupant.value
        next_square.occupant = game.moving_piece  # move the piece to the new square
        game.moving_piece.pos = next_square.pos  # update the piece position
        game.changeTurn()
        game.moving_piece = None

    def minimax(self, game, layer):
        if layer == 1:
            return game.turn.score - game.opponent.score

        max = float('-inf')
        min = float('+inf')
        for piece in game.turn.pieces:
            possible_move = game.turn.getPossibleMove(piece)
            for move in possible_move:
                new_game = copy.deepcopy(game)
                old_square = game.board.findSquare(piece.pos)
                new_square = move
                self.simulate(old_square.pos, new_square.pos, new_game)
                point = self.minimax(new_game, layer + 1)
                if max < point:
                    max = point
                if min > point:
                    min = point
        if game.turn == self:
            return max
        else:
            return min
