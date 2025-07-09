#!/usr/bin/env python3

# region Module Docstring and Imports.
"""Defines the Captain class for the Cosmic Standoff game.

The Captain class represents the player-controlled character and manages
the logic for the Captain's turn in the game. It handles player input
for movement, updates the game board with the Captain's position, and
interacts with the main game instance to manage the state, such as
logging the current board status and updating distances.
"""

from __future__ import annotations

import logging
from textwrap import dedent
from typing import TYPE_CHECKING

import constants as cons

if TYPE_CHECKING:
    from cosmic_standoff import CosmicStandoff


# Aliases for the relevant Enums of constants.py.
Chars = cons.Characters
Moves = cons.Moves
Turns = cons.Turns

# endregion.

# region Captain Class.


class Captain:  # pylint: disable=too-few-public-methods
    """Represents the Captain character in the game.

    Handles the logic for the Captain's turn, including
    prompting the player to move, updating the Captain game board, and
    rendering the Captain's position on the screen.

    Attributes:
        cs_game (CosmicStandoff): Instance of the CosmicStandoff class.
    """

    cs_game: CosmicStandoff

    def __init__(self, cs_game: CosmicStandoff) -> None:
        """Initializes the Captain with a reference to the game instance."""
        self.cs_game = cs_game

    def captain_turn(self) -> None:
        """Handles the Captain's turn.

        Prompts the player to make a move, updates and displays the
        Captain's position, updates the distances, and logs the current
        board status.
        """
        if self.cs_game.is_turn_possible():
            self._prompt_captain_move()
            self.cs_game.update_character_board(Turns.CAP_MOVE, Chars.CAP)
            self._render_captain_move()
            self.cs_game.update_distance()
            self.cs_game.log_board_status()

    def _prompt_captain_move(self) -> None:
        """Prompts the player to choose a move and validates the input."""
        move_options = list(Moves)
        main_moves, no_move = ", ".join(move_options[:-1]), move_options[-1]

        self._print_captain_move_prompt(main_moves, no_move)
        self._get_captain_move(move_options, main_moves, no_move)

        # Captain is the last to move. Used to declare the winner if the distance is 0.
        self.cs_game.turns[Turns.WHO_LAST] = Chars.CAP

    def _print_captain_move_prompt(self, main_moves: str, no_move: str) -> None:
        """Displays the move options to the player.

        Args:
            main_moves: " 'Up', 'Down', 'Left', 'Right' ".
            no_move: 'Still'.
        """
        print(
            dedent(
                f"""
            Captain, where do you want to move?
            Type {main_moves} to move, or {no_move} to stay in place.
        """
            ),
            end="",
        )

    def _get_captain_move(self, move_options: list[Moves], main_moves: str, no_move: str) -> None:
        """Gets and validates the player's move input.

        Args:
            move_options: ['Up', 'Down', 'Left', 'Right', 'Still'].
            main_moves: " 'Up', 'Down', 'Left', 'Right' ".
            no_move: 'Still'.
        """
        # Local variable instead of constant CAP_MOVE for readability.
        # Resets to ensure the loop below runs on each turn.
        cap_move = cons.EMPTY_STRING

        while cap_move not in move_options:
            cap_move = input().lower().capitalize()

            if cap_move not in move_options:
                print(f"\n'{cap_move}' is not a valid move, Captain.")
                print(f"Choose between: {main_moves}, or {no_move}.")

        # Updates the game state.
        self.cs_game.turns[Turns.CAP_MOVE] = cap_move
        logging.info("Captain choice: %s.", cap_move)

    def _render_captain_move(self) -> None:
        """Displays the Captain new positions to the player."""
        cap_move = self.cs_game.turns[Turns.CAP_MOVE]

        print(f"\nCaptain, you moved {cap_move}.")

        if cap_move == Moves.STILL:
            print("Your position did not change:")
        else:
            print("Your new position:")
        self.cs_game.display_board()


# endregion.
