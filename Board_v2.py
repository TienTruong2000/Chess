import Pieces_v2 as Pieces
import pygame
import itertools
from copy import deepcopy


class Square:
    def __init__(self, pos: tuple, occupant: Pieces = None, left_up_corner: tuple = (0, 0), size=60):
        self.pos = pos
        self.occupant = occupant
        self.left_up_corner = left_up_corner
        self.size = size

    def __str__(self):
        x = chr(self.pos[0] + 64)
        y = self.pos[1]
        return f"{x}{y}"


class Board:
    default_size = 600
    default_root = 38
    default_distance = 66.5
    default_square_size = 60

    def __init__(self, board_size=default_size):
        self.size = board_size
        self.root = self.getRoot(board_size)
        self.distance = self.getDistance(board_size)
        self.square_size = self.getSquareSize(board_size)
        self.squares = []
        for x, y in itertools.product([x for x in range(1, 9)], [x for x in range(1, 9)]):
            # find the left up corner screen coordinates
            screen_x = (x - 1) * self.distance + self.root
            screen_y = (y - 1) * self.distance + self.root
            self.squares.append(Square((x, y), None, (screen_x, screen_y), self.square_size))

        self.img = pygame.image.load("board.png")
        self.img = pygame.transform.scale(self.img, (self.size, self.size))

    def getRoot(self, size):
        return int(self.default_root * (size / self.default_size))

    def getDistance(self, size):
        return int(self.default_distance * (size / self.default_size))

    def getSquareSize(self, size):
        return int(self.default_square_size * (size / self.default_size))

    def findSquare(self, pos: tuple):
        # based on chess coordinates
        for square in self.squares:
            if square.pos == pos:
                return square
        return None

    def setOccupant(self, pos: tuple, occupant: Pieces):
        square = self.findSquare(pos)
        square.occupant = occupant

    def __str__(self):
        result = ''
        for x in self.squares:
            result += str(x) + '\n'
        return result

    def getChessPos(self, screen_pos: tuple):
        # get the square chess coordinates
        # based on screen coordinates
        x, y = screen_pos
        for square in self.squares:
            square_x, square_y = square.left_up_corner
            if square_x <= x <= square_x + square.size and square_y <= y <= square_y + square.size:
                return square.pos
        return None

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k == 'img':
                continue
            setattr(result, k, deepcopy(v, memo))
        return result


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_mode((0, 0))
    board = Board(600)
    a = deepcopy(board)
