#!/usr/bin/env python3

"""COSMIC STANDOFF - Terminal-Based Strategy Game
=====================================================================

A terminal-based game where the player and an Alien face off on a board.

The player, referred to as the 'Captain', guides a 'spaceship' on an
board with customizable size, able to move up, down, left, right, or
stay still. The 'alien spaceship' can also move in the same directions.
If after the player's move, the x or y coordinates match those of the
Alien, the player can shoot the Alien to win. The same rule applies to
the Alien.
"""

from __future__ import annotations

import json
import logging
import os
import random
import sys
import time
from textwrap import dedent
from typing import Literal, cast

import pyinputplus as pyip  # type: ignore  # pylint: disable=import-error

import constants as cons
from alien import Alien
from captain import Captain

# Aliases for all the Enums of constants.py.
NCons = cons.NumericalConstants
Paths = cons.Paths
Chars = cons.Characters
Coords = cons.Coordinates
BConfig = cons.BoardConfig
Dist = cons.Distance
Turns = cons.Turns
Moves = cons.Moves
Flags = cons.Flags
AlienMoves = cons.AlienMoves
AlienMovesCond = cons.AlienMovesConditions

logging.basicConfig(
    filename=Paths.LOG_PATH.value,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logging.disable(logging.INFO)


class CosmicStandoff:
    """Manages the setup and execution of a terminal turn-based game.

    Handles game initialization, board configurations, turn-based moves,
    and victory determination.

    Attributes:
        board (dict[Chars, dict[Coords, int]]): Stores the Captain and Alien's coordinates.
        board_config (dict[BConfig, int]): Board initial configuration settings.
        distance (dict[Dist, int]): Dynamic X and Y distances between the Captain and Alien.
        turns (dict[Turns, str]): Game's turn-related data.
        flags (dict[Flags, bool]): Contains logic flags for game flow control.
        score (dict[str, int]): Tracks the scores for the Captain and Alien.
        instances (dict[Chars, Captain | Alien]): Instances of the Captain and Alien classes.
    """

    board: dict[Chars, dict[Coords, int]]
    board_config: dict[BConfig, int]
    distance: dict[Dist, int]
    turns: dict[Turns, str]
    flags: dict[Flags, bool]
    score: dict[str, int]
    instances: dict[Chars, Captain | Alien]

    def __init__(self) -> None:
        """Initializes the game attributes."""
        self.board = {
            character: {coord: NCons.START_VAL.value for coord in Coords} for character in Chars
        }
        self.board_config = {config: NCons.START_VAL.value for config in BConfig}
        self.distance = {distance: NCons.START_VAL.value for distance in Dist}
        self.turns = {turn_data: cons.EMPTY_STRING for turn_data in Turns}
        self.flags = {flag: False for flag in Flags}
        self.score = {character.value: NCons.START_VAL.value for character in Chars}
        self.instances = {Chars.CAP: Captain(self), Chars.ALIEN: Alien(self)}

    def intro(self) -> None:
        """Displays the introduction to the game."""
        logging.debug("Starting the game.")
        print(input(cons.INTRO))

    def main(self) -> None:
        """Manages the game's lifecycle.

        Handles the game setup, the turn-based loop, and the endgame. It
        starts by initializing the game sequence, then enters a turn-
        based loop where the Captain and Alien take turns moving. The
        game continues until 'Flags.START_TURNS' is set to False.
        """
        try:
            while True:
                self._start_game_sequence()
                while self._start_turns():
                    self._handle_turns()
                    if self._is_game_over():
                        self._end_game_sequence()
        except KeyboardInterrupt:
            self._exit_game()

    def _start_game_sequence(self) -> None:
        """Handles the start of the game.

        Reads the score, sets up the board, determines the starter, and
        displays initial positions.
        """
        self._read_score()
        self._get_board_size()
        self._place_characters_on_board()
        self._who_goes_first()
        self._display_initial_positions()

    def _read_score(self) -> None:
        """Reads the score in the JSON file and displays it to the player."""
        try:
            victories = self._load_score_from_file(Paths.SCORE_PATH.value)
        except (FileNotFoundError, json.JSONDecodeError) as err:
            logging.warning("Score file issue (%s). Initializing a new score.", err)
            self._write_score()
        except OSError as err:
            self._handle_os_error(err)
        else:
            self._display_current_score(victories)

    def _load_score_from_file(self, path: str) -> dict[str, int]:
        """Loads the score from the specified JSON file.

        Args:
            path: The path of the Json file.

        Returns:
            The content of the JSON file as a dictionary.
        """
        with open(path, "r", encoding="utf-8") as score_file:
            return json.load(score_file)

    def _handle_os_error(self, err: OSError) -> None:
        """Handles OSError.

        Args:
            err: The OSError instance that was raised during file operations.
        """
        logging.error("Error reading score file: %s", err)
        print("An error occurred while reading the score file.")
        print("Check the file permissions and restart the game.")
        self._exit_game()

    def _display_current_score(self, victories: dict[str, int]) -> None:
        """Displays the current score to the player.

        Args:
            victories: The scores loaded from the JSON file.
        """
        print("\nCurrent score:\n")
        for character in self.board:
            # Loads existing score from JSON to ensure continuity, as self.score
            # resets after each game to prevent accumulation.
            self.score[character.value] += victories[character.value]
            print(f"-- {character.value}: {victories[character.value]}")

    def _write_score(self) -> None:
        """Keeps track of the score in a JSON file."""
        # Creates the directory only when the program runs for the first time.
        os.makedirs(os.path.dirname(Paths.SCORE_PATH.value), exist_ok=True)

        with open(Paths.SCORE_PATH.value, "w", encoding="utf-8") as score_file:
            victories = json.dumps(self.score)
            score_file.write(victories)
            logging.info("The score has been written to file.")

    def _get_board_size(self) -> None:
        """Defines the board size based on player input.

        Prompts the player to specify the minimum and maximum
        coordinates for the board, ensuring a size of at least 10 units.
        It then calculates and sets the starting distance between the
        Captain and Alien.
        """
        self._display_board_instructions()
        self._configure_board()
        self._set_starting_distance()

        print(f"Your board size: {self.board_config[BConfig.BOARD_SIZE]} units.")
        logging.info(
            "The board is set up. Min: %s, Max: %s, Board size: %s.",
            self.board_config[BConfig.MIN_COORD],
            self.board_config[BConfig.MAX_COORD],
            self.board_config[BConfig.BOARD_SIZE],
        )

    def _display_board_instructions(self) -> None:
        """Displays instructions for specifying board coordinates.

        Informs the player how to provide the minimum and maximum
        coordinates for the game board. The coordinates must be at least
        10 units apart to ensure the board is playable.
        """
        print(
            dedent(
                f"""
        How large should the board be at the start of the game?

        Provide the minimum and maximum coordinates, at least {NCons.MIN_BOARD.value} units apart.

        Example:
        ({NCons.MIN_COORD_EX.value}, {NCons.MAX_COORD_EX.value}) spans {NCons.SPAN.value} units.

        Note: A larger difference between the coordinates may increase game duration.
        """
            )
        )

    def _configure_board(self) -> None:
        """Prompts the player for valid board coordinates.

        Repeatedly asks the player to provide minimum and maximum
        coordinates for the game board until the difference between them
        is at least 10 units, ensuring a playable board size.
        """
        while self.board_config[BConfig.BOARD_SIZE] < NCons.MIN_BOARD.value:
            self.board_config[BConfig.MIN_COORD] = pyip.inputInt("Minimum Coordinate: ")
            self.board_config[BConfig.MAX_COORD] = pyip.inputInt("Maximum Coordinate: ")

            # Recalculates the board size.
            self.board_config[BConfig.BOARD_SIZE] = (
                self.board_config[BConfig.MAX_COORD] - self.board_config[BConfig.MIN_COORD]
            ) + NCons.UNIT_INC.value

            if self.board_config[BConfig.BOARD_SIZE] < NCons.MIN_BOARD.value:
                print(f"The board size must be at least {NCons.MIN_BOARD.value} units apart.\n")
                print(f"You chose a board of {self.board_config[BConfig.BOARD_SIZE]} units.")

    def _set_starting_distance(self) -> None:
        """Calculates and sets the starting distance as half the board size.

        Ensures the starting distance between the Captain and Alien is
        sufficient for meaningful gameplay, given the minimum board size
        of 10 units.
        """
        self.board_config[BConfig.START_DIST] = (
            self.board_config[BConfig.BOARD_SIZE] // NCons.HALF.value
        )

    def _place_characters_on_board(self) -> None:
        """Fills the board with the Captain and Alien positions."""
        self._set_captain_position()
        self._set_alien_position()
        self.log_board_status()

    def _set_captain_position(self) -> None:
        """Randomly places the Captain on the board."""
        self._set_random_position(Chars.CAP)

    def _set_random_position(self, character: Chars) -> None:
        """Assigns random coordinates to the specified character.

        The random values are chosen within the range defined by the board
        configuration, which is set up by '_configure_board()'.

        Args:
            character: The character whose coordinates to set
                ('Chars.CAP' or 'Chars.ALIEN').
        """
        for coord in self.board[character]:
            self.board[character][coord] = random.randint(
                self.board_config[BConfig.MIN_COORD],
                self.board_config[BConfig.MAX_COORD],
            )

    def _set_alien_position(self) -> None:
        """Randomly positions the Alien on the board.

        Ensures that the Alien's starting position away from the Captain
        is at least the required minimum distance, defined by
        'BConfig.START_DIST'.
        """
        while not self._is_valid_starting_distance():
            self._set_random_position(Chars.ALIEN)
            # Recalculates the distance between the Captain and the Alien.
            self.update_distance()

    def _is_valid_starting_distance(self) -> bool:
        """Validates the starting distance between the Captain and Alien.

        Checks whether the distance between the Captain and Alien on both
        the X and Y axes is at least the required minimum distance, defined
        by 'BConfig.START_DIST'.

        Returns:
            True if the distance meets the minimum requirement, False otherwise.
        """
        return all(
            self.distance[dist] >= self.board_config[BConfig.START_DIST]
            for dist in (Dist.X_DIST, Dist.Y_DIST)
        )

    def update_distance(self) -> None:
        """Updates the X and Y distances between the Captain and Alien."""
        self.distance[Dist.X_DIST] = self._get_absolute_distance(Coords.X_COORD)
        self.distance[Dist.Y_DIST] = self._get_absolute_distance(Coords.Y_COORD)

    def _get_absolute_distance(self, axis: Coords) -> int:
        """Computes the absoute distance between Captain and Alien coordinates.

        Args:
            axis: The axis for which to calculate the distance
                ('Coords.X_COORD' or 'Coords.Y_COORD').

        Returns:
            The absolute distance between the Captain and Alien as an integer.
        """
        return abs(self.board[Chars.CAP][axis] - self.board[Chars.ALIEN][axis])

    def log_board_status(self) -> None:
        """Logs the current board status of the Captain and Alien."""
        positions = [self.board[char][coord] for char in Chars for coord in Coords]
        distances = self.retrieve_distances()
        logging.info("Captain board: (X: %s, Y: %s). Alien board: (X: %s, Y: %s).", *positions)
        logging.info("Updated distance: (X: %s Y: %s).", *distances)

    def retrieve_distances(self) -> tuple[int, int]:
        """Retrieves the current distances between the Captain and Alien.

        Returns:
            A tuple containing 'Dist.X_DIST' and 'Dist.Y_DIST' distances.
        """
        return (self.distance[Dist.X_DIST], self.distance[Dist.Y_DIST])

    def _who_goes_first(self) -> None:
        """Determines who takes the first turn.

        The starter is decided randomly. Then, 'Flags.START_TURNS' is
        set to True so the turn-based loop can start.
        """
        self._display_first_turn_intro()
        time.sleep(NCons.LONG_PAUSE.value)

        starter = random.choice([char.value for char in Chars])
        print(f"The {starter} goes first.")
        logging.info("Starter: %s.", starter)

        # Updates the game state.
        self.turns[Turns.WHO_STARTS] = starter
        # Sets the START_TURNS flag to True so the turn-based loop can start.
        self.flags[Flags.START_TURNS] = True

    def _display_first_turn_intro(self) -> None:
        """Displays an introductory message before the first turn starts."""
        print(
            dedent(
                """
        The stars have aligned, Captain.
        The Universe rolls the dice to decide who takes the first move.

        Let's wait...
        """
            )
        )

    def _display_initial_positions(self) -> None:
        """Displays the initial board configuration to the player."""
        print("\nThe initial positions of your ship and the alien vessel, Captain.")
        print("Prepare for battle!")
        self.display_board()

    def display_board(self) -> None:
        """Displays the board coordinates on the screen."""
        print()
        for character, coordinates in self.board.items():
            print(f"-- {character.value} {Coords.X_COORD.value}: {coordinates[Coords.X_COORD]}")
            print(f"-- {character.value} {Coords.Y_COORD.value}: {coordinates[Coords.Y_COORD]}")

    def _start_turns(self) -> bool:
        """Checks if the turns sequence should start.

        Returns:
            True if 'Flags.START_TURNS' is set, False otherwise.
        """
        return self.flags[Flags.START_TURNS]

    def _handle_turns(self) -> None:
        """Ensures the Captain and Alien take their turn in a correct sequence.

        The order of turns is determined based on who is the starter.
        """
        match self.turns[Turns.WHO_STARTS]:
            case Chars.CAP.value:
                cast(Captain, self.instances[Chars.CAP]).captain_turn()
                cast(Alien, self.instances[Chars.ALIEN]).alien_turn()
            case Chars.ALIEN.value:
                cast(Alien, self.instances[Chars.ALIEN]).alien_turn()
                cast(Captain, self.instances[Chars.CAP]).captain_turn()
            case _:
                logging.warning("Unexpected starter: %s.", self.turns[Turns.WHO_STARTS])

    def update_character_board(
        self, move: Literal[Turns.CAP_MOVE, Turns.ALIEN_MOVE], character: Chars
    ) -> None:
        """Updates the board position of a character based on their move.

        Args:
            move: One of the five moves, stored in 'Turns.CAP_MOVE' or
                'Turns.ALIEN_MOVE', ('Up', 'Down', 'Left', 'Right', or 'Still').
            character: The character whose position is updated
                ('Chars.CAP' or 'Chars.ALIEN').
        """
        match self.turns[move]:
            case Moves.UP.value:
                self.board[character][Coords.Y_COORD] += NCons.UNIT_INC.value
            case Moves.DOWN.value:
                self.board[character][Coords.Y_COORD] -= NCons.UNIT_DEC.value
            case Moves.LEFT.value:
                self.board[character][Coords.X_COORD] -= NCons.UNIT_DEC.value
            case Moves.RIGHT.value:
                self.board[character][Coords.X_COORD] += NCons.UNIT_INC.value
            case Moves.STILL.value:
                pass  # No movement. Intentional no op for clarity.
            case _:
                logging.warning("Unexpected move: %s by %s.", self.turns[move], character.value)

    def is_turn_possible(self) -> bool:
        """Determines if a turn is possible for the Captain or Alien.

        Ensures that a turn is processed only if the distances between the
        Captain and Alien are greater than 0 in both axes.

        Returns:
            True if both distances are greater than 0, False otherwise.
        """
        distances = self.retrieve_distances()
        return all(dist > NCons.ZERO_DIST.value for dist in distances)

    def _is_game_over(self) -> bool:
        """Checks if the game is over.

        Determines if the distance between the Captain and the Alien is 0
        in either the X or Y axis.

        Returns:
            True if either distance is 0, False otherwise.
        """
        distances = self.retrieve_distances()
        return NCons.ZERO_DIST.value in distances

    def _end_game_sequence(self) -> None:
        """Handles the game's end by determining the winner.

        Determines the winner, prompts the player to play again, saves
        scores to a JSON file, and either starts a new game or exits.
        """
        self._who_won()
        self._play_again()
        self._end_game()

    def _who_won(self) -> None:
        """Determines and announces the winner of the game.

        Identifies whether the Captain or Alien reached the opponent's
        coordinates, displays the appropriate message, and updates the
        winner's score.
        """
        character = self.turns[Turns.WHO_LAST]

        match character:
            case Chars.CAP.value:
                self._captain_won()
            case Chars.ALIEN.value:
                self._alien_won()
            case _:
                logging.warning("Unexpected winner: %s.", character)

        # Updates the score for the winner.
        self.score[character] += NCons.UNIT_INC.value

    def _captain_won(self) -> None:
        """Displays a victory message for the Captain."""
        print("\nAlien at sight, Captain. Prepare to engage.")
        input("Press ENTER to shoot! ")
        print("\nBOOM! Direct hit, Captain!")
        time.sleep(NCons.SHORT_PAUSE.value)
        print("\nCongratulations Captain, you destroyed the alien and saved your species.")
        print("The galaxy is safe once again.")

    def _alien_won(self) -> None:
        """Displays messages indicating that the Alien has won the game."""
        print("\nThe Alien has reached you, Captain. It's getting ready to shoot.")
        time.sleep(NCons.SHORT_PAUSE.value)
        print("\nYou have lost the battle, Captain.")
        print("The invasion continues. Our fate is uncertain.")

    def _play_again(self) -> None:
        """Prompts the player to play another game."""
        print("\nDo you want to play again? Type: (yes or no).")
        self.flags[Flags.NEW_GAME] = pyip.inputYesNo() == "yes"

    def _end_game(self) -> None:
        """Starts a new game or quits it based on the player's choice."""
        self._write_score()

        if self.flags[Flags.NEW_GAME]:
            logging.debug("Starting a new game.")
            self._reset_state()
        else:
            self._exit_game()

    def _reset_state(self) -> None:
        """Resets necessary flags and attributes to start a new game."""
        self.board_config[BConfig.BOARD_SIZE] = NCons.RESET_VAL.value
        self.distance[Dist.X_DIST] = NCons.RESET_VAL.value
        self.distance[Dist.Y_DIST] = NCons.RESET_VAL.value
        self.flags[Flags.START_TURNS] = False
        self.flags[Flags.NEW_GAME] = False
        self.score[Chars.CAP.value] = NCons.RESET_VAL.value
        self.score[Chars.ALIEN.value] = NCons.RESET_VAL.value

    def _exit_game(self) -> None:
        """Exits the game, logging and printing a quit message."""
        exit_message = "Exiting the game..."
        logging.debug(exit_message)
        print(f"\n{exit_message}")
        time.sleep(NCons.SHORT_PAUSE.value)
        sys.exit()


if __name__ == "__main__":
    cosmic_standoff = CosmicStandoff()
    cosmic_standoff.intro()
    cosmic_standoff.main()
