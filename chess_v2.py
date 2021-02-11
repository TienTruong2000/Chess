import pygame
import Game_v2 as Game
import Board_v2 as Board
import Player_v2 as Player
import time


def endGame():
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(f'{game.winner.color} win!!!!!', True, (255, 255, 255), (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (600 // 2, 600 // 2)
    screen.blit(text, textRect)


def drawBoard(board: Board.Board, board_pos: tuple):
    screen.blit(board.img, board_pos)
    for square in board.squares:
        if square.occupant is not None:
            x, y = square.left_up_corner
            screen.blit(square.occupant.img, (x, y))


if __name__ == '__main__':
    pygame.init()

    height = 600
    width = 600
    board_size = 600

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Chess')

    game = Game.Game(board_size, player={'black': 'bot', 'white': 'bot'})
    game.setUp()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.status:
                    screen_pos = pygame.mouse.get_pos()
                    game.clickDetection(screen_pos)
        screen.fill((0, 0, 0))
        drawBoard(game.board, (0, 0))
        if game.status:
            # draw moving pieces
            if game.moving_piece is not None:
                screen.blit(game.moving_piece.img, pygame.mouse.get_pos())
            # check if its bot turn
            piece, pos = game.botMove()
            if piece is not None and pos is not None:
                drawBoard(game.board, (0, 0))
                screen.blit(piece.img, pos)
        else:
            endGame()
        pygame.display.update()
