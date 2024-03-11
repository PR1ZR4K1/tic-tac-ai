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
from GameStatus import GameStatus
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

        # Grid Variables
        self.grid_squares = 3
        self.grid_lines = self.grid_squares - 1
        self.new_size_str = str(self.grid_squares)
        # border radius for line
        self.grid_line_br = 1
        self.grid_line_width = 4
        # total line width
        self.grid_line_tw = (self.grid_line_br + self.grid_line_width)
        self.grid_offset = 45
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
        self.grid_square_size = round(self.width - (2 * self.grid_offset + (
            (self.grid_lines-1) * self.grid_line_tw))) / (self.grid_squares)

        self.game_state = GameStatus()

        self.CIRCLE_COLOR = (8, 145, 178)
        self.CROSS_COLOR = (8, 145, 178)

        # This sets the margin between each cell
        self.MARGIN = 5
        self.FONT_SIZE = 50
        self.OPTIONS_SIZE = 25
        self.running = True

        pygame.init()

        # main menu options
        self.menu_options = [
            Text("Play", x_pos=self.width/2-20, y_pos=150,
                 font_size=self.FONT_SIZE, font_color=self.WHITE),
            Text("Options", x_pos=self.width/2-20, y_pos=300,
                 font_size=self.FONT_SIZE, font_color=self.WHITE),
            Text("Exit", x_pos=self.width/2-20, y_pos=450,
                 font_size=self.FONT_SIZE, font_color=self.WHITE)
        ]
        self.menu_options[0].setSelected(True)

        # options-menu text
        self.options_menu_items = [
            Text("Game Mode: ", x_pos=self.width/2, y_pos=30,
                 font_size=self.OPTIONS_SIZE + 10, font_color=self.WHITE, font_file='basic.ttf', underline=True),
            Text("Player Symbol: ", x_pos=self.width/2, y_pos=190,
                 font_size=self.OPTIONS_SIZE + 10, font_color=self.WHITE, font_file='basic.ttf', underline=True),
            Text("Board Size: ", x_pos=self.width/2, y_pos=350,
                 font_size=self.OPTIONS_SIZE + 10, font_color=self.WHITE, font_file='basic.ttf', underline=True),
            Text("Apply Changes", x_pos=self.width/2, y_pos=500,
                 font_size=self.OPTIONS_SIZE + 15, font_color=self.WHITE, font_file='basic.ttf'),
        ]
        self.options_menu_items[3].setSelected(True)

        # Game-mode options in options-menu
        self.game_mode_options = [
            Text("Human vs Human", x_pos=self.width/2, y_pos=85,
                 font_size=self.OPTIONS_SIZE, font_color=self.WHITE, font_file='basic.ttf'),
            Text("Human vs Computer", x_pos=self.width/2 + 16, y_pos=135,
                 font_size=self.OPTIONS_SIZE, font_color=self.WHITE, font_file='basic.ttf'),
        ]
        self.selected_game_mode = 0  # set Human vs Human to be default

        # player-symbol options in options-menu
        self.player_symbol_options = [
            Text("Cross (X)", x_pos=self.width/2, y_pos=245,
                 font_size=self.OPTIONS_SIZE, font_color=self.WHITE, font_file='basic.ttf'),
            Text("Nought (O)", x_pos=self.width/2, y_pos=295,
                 font_size=self.OPTIONS_SIZE, font_color=self.WHITE, font_file='basic.ttf'),
        ]
        self.selected_player_symbol = 0  # set cross to be default

        # set board size in options menu
        self.board_size_option = [
            Text("Size: ", x_pos=self.width/2 - 20, y_pos=405,
                 font_size=self.OPTIONS_SIZE, font_color=self.WHITE, font_file='basic.ttf'),
            Text("3", x_pos=(self.width/2) + 40, y_pos=405,
                 font_size=self.OPTIONS_SIZE, font_color=self.BLACK, bg_color=(255, 255, 255), font_file='basic.ttf')
        ]
        # make sure key clicks dont do anything unless in type box
        self.is_typing_size = False

        self.error_board_size_message = Text("Invalid Board Size! Minimum: 3", x_pos=self.width/2, y_pos=460,
                                             font_size=self.OPTIONS_SIZE, font_color=self.RED, font_file='basic.ttf')
        self.show_error_message = False

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

    # applies changes to all calculations for creating the grid
    def apply_changes(self, new_grid_size):

        self.grid_squares = new_grid_size
        self.grid_lines = self.grid_squares - 1

        # if the grid is really big, reduce the width of each line to make it look cleaner
        if (self.grid_squares > 15 and self.grid_squares < 40):
            self.grid_line_width = 2
            self.grid_line_br = 1
        elif (self.grid_squares >= 40):
            self.grid_line_width = 1
            self.grid_line_br = 0

        self.grid_line_tw = (self.grid_line_br + self.grid_line_width)
        self.grid_square_size = round(self.width - (2 * self.grid_offset + (
            (self.grid_lines-1) * self.grid_line_tw))) / (self.grid_squares)

        new_board = np.full((new_grid_size, new_grid_size), "_")
        self.game_state = GameStatus(new_board)

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

            # Displays titles and Apply button
            for obj in self.options_menu_items:

                # To highlight the apply changes button
                if (obj.isSelected):
                    pygame.draw.rect(self.screen, self.RED,
                                     obj.rectangle_rect, border_radius=1)
                    obj.setBackgroundColor(self.RED)
                    obj.hitbox = obj.get_hitbox(10, 5)
                    pygame.draw.rect(self.screen, self.WHITE,
                                     obj.hitbox, 1)  # draws the hitbox

                # draws all the titles and apply changes button
                self.screen.blit(obj.name, obj.rect)

            # Display Game mode options (Human vs. Human OR Human vs. Computer)
            for obj in self.game_mode_options:
                self.screen.blit(obj.name, obj.rect)

            # Display player symbol options (Nought (0) OR Cross (X))
            for obj in self.player_symbol_options:
                self.screen.blit(obj.name, obj.rect)

            # Display Size text
            for obj in self.board_size_option:
                self.screen.blit(obj.name, obj.rect)

            # Draw the entry box for board size
            # Adjust the position as needed
            entry_box_pos = (self.width/2 + 15, 390)
            entry_box_size = (50, 35)  # Width, Height
            self.entry_box_rect = pygame.Rect(entry_box_pos, entry_box_size)
            pygame.draw.rect(self.screen, self.WHITE, self.entry_box_rect, 0)

            # Display Size text
            for obj in self.board_size_option:
                self.screen.blit(obj.name, obj.rect)

            # Display radio buttons and hitboxes for Game Mode
            for button, option in enumerate(self.game_mode_options):
                mode_circle_center = (self.width/2-120, option.y_pos)
                option.hitbox = option.get_hitbox(50, 20, -15)
                # pygame.draw.rect(self.screen, self.RED, option.hitbox, 1) #draws the hitbox

                pygame.draw.circle(self.screen, self.WHITE,
                                   mode_circle_center, 10, 2)

                # fills in circle for whichever option is selected
                if button == self.selected_game_mode:
                    pygame.draw.circle(
                        self.screen, self.WHITE, mode_circle_center, 5)

            # Display radio buttons and hitboxes for Player Symbol
            for button, option in enumerate(self.player_symbol_options):
                symbol_circle_center = (self.width/2-120, option.y_pos)
                # creates hitbox around both button and respective text
                option.hitbox = option.get_hitbox(130, 20, -15)

                pygame.draw.circle(self.screen, self.WHITE,  # creates non filled circle
                                   symbol_circle_center, 10, 2)

                if button == self.selected_player_symbol:  # if option is selected, fill the circle
                    pygame.draw.circle(
                        self.screen, self.WHITE, symbol_circle_center, 5)

            if self.show_error_message == True:
                self.screen.blit(self.error_board_size_message.name,
                                 self.error_board_size_message.rect)

            pygame.display.update()

            # any time there is a user interaction
            for event in pygame.event.get():

                # mouse click
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos

                    # Check for game mode selection
                    for i, option in enumerate(self.game_mode_options):
                        if option.hitbox.collidepoint(mouse_pos):
                            self.selected_game_mode = i  # Update the selected game mode
                            break  # Break after selection to avoid multiple selections

                    # Check for player symbol selection
                    for i, option in enumerate(self.player_symbol_options):
                        if option.hitbox.collidepoint(mouse_pos):
                            self.selected_player_symbol = i  # Update the selected player symbol
                            break  # Break after selection to avoid multiple selections

                    # Check if they click on board size number
                    if self.entry_box_rect.collidepoint(mouse_pos):
                        self.is_typing_size = True
                    else:
                        self.is_typing_size = False

                    # Check for apply changes selection
                    if self.options_menu_items[3].hitbox.collidepoint(mouse_pos):
                        new_grid_size = int(self.new_size_str)

                        # Check for board size limit
                        if (new_grid_size < 3):
                            self.show_error_message = True
                        else:
                            self.show_error_message = False
                            self.apply_changes(new_grid_size)
                            done = True

                elif event.type == pygame.KEYDOWN:
                    if self.is_typing_size == True:
                        if event.unicode.isnumeric():
                            self.new_size_str += event.unicode
                            self.board_size_option[1].update_text(
                                self.new_size_str)

                        elif event.key == pygame.K_BACKSPACE:
                            # Remove the last character
                            self.new_size_str = self.new_size_str[:-1]
                            self.board_size_option[1].update_text(
                                self.new_size_str)

                    if event.key == pygame.K_ESCAPE:

                        self.quit()
                    elif event.key == pygame.K_RETURN:
                        new_grid_size = int(self.new_size_str)

                        # Check for board size limit
                        if (new_grid_size < 3):
                            self.show_error_message = True
                        else:
                            self.show_error_message = False
                            self.apply_changes(new_grid_size)
                            done = True

                # exit button event
                if event.type == pygame.QUIT:
                    self.quit()

    def change_turn(self):

        if (self.game_state.turn_O):
            pygame.display.set_caption("Tic Tac Toe - O's turn")
        else:
            pygame.display.set_caption("Tic Tac Toe - X's turn")

    def draw_circle(self, move):
        """
        YOUR CODE HERE TO DRAW THE CIRCLE FOR THE NOUGHTS PLAYER
        """

        circle_color = self.CIRCLE_COLOR  # The color of the cross
        circle_width = self.grid_line_width  # The width of the circle lines
        # The length of each line of the circle
        circle_radius = (self.grid_square_size * 0.40)

        half_size = self.grid_square_size // 2

        x = round((self.grid_offset +
                   (self.grid_square_size * (int(move[1]) + 1))) - half_size + (int(move[1] * self.grid_line_tw)))
        y = round(self.grid_offset +
                  (self.grid_square_size * (int(move[0]) + 1))) - half_size + (int(move[0] * self.grid_line_tw))

        # # Draw the first line of the circle
        pygame.draw.circle(self.screen, circle_color,
                           (x, y), circle_radius, circle_width)

    def draw_cross(self, move: tuple[int, int]):

        # (0, 0)
        """
        YOUR CODE HERE TO DRAW THE CROSS FOR THE CROSS PLAYER AT THE CELL THAT IS SELECTED VIA THE gui
        """
        cross_color = self.CROSS_COLOR  # The color of the cross
        cross_width = self.grid_line_width  # The width of the cross lines
        # The length of each line of the cross
        cross_size = (self.grid_square_size * 0.65)

        half_size = self.grid_square_size // 2
        # print(self.grid_square_size, ' grid square size')

        x = round((self.grid_offset +
                   (self.grid_square_size * (int(move[1]) + 1))) - half_size + (int(move[1] * self.grid_line_tw)))
        y = round((self.grid_offset +
                   (self.grid_square_size * (int(move[0]) + 1))) - half_size + (int(move[0] * self.grid_line_tw)))

        # print(f'x: {x}, y: {y}')
        # Calculate the endpoints of the first line of the cross
        start_line1 = (x - cross_size // 2, y - cross_size // 2)
        end_line1 = (x + cross_size // 2, y + cross_size // 2)

        # # Calculate the endpoints of the second line of the cross
        start_line2 = (x + cross_size // 2, y - cross_size // 2)
        end_line2 = (x - cross_size // 2, y + cross_size // 2)

        # # Draw the first line of the cross
        pygame.draw.line(self.screen, cross_color,
                         start_line1, end_line1, cross_width)

        # # Draw the second line of the cross
        pygame.draw.line(self.screen, cross_color,
                         start_line2, end_line2, cross_width)

    def is_game_over(self):
        """
        YOUR CODE HERE TO SEE IF THE GAME HAS TERMINATED AFTER MAKING A MOVE. YOU SHOULD USE THE IS_TERMINAL()
        FUNCTION FROM GAMESTATUS_5120.PY FILE (YOU WILL FIRST NEED TO COMPLETE IS_TERMINAL() FUNCTION)

        YOUR RETURN VALUE SHOULD BE TRUE OR FALSE TO BE USED IN OTHER PARTS OF THE GAME
        """

        return self.game_state.is_terminal()

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
        value, move = minimax(self.game_state, 3, False)

        self.move(move)
        print(f'Best Move: {move}, Value: {value}')
        # self.change_turn()
        # pygame.display.update()
        # terminal = self.game_state.is_terminal()
        """ USE self.game_state.get_scores(terminal) HERE TO COMPUTE AND DISPLAY THE FINAL SCORES """

    def game_reset(self):
        self.main_menu()
        """
        YOUR CODE HERE TO RESET THE BOARD TO VALUE 0 FOR ALL CELLS AND CREATE A NEW GAME STATE WITH NEWLY INITIALIZED
        BOARD STATE
        """

        pygame.display.update()

    def draw_grid(self):

        for i in range(1, self.grid_squares):

            # the y intercept for the horizontal line will always retain the same offset, but
            # needs to know the size of each preceding square that has passed.
            # we also need to include the total widths of the intercepting lines that had preceded, but
            # we do not include the current line hence i - 1
            h_y = self.grid_offset + \
                (self.grid_square_size * i) + (self.grid_line_tw * (i - 1))

            h_start_pos = (self.grid_offset, h_y)
            h_end_pos = ((self.width - self.grid_offset), h_y)

            # same as h_y, but I flip the position of the coordinates
            v_x = self.grid_offset + \
                (self.grid_square_size * i) + (self.grid_line_tw * (i - 1))

            v_start_pos = (v_x, self.grid_offset)
            v_end_pos = (v_x, (self.height - self.grid_offset))

            # draw the line
            horizontal_rect = pygame.draw.line(self.screen, self.WHITE, h_start_pos, h_end_pos, self.grid_line_width).inflate(
                self.grid_line_br, self.grid_line_br)

            # draw surrounding box to make a border radius to make our lines rounded
            pygame.draw.rect(self.screen, self.WHITE,
                             horizontal_rect, border_radius=self.grid_line_br)

            # draw the line
            vertical_rect = pygame.draw.line(self.screen, self.WHITE, v_start_pos, v_end_pos, self.grid_line_width).inflate(
                self.grid_line_br, self.grid_line_br)

            # draw surrounding box to make a border radius to make our lines rounded
            pygame.draw.rect(self.screen, self.WHITE,
                             vertical_rect, border_radius=self.grid_line_br)

        for i in range(self.grid_squares):
            for j in range(self.grid_squares):
                if self.game_state.board_state[i][j] == 'x':
                    self.draw_cross((i, j))
                elif self.game_state.board_state[i][j] == 'o':
                    self.draw_circle((i, j))

    def get_clicked_box(self, mouse_pos):
        x_click, y_click = mouse_pos  # Unpack the mouse position

        # Calculate the column and row index based on the mouse click position
        if self.grid_offset < x_click < (self.grid_offset + self.grid_square_size):
            col = (x_click - self.grid_offset - 1) // (self.grid_square_size)
        else:
            col = (x_click - self.grid_offset) // (self.grid_square_size +
                                                   self.grid_line_tw)

        # print((x_click - self.grid_offset) /
            #   (self.grid_square_size + self.grid_line_tw), ' col')

        if y_click > self.grid_offset and y_click < self.grid_offset + self.grid_square_size:
            row = (y_click - self.grid_offset) // (self.grid_square_size)
        else:
            row = (y_click - self.grid_offset) // (self.grid_square_size +
                                                   self.grid_line_tw)

        # print((y_click - self.grid_offset) /
        #       (self.grid_square_size + self.grid_line_tw), ' row')

        # Check if the click is within the bounds of the grid
        if 0 <= col < self.grid_squares and 0 <= row < self.grid_squares:
            # print(f"Clicked on box at row {row}, column {col}")
            return int(row), int(col)
        else:
            # print("Clicked outside of the grid")
            return None, None

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

                        mouse_pos = pygame.mouse.get_pos()
                        move = self.get_clicked_box(mouse_pos)

                        if move in self.game_state.get_moves() and self.game_state.turn_O == False:
                            self.move(move)
                            if not self.is_game_over():
                                self.play_ai()
                        # print(mouse_pos)
                            print(f'Clicked!, {self.game_state.board_state}')

                    case pygame.KEYDOWN:

                        if event.key == pygame.K_q:
                            done = True

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
