# imports
import pygame
from large_board_tic_tac_toe import RandomBoardTicTacToe, handle_key_down, handle_mouse_up


def main():

    # adjust depth for AI here!
    ai_depth = 5
    tictactoegame = RandomBoardTicTacToe(ai_depth=ai_depth)
    pygame.init()

    current_selection = 0

    while tictactoegame.running:
        # draw our first screen
        tictactoegame.main_menu()

        # handle player events
        for event in pygame.event.get():
            match event.type:
                case pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    handle_mouse_up(pos, tictactoegame)
                case pygame.KEYDOWN:
                    current_selection = handle_key_down(
                        event, current_selection, tictactoegame)
                case pygame.QUIT:
                    tictactoegame.quit()


if __name__ == '__main__':
    main()
