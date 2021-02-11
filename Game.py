import Chess.Board as Board
import Chess.Pieces as Pieces
import Chess.Player as Player


class Game:
    def __init__(self):
        self.board = Board.Board()
        #self.player1 = Player.Player('black')
        #self.player2 = Player.Player('white')
        self.turn = 'black'
        self.player_moving = False
        self.status = True
        self.winner = None

    def setUp(self):
        # set up the fucking board
        colors = {'white': [1, 2], 'black': [8, 7]}
        for color, rows in colors.items():
            self.board.setOccupant(('A', rows[0]), Pieces.Rook(color, 'A', rows[0]))
            self.board.setOccupant(('B', rows[0]), Pieces.Knight(color, 'B', rows[0]))
            self.board.setOccupant(('C', rows[0]), Pieces.Bishop(color, 'C', rows[0]))
            self.board.setOccupant(('D', rows[0]), Pieces.King(color, 'D', rows[0]))
            self.board.setOccupant(('E', rows[0]), Pieces.Queen(color, 'E', rows[0]))
            self.board.setOccupant(('F', rows[0]), Pieces.Bishop(color, 'F', rows[0]))
            self.board.setOccupant(('G', rows[0]), Pieces.Knight(color, 'G', rows[0]))
            self.board.setOccupant(('H', rows[0]), Pieces.Rook(color, 'H', rows[0]))
            for x in self.board.X_axis:
                self.board.setOccupant((x, rows[1]), Pieces.Pawn(color, x, rows[1]))

    def change_turn(self):
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'

    def select(self, screen_pos):
        selected_square = self.board.getSquare(screen_pos)
        if selected_square is not None:
            if self.player_moving:
                # DROP
                # if the player is moving and press mouse then move the selected piece to new squared
                old_square = self.board.findSelectedSqure()  # find the selected square
                old_square.being_clicked = False
                # find possible move
                possible_moves = self.board.getPossibleMove(old_square.pos, self.turn)
                # check selected square is possible
                if selected_square in possible_moves:
                    # check if the player select the old square
                    if old_square != selected_square:
                        # change squares
                        self.checkCheck(selected_square)
                        selected_square.occupant, old_square.occupant = old_square.occupant, None
                        selected_square.occupant.setPosition(selected_square.pos)
                        # change the first move of the pawn
                        if type(selected_square.occupant) is Pieces.Pawn:
                            selected_square.occupant.first_move = False
                        self.change_turn()
                self.player_moving = False
            else:
                # CLICK
                # if the player is not moving and press the mouse then mark that the square is being move
                if selected_square.occupant is not None:
                    # only move pieces that has same colors
                    if selected_square.occupant.color == self.turn:
                        selected_square.being_clicked = True
                        self.player_moving = True

    def checkCheck(self, square):
        if type(square.occupant) is Pieces.King:
            self.status = False
            self.winner = self.turn

    # if it's the bot turn and after the bot has choose the

if __name__ == '__main__':
    game = Game()
    game.setUp()
    print(game.board)
