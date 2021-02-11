import pygame
from copy import deepcopy

class Direction:
    def __init__(self, name):
        self.name = name


class Piece:
    def __init__(self, color: str, pos: tuple, size):
        self.color = color
        self.pos = pos
        self.name = self.getName()
        self.size = size
        self.img = None

    def getName(self):
        return str(self.__class__)[24:][:-2]

    def __str__(self):
        return f'{self.color} {self.name}'

    def getMove(self, direction=None, step=None, L_shape=False):
        if direction is not None and step is not None:
            f = getattr(self, direction)  # get the direction method
            x_range, y_range = f(step)
        else:
            x_range, y_range = [], []
        moves = []
        if not L_shape:
            for x, y in zip(x_range, y_range):
                if x in range(1, 9) and y in range(1, 9):
                    moves.append((x, y))
        else:
            # LShape return a very different list of movements
            for x, y in self.LShape():
                if x in range(1, 9) and y in range(1, 9):
                    moves.append((x, y))
        return moves

    # from the 'position' move 'step' moves in that 'direction'
    # return x_range, y_range: x,y coordinate with the move
    def North(self, step):
        x, y = self.pos
        if self.color == 'black':
            y_range = range(y - 1, y - step - 1, -1)
        else:
            y_range = range(y + 1, y + step + 1)
        x_range = [x] * 8
        return x_range, y_range

    def NorthEast(self, step):
        x, y = self.pos
        if self.color == 'black':
            y_range = range(y - 1, y - step - 1, -1)
            x_range = range(x + 1, x + step + 1)
        else:
            y_range = range(y + 1, y + step + 1)
            x_range = range(x - 1, x - step - 1, -1)
        return x_range, y_range

    def East(self, step):
        x, y = self.pos
        if self.color == 'black':
            x_range = range(x + 1, x + step + 1)
        else:
            x_range = range(x - 1, x - step - 1, -1)
        y_range = [y] * len(x_range)
        return x_range, y_range

    def SouthEast(self, step):
        x, y = self.pos
        if self.color == 'black':
            y_range = range(y + 1, y + step + 1)
            x_range = range(x + 1, x + step + 1)
        else:
            y_range = range(y - 1, y - step - 1, -1)
            x_range = range(x - 1, x - step - 1, -1)
        return x_range, y_range

    def South(self, step):
        x, y = self.pos
        if self.color == 'black':
            y_range = range(y + 1, y + step + 1)
        else:
            y_range = range(y - 1, y - step - 1, -1)
        x_range = [x] * len(y_range)
        return x_range, y_range

    def SouthWest(self, step):
        x, y = self.pos
        if self.color == 'black':
            y_range = range(y + 1, y + step + 1)
            x_range = range(x - 1, x - step - 1, -1)
        else:
            y_range = range(y - 1, y - step - 1, -1)
            x_range = range(x + 1, x + step + 1)
        return x_range, y_range

    def West(self, step):
        x, y = self.pos
        if self.color == 'black':
            x_range = range(x - 1, x - step - 1, -1)
        else:
            x_range = range(x + 1, x + step + 1)
        y_range = [y] * len(x_range)
        return x_range, y_range

    def NorthWest(self, step):
        x, y = self.pos
        if self.color == 'black':
            y_range = range(y - 1, y - step - 1, -1)
            x_range = range(x - 1, x - step - 1, -1)
        else:
            y_range = range(y + 1, y + step + 1)
            x_range = range(x + 1, x + step + 1)
        return x_range, y_range

    def LShape(self):
        # return all the possible position of L shape
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
        x, y = self.pos
        for index, value in enumerate(moves):
            next_x, next_y = value
            moves[index] = (x + next_x, y + next_y)
        return moves

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k == 'img':
                continue
            setattr(result, k, deepcopy(v, memo))
        return result



class King(Piece):
    def __init__(self, color: str, pos: tuple, size):
        Piece.__init__(self, color, pos, size)
        self.img = pygame.image.load('Pieces/' + color + '_king' + '.png').convert()
        self.img = pygame.transform.scale(self.img, (self.size, self.size))
        self.img.set_colorkey((255, 255, 255))
        self.value = 10000
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
        self.check = {
            'North': 7,
            'NorthEast': 7,
            'East': 7,
            'SouthEast': 7,
            'South': 7,
            'SouthWest': 7,
            'West': 7,
            'NorthWest': 7,
        }



class Queen(Piece):
    def __init__(self, color: str, pos: tuple, size):
        Piece.__init__(self, color, pos, size)
        self.img = pygame.image.load('Pieces/' + color + '_queen' + '.png').convert()
        self.img = pygame.transform.scale(self.img, (self.size, self.size))
        # remove white background
        self.img.set_colorkey((255, 255, 255))
        self.value = 9
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
    def __init__(self, color: str, pos: tuple, size):
        Piece.__init__(self, color, pos, size)
        self.img = pygame.image.load('Pieces/' + color + '_rook' + '.png').convert()
        self.img = pygame.transform.scale(self.img, (self.size, self.size))
        # remove white background
        self.img.set_colorkey((255, 255, 255))
        self.value = 5
        self.move = {
            'North': 7,
            'East': 7,
            'South': 7,
            'West': 7,
        }


class Knight(Piece):
    def __init__(self, color: str, pos: tuple, size):
        Piece.__init__(self, color, pos, size)
        self.img = pygame.image.load('Pieces/' + color + '_knight' + '.png').convert()
        self.img = pygame.transform.scale(self.img, (self.size, self.size))
        # remove white background
        self.img.set_colorkey((255, 255, 255))
        self.value = 3
        self.move = {
            'LShape': 0
        }


class Bishop(Piece):
    def __init__(self, color: str, pos: tuple, size):
        Piece.__init__(self, color, pos, size)
        self.img = pygame.image.load('Pieces/' + color + '_bishop' + '.png').convert()
        self.img = pygame.transform.scale(self.img, (self.size, self.size))
        # remove white background
        self.img.set_colorkey((255, 255, 255))
        self.value = 3
        self.move = {
            'NorthEast': 7,
            'SouthEast': 7,
            'SouthWest': 7,
            'NorthWest': 7,
        }


class Pawn(Piece):
    def __init__(self, color: str, pos: tuple, size):
        Piece.__init__(self, color, pos, size)
        self.img = pygame.image.load('Pieces/' + color + '_pawn' + '.png').convert()
        self.img = pygame.transform.scale(self.img, (self.size, self.size))
        # remove white background
        self.img.set_colorkey((255, 255, 255))
        self.first_move = True
        self.value = 1

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
        # pawn can eat diagonally if there is an opponent piece
        return {
            'NorthEast': 1,
            'NorthWest': 1,
        }


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((0, 0))
    knight = Knight('white', (1, 1), 60)
    king = Knight('white', (1, 1), 60)
    import copy
    king = deepcopy(knight)
