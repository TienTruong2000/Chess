import Board_v2 as Board
import Player_v2 as Player
import Pieces_v2 as Pieces
import pygame
import time


class Game:
    def __init__(self, size, player={'black': 'human', 'white': 'human'}):
        self.board = Board.Board(size)
        self.player1 = Player.Human('black') if player['black'] == 'human' else Player.Bot('black')
        self.player2 = Player.Human('white') if player['white'] == 'human' else Player.Bot('white')
        self.turn = self.player2
        self.opponent = self.player1
        self.player_is_moving = False
        self.moving_piece = None
        self.status = True
        self.winner = None
        self.history = []

    def setUp(self):
        colors = {'white': [1, 2], 'black': [8, 7]}
        # give player the pieces
        for color, rows in colors.items():
            player = self.player1 if color == 'black' else self.player2
            player.pieces.append(Pieces.Rook(color, (1, rows[0]), self.board.square_size))
            player.pieces.append(Pieces.Knight(color, (2, rows[0]), self.board.square_size))
            player.pieces.append(Pieces.Bishop(color, (3, rows[0]), self.board.square_size))
            player.pieces.append(Pieces.King(color, (4, rows[0]), self.board.square_size))
            player.pieces.append(Pieces.Queen(color, (5, rows[0]), self.board.square_size))
            player.pieces.append(Pieces.Bishop(color, (6, rows[0]), self.board.square_size))
            player.pieces.append(Pieces.Knight(color, (7, rows[0]), self.board.square_size))
            player.pieces.append(Pieces.Rook(color, (8, rows[0]), self.board.square_size))

            for x in range(1, 9):
                player.pieces.append(Pieces.Pawn(color, (x, rows[1]), self.board.square_size))
        # setup board
        for name in ['player1', 'player2']:
            player = getattr(self, name)
            for piece in player.pieces:
                pos = piece.pos
                self.board.setOccupant(pos, piece)

        # give the player sight on the board
        self.player1.board = self.board
        self.player2.board = self.board
        # give the player sight on the opponent
        self.player1.opponent = self.player2
        self.player2.opponent = self.player1
        # give bot to see the game
        if type(self.player1) is Player.Bot:
            self.player1.game = self
        if type(self.player2) is Player.Bot:
            self.player2.game = self



    def clickDetection(self, screen_pos):
        # the game will detect the click action and assign the suitable task
        pos = self.board.getChessPos(screen_pos)
        # check if pos is in chess square
        if pos is None:
            return

        # check if it is human turn
        if type(self.turn) is Player.Human:
            if self.player_is_moving:
                # if there is a player who is moving a piece and just clicked on the board: drop the piece
                old_square, next_square = self.turn.drop(pos)
                # compare the player old square and new square
                if old_square != next_square:
                    self.move(old_square, next_square)
                else:
                    old_square.occupant = self.moving_piece  # return the piece to its original place
                self.moving_piece = None
                self.player_is_moving = False

            else:
                # if no one is moving a piece and the player just clicked on the board: pick the piece
                self.moving_piece = self.turn.click(pos)
                if self.moving_piece is not None:
                    self.player_is_moving = True

    def changeTurn(self):
        self.turn = self.player1 if self.turn is self.player2 else self.player2
        self.opponent = self.player1 if self.turn is self.player2 else self.player2

    def isOver(self, square):
        # check that square is a King
        if type(square.occupant) is Pieces.King:
            self.status = False
            self.winner = self.turn

    def writeHistory(self, old_square, next_square):
        self.history.append(f'{self.moving_piece} {str(old_square)} {str(next_square)}')

    def checkPawn(self):
        if type(self.moving_piece) is Pieces.Pawn:  # set pawn first move
            self.moving_piece.first_move = False

    def move(self, old_square, next_square):
        # move the piece from old_square to next_square
        self.checkPawn()  # check Pawn first move
        if next_square.occupant is not None:  # check if the player eat a piece
            self.opponent.removePiece(next_square.occupant)
            self.isOver(next_square)  # check if the game is over
            self.turn.score += next_square.occupant.value
        self.writeHistory(old_square, next_square)  # write history
        next_square.occupant = self.moving_piece  # move the piece to the new square
        self.moving_piece.pos = next_square.pos  # update the piece position
        self.changeTurn()



    def botMove(self):
        if type(self.turn) is Player.Bot:
            old_square, next_square = self.turn.chooseMove()  # bot will make a move
            # remember bot moving piece
            self.moving_piece = old_square.occupant
            piece = old_square.occupant
            # delete moving piece on board
            old_square.occupant = None
            # move the piece
            self.move(old_square, next_square)
            self.moving_piece = None
            return piece, next_square.left_up_corner
        else:
            return None, None



if __name__ == '__main__':
    pygame.init()
    pygame.display.set_mode((0, 0))
    game = Game(600)
    game.setUp()
    print(game.board)
