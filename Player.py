class Player:
    def __init__(self, color, type, pieces=[]):
        self.color = color
        self.pieces = pieces
        self.type = type
        self.score = 0
        self.history = []

    def eatPieces(self):
        # TODO implement the method
        pass


class Bot:
    pass
    # TODO implement the bot
    # if it's the bot turn then the bot will search through its pieces on the board
    #                                        choose which piece to move (access the board information, using game as
    #                                        bridge)
    # choose piece: 1.randomly choose the pieces and randomly choose the move
    #               2.use min-max algorithm to choose the move
    # return the selected square and selected move

