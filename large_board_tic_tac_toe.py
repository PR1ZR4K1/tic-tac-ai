"""
PLEASE READ THE COMMENTS BELOW AND THE HOMEWORK DESCRIPTION VERY CAREFULLY BEFORE YOU START CODING

 The file where you will need to create the GUI which should include (i) drawing the grid, (ii) call your Minimax/Negamax functions
 at each step of the game, (iii) allowing the controls on the GUI to be managed (e.g., setting board size, using 
                                                                                 Minimax or Negamax, and other options)
 In the example below, grid creation is supported using pygame which you can use. You are free to use any other 
 library to create better looking GUI with more control. In the __init__ function, GRID_SIZE (Line number 36) is the variable that
 sets the size of the grid. Once you have the Minimax code written in multiAgents.py file, it is recommended to test
 your algorithm (with alpha-beta pruning) on a 3x3 GRID_SIZE to see if the computer always tries for a draw and does 
 not let you win the game. Here is a video tutorial for using pygame to create grids http://youtu.be/mdTeqiWyFnc
 
 
 PLEASE CAREFULLY SEE THE PORTIONS OF THE CODE/FUNCTIONS WHERE IT INDICATES "YOUR CODE BELOW" TO COMPLETE THE SECTIONS
 
"""
import pygame
import numpy as np
# from GameStatus_5120 import GameStatus
from Text import Text
# from multiAgents import minimax, negamax
import sys
import random

mode = "player_vs_ai"  # default mode for playing the game (player vs AI)


class RandomBoardTicTacToe:
    def __init__(self, size=(600, 600)):

        self.size = self.width, self.height = size
        # Define some colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        # Grid Variables
        self.GRID_SQUARES = 50
        self.GRID_LINES = self.GRID_SQUARES - 1
        # border radius for line
        self.GRID_LINE_BR = 2
        self.GRID_LINE_WIDTH = 4
        # total line width
        self.GRID_LINE_TW = (self.GRID_LINE_BR + self.GRID_LINE_WIDTH)
        self.GRID_OFFSET = 45

        # size of each square
        """
        Explained:
            get the screen width (outer box) find the size of the inner box
            Do this by removing the offset from both sides of inner box and the amount of space
            the grid lines will take up in total, i use grid lines - 1 because we don't need to include the width of the
            first  and last lines for our total.
            Finally divide this by the amount of squares that we need and round appropriately to get as close as possible
            to a completely even distribution. This is necessary because pygame does not do decimal values for coordinates
        """
        self.GRID_SQUARE_SIZE = round(self.width - (2 * self.GRID_OFFSET + (
            (self.GRID_LINES-1) * self.GRID_LINE_TW))) / (self.GRID_SQUARES)

        self.CIRCLE_COLOR = (140, 146, 172)
        self.CROSS_COLOR = (140, 146, 172)

        # This sets the margin between each cell
        self.MARGIN = 5
        self.FONT_SIZE = 50
        self.OPTIONS_SIZE = 25
        self.running = True

        pygame.init()

        self.menu_options = [
            Text("Play", x_pos=self.width/2-20, y_pos=150,
                 font_size=self.FONT_SIZE, font_color=self.WHITE),
            Text("Options", x_pos=self.width/2-20, y_pos=300,
                 font_size=self.FONT_SIZE, font_color=self.WHITE),
            Text("Exit", x_pos=self.width/2-20, y_pos=450,
                 font_size=self.FONT_SIZE, font_color=self.WHITE)
        ]
        self.menu_options[0].setSelected(True)

        # options menu text
        self.options_menu_items = [
            Text("Game Mode: ", x_pos=self.width/2, y_pos=50,
                 font_size=self.OPTIONS_SIZE, font_color=self.WHITE, font_file='basic.ttf'),
            Text("Player Symbol: ", x_pos=self.width/2, y_pos=175,
                 font_size=self.OPTIONS_SIZE, font_color=self.WHITE, font_file='basic.ttf'),
            Text("Board Size: ", x_pos=self.width/2, y_pos=300,
                 font_size=self.OPTIONS_SIZE, font_color=self.WHITE, font_file='basic.ttf'),
            Text("Apply Changes", x_pos=self.width/2, y_pos=500,
                 font_size=self.OPTIONS_SIZE, font_color=self.WHITE, font_file='basic.ttf'),
        ]
        self.options_menu_items[3].setSelected(True)

        self.game_mode_options = [
            Text("Human vs Human", x_pos=self.width/2, y_pos=75,
                 font_size=self.OPTIONS_SIZE, font_color=self.WHITE, font_file='basic.ttf'),
            Text("Human vs Computer", x_pos=self.width/2, y_pos=100,
                 font_size=self.OPTIONS_SIZE, font_color=self.WHITE, font_file='basic.ttf'),
        ]
        self.selected_game_mode = 0

        self.player_symbol_options = [
            Text("Nought (0)", x_pos=self.width/2, y_pos=200,
                 font_size=self.OPTIONS_SIZE, font_color=self.WHITE, font_file='basic.ttf'),
            Text("Cross (X)", x_pos=self.width/2, y_pos=225,
                 font_size=self.OPTIONS_SIZE, font_color=self.WHITE, font_file='basic.ttf'),
        ]
        self.selected_player_symbol = 0

        self.screen = pygame.display.set_mode(self.size)

        # Initialize pygame
        self.game_reset()

    def quit(self):
        self.running = False
        pygame.quit()

    # change the currently selected option and return new selection value
    # direction is -1 for up and +1 for down
    def change_selection(self, current_selection, direction: int):
        self.menu_options[current_selection].setSelected(
            False)
        self.menu_options[current_selection].setBackgroundColor(
            self.BLACK)
        new_selection = (
            current_selection + direction) % len(self.menu_options)
        self.menu_options[new_selection].setSelected(
            True)

        return new_selection

    def main_menu(self):

        # Create a 2 dimensional array using the column and row variables

        pygame.display.set_caption("Tic Tac Toe Menu")
        self.screen.fill(self.BLACK)

        # Draw the menu

        for obj in self.menu_options:
            if (obj.isSelected):
                pygame.draw.rect(self.screen, self.RED,
                                 obj.rectangle_rect, border_radius=2)
                obj.setBackgroundColor(self.RED)

            self.screen.blit(
                obj.name, obj.rect)

        pygame.display.update()

    def options_menu(self):
        # Create the options menu
        done = False
        pygame.init()

        while self.running and not done:
            pygame.display.set_caption("Tic Tac Toe Options")
            self.screen.fill(self.BLACK)

            for obj in self.options_menu_items:
                if (obj.isSelected):
                    pygame.draw.rect(self.screen, self.RED,
                                     obj.rectangle_rect, border_radius=1)
                    obj.setBackgroundColor(self.RED)
                self.screen.blit(obj.name, obj.rect)

            # for ob

            for button, option in enumerate(self.game_mode_options):
                mode_circle_center = (self.width/2-120, option.y_pos)

                pygame.draw.circle(self.screen, self.WHITE,
                                   mode_circle_center, 6, 2)

                if button == self.selected_game_mode:
                    pygame.draw.circle(
                        self.screen, self.WHITE, mode_circle_center, 6)

            for button, option in enumerate(self.player_symbol_options):
                symbol_circle_center = (self.width/2-120, option.y_pos)

                pygame.draw.circle(self.screen, self.WHITE,
                                   symbol_circle_center, 6, 2)

                if button == self.selected_player_symbol:
                    pygame.draw.circle(
                        self.screen, self.WHITE, symbol_circle_center, 6)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()

                # exit button event
                if event.type == pygame.QUIT:
                    self.quit()

    def change_turn(self):

        if (self.game_state.turn_O):
            pygame.display.set_caption("Tic Tac Toe - O's turn")
        else:
            pygame.display.set_caption("Tic Tac Toe - X's turn")

    def draw_circle(self, x, y):
        """
        YOUR CODE HERE TO DRAW THE CIRCLE FOR THE NOUGHTS PLAYER
        """

    def draw_cross(self, x, y):
        """
        YOUR CODE HERE TO DRAW THE CROSS FOR THE CROSS PLAYER AT THE CELL THAT IS SELECTED VIA THE gui
        """

    def is_game_over(self):
        """
        YOUR CODE HERE TO SEE IF THE GAME HAS TERMINATED AFTER MAKING A MOVE. YOU SHOULD USE THE IS_TERMINAL()
        FUNCTION FROM GAMESTATUS_5120.PY FILE (YOU WILL FIRST NEED TO COMPLETE IS_TERMINAL() FUNCTION)

        YOUR RETURN VALUE SHOULD BE TRUE OR FALSE TO BE USED IN OTHER PARTS OF THE GAME
        """

    def move(self, move):
        self.game_state = self.game_state.get_new_state(move)

    def play_ai(self):
        """
        YOUR CODE HERE TO CALL MINIMAX OR NEGAMAX DEPENDING ON WHICH ALGORITHM SELECTED FROM THE GUI
        ONCE THE ALGORITHM RETURNS THE BEST MOVE TO BE SELECTED, YOU SHOULD DRAW THE NOUGHT (OR CIRCLE DEPENDING
        ON WHICH SYMBOL YOU SELECTED FOR THE AI PLAYER)

        THE RETURN VALUES FROM YOUR MINIMAX/NEGAMAX ALGORITHM SHOULD BE THE SCORE, MOVE WHERE SCORE IS AN INTEGER
        NUMBER AND MOVE IS AN X,Y LOCATION RETURNED BY THE AGENT
        """

        self.change_turn()
        pygame.display.update()
        terminal = self.game_state.is_terminal()
        """ USE self.game_state.get_scores(terminal) HERE TO COMPUTE AND DISPLAY THE FINAL SCORES """

    def game_reset(self):
        self.main_menu()
        """
        YOUR CODE HERE TO RESET THE BOARD TO VALUE 0 FOR ALL CELLS AND CREATE A NEW GAME STATE WITH NEWLY INITIALIZED
        BOARD STATE
        """

        pygame.display.update()

    def draw_grid(self):

        for i in range(1, self.GRID_SQUARES):

            # the y intercept for the horizontal line will always retain the same offset, but
            # needs to know the size of each preceding square that has passed.
            # we also need to include the total widths of the intercepting lines that had preceded, but
            # we do not include the current line hence i - 1
            h_y = self.GRID_OFFSET + \
                (self.GRID_SQUARE_SIZE * i) + (self.GRID_LINE_TW * (i - 1))

            h_start_pos = (self.GRID_OFFSET, h_y)
            h_end_pos = ((self.width - self.GRID_OFFSET), h_y)

            # same as h_y, but I flip the position of the coordinates
            v_x = self.GRID_OFFSET + \
                (self.GRID_SQUARE_SIZE * i) + (self.GRID_LINE_TW * (i - 1))

            v_start_pos = (v_x, self.GRID_OFFSET)
            v_end_pos = (v_x, (self.height - self.GRID_OFFSET))

            # draw the line
            horizontal_rect = pygame.draw.line(self.screen, self.WHITE, h_start_pos, h_end_pos, self.GRID_LINE_WIDTH).inflate(
                self.GRID_LINE_BR, self.GRID_LINE_BR)

            # draw surrounding box to make a border radius to make our lines rounded
            pygame.draw.rect(self.screen, self.WHITE,
                             horizontal_rect, border_radius=self.GRID_LINE_BR)

            # draw the line
            vertical_rect = pygame.draw.line(self.screen, self.WHITE, v_start_pos, v_end_pos, self.GRID_LINE_WIDTH).inflate(
                self.GRID_LINE_BR, self.GRID_LINE_BR)

            # draw surrounding box to make a border radius to make our lines rounded
            pygame.draw.rect(self.screen, self.WHITE,
                             vertical_rect, border_radius=self.GRID_LINE_BR)

    def play_game(self, mode="player_vs_ai"):
        done = False

        clock = pygame.time.Clock()

        while self.running and not done:
            pygame.display.set_caption("Tic Tac Toe!")
            self.screen.fill(self.BLACK)
            self.draw_grid()

            pygame.display.update()

            for event in pygame.event.get():  # User did something
                """
                YOUR CODE HERE TO CHECK IF THE USER CLICKED ON A GRID ITEM. EXIT THE GAME IF THE USER CLICKED EXIT
                """

                """
                YOUR CODE HERE TO HANDLE THE SITUATION IF THE GAME IS OVER. IF THE GAME IS OVER THEN DISPLAY THE SCORE,
                THE WINNER, AND POSSIBLY WAIT FOR THE USER TO CLEAR THE BOARD AND START THE GAME AGAIN (OR CLICK EXIT)
                """

                """
                YOUR CODE HERE TO NOW CHECK WHAT TO DO IF THE GAME IS NOT OVER AND THE USER SELECTED A NON EMPTY CELL
                IF CLICKED A NON EMPTY CELL, THEN GET THE X,Y POSITION, SET ITS VALUE TO 1 (SELECTED BY HUMAN PLAYER),
                DRAW CROSS (OR NOUGHT DEPENDING ON WHICH SYMBOL YOU CHOSE FOR YOURSELF FROM THE gui) AND CALL YOUR 
                PLAY_AI FUNCTION TO LET THE AGENT PLAY AGAINST YOU
                """

                # if event.type == pygame.MOUSEBUTTONUP:
                # Get the position

                # Change the x/y screen coordinates to grid coordinates

                # Check if the game is human vs human or human vs AI player from the GUI.
                # If it is human vs human then your opponent should have the value of the selected cell set to -1
                # Then draw the symbol for your opponent in the selected cell
                # Within this code portion, continue checking if the game has ended by using is_terminal function

                # key events
                match event.type:

                    case pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        print(pos)

                    case pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.quit()

                    # exit button event
                    case pygame.QUIT:
                        self.quit()


"""
YOUR CODE HERE TO SELECT THE OPTIONS VIA THE GUI CALLED FROM THE ABOVE LINE
AFTER THE ABOVE LINE, THE USER SHOULD SELECT THE OPTIONS AND START THE GAME. 
YOUR FUNCTION PLAY_GAME SHOULD THEN BE CALLED WITH THE RIGHT OPTIONS AS SOON
AS THE USER STARTS THE GAME
"""


def handle_k_return(current_selection, tictactoegame):
    match current_selection:
        case 0:
            print('play the game!')
            tictactoegame.play_game()
        case 1:
            print('options!')
            tictactoegame.options_menu()
        case 2:
            print('exiting!')
            tictactoegame.quit()


def handle_mouse_up(pos, tictactoegame):
    for obj in tictactoegame.menu_options:
        # if one of them was clicked
        if not obj.rect.collidepoint(pos):
            continue

        match obj.text.lower():
            case 'play':
                print('play the game!')
                # obj.setBackgroundColor(tictactoegame.RED)
                # obj.setSelected(True)
                tictactoegame.play_game()
            case 'options':
                print('options!')
                tictactoegame.options_menu()
            case 'exit':
                print('exiting!')
                tictactoegame.quit()


def handle_key_down(event, current_selection, tictactoegame):
    match event.key:
        case pygame.K_ESCAPE:
            tictactoegame.quit()
        case pygame.K_UP:
            current_selection = tictactoegame.change_selection(
                current_selection=current_selection, direction=-1)
        case pygame.K_DOWN:
            current_selection = tictactoegame.change_selection(
                current_selection=current_selection, direction=1)
        case pygame.K_RETURN:
            handle_k_return(current_selection, tictactoegame)

    return current_selection


def main():
    tictactoegame = RandomBoardTicTacToe()
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
