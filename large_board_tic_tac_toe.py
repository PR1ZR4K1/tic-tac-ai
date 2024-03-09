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
from multiAgents import minimax, negamax
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

        # Grid Size
        self.GRID_SIZE = 4
        self.OFFSET = 5

        self.CIRCLE_COLOR = (140, 146, 172)
        self.CROSS_COLOR = (140, 146, 172)

        # This sets the WIDTH and HEIGHT of each grid location
        self.WIDTH = self.size[0]/self.GRID_SIZE - self.OFFSET  # 150
        self.HEIGHT = self.size[1]/self.GRID_SIZE - self.OFFSET  # 150

        # This sets the margin between each cell
        self.MARGIN = 5
        self.FONT_SIZE = 50
        self.running = True

        pygame.init()

        self.menu_options = [Text(label, x_pos=self.width/2-20, y_pos=y_pos,
                                  font_size=self.FONT_SIZE, font_color=self.WHITE)
                             for label, y_pos in [
            ('Play', 150),
            ('Options', 300),
            ('Exit', 450)
        ]]

        self.menu_options[0].setSelected(True)

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
        pygame.init()

        while self.running:
            pygame.display.set_caption("Tic Tac Toe Options")
            self.screen.fill(self.BLACK)
            pygame.display.update()

            for event in pygame.event.get():

                # key events
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

    def play_game(self, mode="player_vs_ai"):
        done = False

        clock = pygame.time.Clock()

        while not done:
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

            # Update the screen with what was drawn.
            pygame.display.update()

        pygame.quit()


"""
YOUR CODE HERE TO SELECT THE OPTIONS VIA THE GUI CALLED FROM THE ABOVE LINE
AFTER THE ABOVE LINE, THE USER SHOULD SELECT THE OPTIONS AND START THE GAME. 
YOUR FUNCTION PLAY_GAME SHOULD THEN BE CALLED WITH THE RIGHT OPTIONS AS SOON
AS THE USER STARTS THE GAME
"""


def main():
    tictactoegame = RandomBoardTicTacToe()
    pygame.init()
    current_selection = 0

    while tictactoegame.running:

        # draw our first screen
        tictactoegame.main_menu()

        # handle player events
        for event in pygame.event.get():

            # mouse events
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                # iterate through available objects
                for obj in tictactoegame.menu_options:

                    # if one of them was clicked
                    if obj.rect.collidepoint(pos):
                        # determine which one

                        if obj.text.lower() == 'play':
                            print('play the game!')

                            # check if the text item has not already been selected
                            if not obj.isSelected:
                                # select it
                                obj.setBackgroundColor(tictactoegame.RED)
                                obj.setSelected(True)

                        elif obj.text.lower() == 'options':
                            print('options!')
                            tictactoegame.options_menu()
                        elif obj.text.lower() == 'exit':
                            print('exiting!')
                            tictactoegame.quit()

            # key events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    tictactoegame.quit()
                elif event.key == pygame.K_UP:
                    current_selection = tictactoegame.change_selection(
                        current_selection=current_selection, direction=-1)
                elif event.key == pygame.K_DOWN:
                    current_selection = tictactoegame.change_selection(
                        current_selection=current_selection, direction=1)
                elif event.key == pygame.K_RETURN:
                    # play
                    if current_selection == 0:
                        print('play the game!')
                    elif current_selection == 1:
                        print('options!')
                        tictactoegame.options_menu()
                    elif current_selection == 2:
                        print('exiting!')
                        tictactoegame.quit()

            # exit button event
            if event.type == pygame.QUIT:
                tictactoegame.quit()


if __name__ == '__main__':
    main()
