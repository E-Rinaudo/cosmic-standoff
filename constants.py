#!/usr/bin/env python3

# region Module Docstring and Imports.
"""Constants and configuration values for the Cosmic Standoff program.

This module stores fixed values to avoid hardcoding them throughout the
project.
"""

import os
from enum import IntEnum, StrEnum

# endregion.

# region Constants.

INTRO: str = """
                            ***Cosmic Standoff***

In a far away galaxy, you are the captain of an ultra-advanced spaceship,
your species last hope.

Looming nearby is an alien spaceship, ready for battle.
It's a high-stakes standoff: one wrong move could be your last.
Will your strategic skills lead to victory, or will the alien outmaneuver you?
Prepare yourself, Captain. The fate of your species is in your hands.


How to Play:
  - You and the alien take turns to move on the game board.
  - On your turn, you can move: Up, Down, Left, Right or stay Still.
  - The alien will also be able to choose between the same directions.
  - NOTE: Press Ctrl + C at any time to quit the game.

How to Win:
  - Your goal is to reach the alien's position, either in the X or Y coordinate.
  - The alien is also trying to reach you, so you must stay alert.
  - The first one to match the opponent's position in either axis, wins."""

EMPTY_STRING = ""


class NumericalConstants(IntEnum):
    """Enum defining labels for the numerical values used in the game.

    Attributes:
        MIN_BOARD (int): Min board size to ensure enough moves before game ends.
        HALF (int): Used to set the starting distance between Captain and Alien.
        UNIT_INC (int): One unit used in various increments in the game.
        UNIT_DEC (int): One unit used in various decrements in the game.
        MIN_COORD_EX (int): Example of a minimum coordinate value.
        MAX_COORD_EX (int): Example of a maximum coordinate value.
        SPAN (int): Example board size (MAX_COORD_EX - MIN_COORD_EX) + UNIT_INC.
        START_VAL (int): Initial value to start game instances.
        ZERO_DIST (int): Captain and Alien distance on coordinate match.
        RESET_VAL (int): Value to reset attributes when starting a new game.
        LOSE_DIST (int): Distance indicating Captain and are 2 units apart.
        WIN_DIST (int): Distance indicating Captain and are 1 unit apart.
        LONG_PAUSE (int): Duration for a long pause, in seconds.
        SHORT_PAUSE (int): Duration for a short pause, in seconds.
        NOT_AFRAID_PROBABILITY (int): Probability that the Alien will make an
            unpredictable move, instead of taking a defensive move.
    """

    MIN_BOARD = 10
    HALF = 2
    UNIT_INC = 1
    UNIT_DEC = 1
    MIN_COORD_EX = -5
    MAX_COORD_EX = 5
    SPAN = (MAX_COORD_EX - MIN_COORD_EX) + UNIT_INC
    START_VAL = 0
    ZERO_DIST = 0
    RESET_VAL = 0
    LOSE_DIST = 2
    WIN_DIST = 1
    LONG_PAUSE = 2
    SHORT_PAUSE = 1
    NOT_AFRAID_PROBABILITY = 0.2


class Paths(StrEnum):
    """Enum defining labels for the paths used in the game.

    Attributes:
        SCORE_PATH (str): The path to the score file.
        LOG_PATH (str): The path to the logging file.
    """

    SCORE_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "c_standoff_score/score.json"
    )
    LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log_file.txt")


class Characters(StrEnum):
    """Enum defining labels for the characters of the game.

    Attributes:
        CAP (str): The Captain character.
        ALIEN (str): The Alien character.
    """

    CAP = "Captain"
    ALIEN = "Alien"


class Coordinates(StrEnum):
    """Enum defining labels for the coordinate values of the board.

    Attributes:
        X (str): Label for the X coordinate.
        Y (str): Label for the Y coordinate.
    """

    X_COORD = "X"
    Y_COORD = "Y"


class BoardConfig(StrEnum):
    """Enum defining labels for the board initial configuration settings.

    Attributes:
        MIN_COORD (str): Label for the minimum coordinate for placing characters.
        MAX_COORD (str): Label for the maximum coordinate for placing characters.
        BOARD_SIZE (str): Label for the board size ((max_coord - min_coord) + 1).
        START_DIST (str): Label for the initial distance between the characters.
    """

    MIN_COORD = "min_coord"
    MAX_COORD = "max_coord"
    BOARD_SIZE = "board_size"
    START_DIST = "start_distance"


class Distance(StrEnum):
    """Enum defining labels for the distances between the characters.

    Attributes:
        X_DIST (str): Label for the dynamic distance on the x axis.
        Y_DIST (str): Label for the dynamic distance on the y axis.
    """

    X_DIST = "x_distance"
    Y_DIST = "y_distance"


class Turns(StrEnum):
    """Enum defining labels for the turns-related data used in the game.

    Attributes:
        WHO_STARTS (str): Label for who makes the first move (randomly decided).
        WHO_LAST (str): Label for the last character to move in a turn.
        CAP_MOVE (str): Label for the possible moves the Captain can make.
            Can be ('Up', 'Down', 'Left', 'Right', or 'Still').
        ALIEN_MOVE (str): Same as CAPTAIN_MOVE.
    """

    WHO_STARTS = "who_starts"
    WHO_LAST = "who_last"
    CAP_MOVE = "captain_move"
    ALIEN_MOVE = "alien_move"


class Moves(StrEnum):
    """Enum defining labels for the moves the Captain and Alien can make.

    Attributes:
        UP (str): Up move.
        DOWN (str): Down move.
        LEFT (str): Left move.
        RIGHT (str): Right move.
        STILL (str): Still move.
    """

    UP = "Up"
    DOWN = "Down"
    LEFT = "Left"
    RIGHT = "Right"
    STILL = "Still"


class Flags(StrEnum):
    """Enum defining labels for the game logic flags used in the game.

    Attributes:
        START_TURNS (str): Label for the flag to control the turn-based loop.
        NEW_GAME (str): Label for the flag to start a new game.
    """

    START_TURNS = "start_turns"
    NEW_GAME = "new_play"


class AlienMoves(StrEnum):
    """Enum defining labels for the Alien's movement strategies.

    Attributes:
        RANDOM (str): Label for a strategy where the Alien moves randomly.
        AFRAID_TO_LOSE (str): Label for a defensive strategy where the Alien
            avoids losing when close to the Captain.
        NOT_AFRAID_TO_LOSE (str): Label for a strategy where the Alien ignores
            defensive behavior and takes unpredictable actions instead.
        AGGRESSIVE_FLEE (str): Label for a mixed strategy where the Alien moves
            either towards or away from the Captain based on the situation.
        CLOSE_TO_WIN (str): Label for a strategy where the Alien moves to secure
            victory when close to the Captain.
    """

    RANDOM = "random"
    AFRAID_TO_LOSE = "afraid_to_lose"
    NOT_AFRAID_TO_LOSE = "not_afraid_to_lose"
    AGGRESSIVE_FLEE = "aggressive_flee"
    CLOSE_TO_WIN = "close_to_win"


class AlienMovesConditions(StrEnum):
    """Enum defining labels for conditions to pick the Alien's strategy.

    Attributes:
        WIN_CONDITION (str): Label for the condition when the Alien is close to
            winning.
        CLOSE_TO_LOSE_CONDITION (str): Label for the condition when the Alien
            is close to losing.
        AGGRESSIVE_FLEE_CONDITION (str): Label for the condition when the Alien
            should use an aggressive or flee strategy.
    """

    WIN_CONDITION = "win_condition"
    CLOSE_TO_LOSE_CONDITION = "lose_condition"
    AGGRESSIVE_FLEE_CONDITION = "aggressive_flee_condition"


# endregion.
