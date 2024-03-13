---

# Tic Tac AI Game

Welcome to Tic Tac AI, a customizable Tic Tac Toe game designed to test the effectiveness of minimax and negamax algorithms on a Tic Tac Toe board of any size NxN. This game incorporates minimax and negamax algorithms, alpha-beta pruning, and a custom heuristic function to help the algorithms properly interpret game states and select the best moves.
Drawing the screen and the board was all done using pygame where every symbol and board line was drawn and calculated with MATH, _there were definitely better ways to do it, but it would not have been as satisfying_. If you find any issues running the program or have any questions feel free to reach out!

## Installation

Before you start, ensure you have Python installed on your system. This game requires Python 3.6 or newer.

To install the game dependencies, navigate to the game's root directory in your terminal and run:

```sh
pip install -r requirements.txt
```

This command will install all necessary Python packages listed in `requirements.txt`, ensuring the game runs smoothly.

## Starting the Game

To dive into the game, simply run the following command in the game's root directory:

```sh
python main.py
```

## Game Features

Tic Tac AI is packed with features that allow for a customizable gaming experience:

- **Flexible Board Size:** Play on a traditional 3x3 board or increase the size for a more complex game.
- **AI Algorithms:** Choose between minimax and negamax algorithms to challenge the AI opponent.
- **Customizable Symbols:** Select your preferred symbol to play with.
- **Dynamic AI Difficulty:** Adjust the AI depth within the `main.py` file for a more challenging or easier game experience.
- **Keybinds and Navigation:**
  - Use the **arrow keys** and **return button** to navigate through the initial menu.
  - **ESC** key or the **X** button on the window to quit the program.
  - In the options screen, configure your game preferences including opponent type (AI or human), AI algorithm, player symbol, and board size.
  - Apply changes by clicking the "apply changes" button or pressing **return**.
  - Press **q** to quit the current game and return to the main menu or **r** to reset the board with the same configuration.

## Gameplay and Rules

- **Making Moves:** Click on any square to make your move. When playing against an AI, you will see an indication of whose turn it is.
- **Game Objective:** For a 3x3 board, traditional Tic Tac Toe rules apply. For larger boards, the goal is to accumulate the most sets of 3. Each set of 3 earns you one point, with the possibility of earning multiple points for lines containing multiples of 3.
- **AI Response Time:** Depending on the AI depth and board size, the response time for the AI's move may vary. Consider the time complexity which is on average `O(b^d)` where b is the board size and n is the depth, especially for larger boards and higher AI depth levels. 
