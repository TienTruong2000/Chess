import pygame
import itertools


class Piece:
    Y_axis = [1, 2, 3, 4, 5, 6, 7, 8]
    X_axis = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    def __init__(self, name, color, x, y):
        self.name = name
        self.color = color
        self.x = x
        self.y = y

    def getMove(self, x_range: list = [], y_range: list = [], L_shape=False):
        moves = []
        if not L_shape:
            for x, y in zip(x_range, y_range):
                if chr(x) in self.X_axis and y in self.Y_axis:
                    moves.append((chr(x), y))
        else:
            for x, y in self.LShape():
                if chr(x) in self.X_axis and y in self.Y_axis:
                    moves.append((chr(x), y))
        return moves

    def North(self, step):

        if self.color == 'black':
            y_range = range(self.y - 1, self.y - step - 1, -1)
        else:
            y_range = range(self.y + 1, self.y + step + 1)
        x_range = [ord(self.x)] * len(y_range)
        return x_range, y_range

    def NorthEast(self, step):
        if self.color == 'black':
            y_range = range(self.y - 1, self.y - step - 1, -1)
            x_range = range(ord(self.x) + 1, ord(self.x) + step + 1)
        else:
            y_range = range(self.y + 1, self.y + step + 1)
            x_range = range(ord(self.x) - 1, ord(self.x) - step - 1, -1)
        return x_range, y_range

    def East(self, step):
        if self.color == 'black':
            x_range = range(ord(self.x) + 1, ord(self.x) + step + 1)
        else:
            x_range = range(ord(self.x) - 1, ord(self.x) - step - 1, -1)
        y_range = [self.y] * len(x_range)
        return x_range, y_range

    def SouthEast(self, step):
        if self.color == 'black':
            y_range = range(self.y + 1, self.y + step + 1)
            x_range = range(ord(self.x) + 1, ord(self.x) + step + 1)
        else:
            y_range = range(self.y - 1, self.y - step - 1, -1)
            x_range = range(ord(self.x) - 1, ord(self.x) - step - 1, -1)
        return x_range, y_range

    def South(self, step):
        if self.color == 'black':
            y_range = range(self.y + 1, self.y + step + 1)
        else:
            y_range = range(self.y - 1, self.y - step - 1, -1)
        x_range = [ord(self.x)] * len(y_range)
        return x_range, y_range

    def SouthWest(self, step):
        if self.color == 'black':
            y_range = range(self.y + 1, self.y + step + 1)
            x_range = range(ord(self.x) - 1, ord(self.x) - step - 1, -1)
        else:
            y_range = range(self.y - 1, self.y - step - 1, -1)
            x_range = range(ord(self.x) + 1, ord(self.x) + step + 1)
        return x_range, y_range

    def West(self, step):
        if self.color == 'black':
            x_range = range(ord(self.x) - 1, ord(self.x) - step - 1, -1)
        else:
            x_range = range(ord(self.x) + 1, ord(self.x) + step + 1)
        y_range = [self.y] * len(x_range)
        return x_range, y_range

    def NorthWest(self, step):
        if self.color == 'black':
            y_range = range(self.y - 1, self.y - step - 1, -1)
            x_range = range(ord(self.x) - 1, ord(self.x) - step - 1, -1)
        else:
            y_range = range(self.y + 1, self.y + step + 1)
            x_range = range(ord(self.x) + 1, ord(self.x) + step + 1)
        return x_range, y_range

    def LShape(self):
        moves = [
            (1, 2),
            (2, 1),
            (2, -1),
            (1, -2),
            (-1, -2),
            (-2, -1),
            (-2, 1),
            (-1, 2)
        ]
        for index, value in enumerate(moves):
            x, y = value
            moves[index] = (ord(self.x) + x, self.y + y)
        return moves

    def setPosition(self, pos):
        self.x, self.y = pos

    def __str__(self):
        return f'{self.color} {self.name}: {self.x},{self.y}'


class King(Piece):
    def __init__(self, color, x, y):
        Piece.__init__(self, 'king', color, x, y)
        self.img = pygame.image.load('Pieces/' + color + '_king' + '.png').convert()
        # remove white background
        self.img.set_colorkey((255, 255, 255))
        self.move = {
            'North': 1,
            'NorthEast': 1,
            'East': 1,
            'SouthEast': 1,
            'South': 1,
            'SouthWest': 1,
            'West': 1,
            'NorthWest': 1,
        }


class Queen(Piece):
    def __init__(self, color, x, y):
        Piece.__init__(self, 'queen', color, x, y)
        self.img = pygame.image.load('Pieces/' + color + '_queen' + '.png').convert()
        # remove white background
        self.img.set_colorkey((255, 255, 255))

        self.move = {
            'North': 7,
            'NorthEast': 7,
            'East': 7,
            'SouthEast': 7,
            'South': 7,
            'SouthWest': 7,
            'West': 7,
            'NorthWest': 7,
        }


class Rook(Piece):
    def __init__(self, color, x, y):
        Piece.__init__(self, 'rook', color, x, y)
        self.img = pygame.image.load('Pieces/' + color + '_rook' + '.png').convert()
        # remove white background
        self.img.set_colorkey((255, 255, 255))

        self.move = {
            'North': 7,
            'East': 7,
            'South': 7,
            'West': 7,
        }


class Knight(Piece):
    def __init__(self, color, x, y):
        Piece.__init__(self, 'knight', color, x, y)
        self.img = pygame.image.load('Pieces/' + color + '_knight' + '.png').convert()
        # remove white background
        self.img.set_colorkey((255, 255, 255))

        self.move = {
            'LShape': 0
        }


class Bishop(Piece):
    def __init__(self, color, x, y):
        Piece.__init__(self, 'bishop', color, x, y)
        self.img = pygame.image.load('Pieces/' + color + '_bishop' + '.png').convert()
        # remove white background
        self.img.set_colorkey((255, 255, 255))

        self.move = {
            'NorthEast': 7,
            'SouthEast': 7,
            'SouthWest': 7,
            'NorthWest': 7,
        }


class Pawn(Piece):
    def __init__(self, color, x, y):
        Piece.__init__(self, 'pawn', color, x, y)
        self.img = pygame.image.load('Pieces/' + color + '_pawn' + '.png').convert()
        # remove white background
        self.img.set_colorkey((255, 255, 255))
        self.first_move = True

    @property
    def move(self):
        if self.first_move:
            return {
                'North': 2,
            }
        else:
            return {
                'North': 1,
            }

    @property
    def eat(self):
        return {
            'NorthEast': 1,
            'NorthWest': 1,
        }


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((0, 0))
    knight = Queen('white', 'E', 1)
    for function, step in knight.move.items():
        if function == 'LShape':
            for x in knight.getMove(L_shape=True):
                print(x)
        else:
            f = getattr(knight, function)
            range_x, range_y = f(step)
            print(f.__name__)
            for x in knight.getMove(range_x, range_y):
                print(x)