import Chess.Board as Board
import Chess.Pieces as Pieces
import Chess.Game as Game
import pygame


def endGame():
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(f'{game.winner} win!!!!!', True, (255, 255, 255), (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (600 // 2, 600 // 2)
    screen.blit(text, textRect)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption('Chess')
    game = Game.Game()
    game.setUp()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if the game is done: do not allow clicking
                if game.status:
                    screen_pos = pygame.mouse.get_pos()
                    game.select(screen_pos)
        screen.fill((0, 0, 0))
        game.board.draw(screen)
        game.board.drawSquare(screen, pygame.mouse.get_pos())
        if not game.status:
            endGame()
        pygame.display.update()
