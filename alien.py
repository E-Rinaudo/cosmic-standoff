#!/usr/bin/env python3

"""Defines the Alien class for the Cosmic Standoff game.

The Alien class represents the computer-controlled character and defines
the logic for its behavior during gameplay. The Alien selects and
executes moves based on various predefined strategies, which are
influenced by the game's current state and the distance between the
Alien and the Captain. The Alien's reacts to the Captain's actions by
choosing aggressive or defensive tactics, depending on the situation.
The class interacts with the main game instance to update the game state
and log the current board status.
"""

# TODO: Would be nice to come up with other alien movement patterns.

from __future__ import annotations

import logging
import random
import time
from typing import TYPE_CHECKING, Any, Callable

import constants as cons

if TYPE_CHECKING:
    from cosmic_standoff import CosmicStandoff

# Aliases for the relevant Enums of constants.py.
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
# logging.disable(logging.INFO)


class Alien:  # pylint: disable=too-few-public-methods
    """Represents the Alien character in the game.

    Handles the logic for the Alien's behavior, including managing its turn,
    and deciding and executing moves based on predefined strategies.
    It ensures unpredictability in the Alien actions in response to the player's
    moves.

    Attributes:
        cs_game (CosmicStandoff): Instance of the CosmicStandoff class.
    """

    cs_game: CosmicStandoff

    def __init__(self, cs_game: CosmicStandoff) -> None:
        """Initializes the Alien with a reference to the game instance."""
        self.cs_game = cs_game

    def alien_turn(self) -> None:
        """Handles the Alien's turn.

        Processes the Alien's move, updates and displays its position,
        updates the distances, and logs the current board status.
        """
        if self.cs_game.is_turn_possible():
            self._select_move()
            self.cs_game.update_character_board(Turns.ALIEN_MOVE, Chars.ALIEN)
            self._render_alien_move()
            self.cs_game.update_distance()
            self.cs_game.log_board_status()

    def _select_move(self) -> None:
        """Executes the Alien's turn by selecting and performing a move.

        A move is chosen randomly from a set of available strategies
        determined by '_decide_move()'.
        """
        print("\nThe Alien is deciding its move.")
        time.sleep(NCons.SHORT_PAUSE.value)

        selected_move = random.choice(self._decide_move())
        selected_move()

        logging.info(
            "The Alien called %s: %s.", selected_move.__name__, self.cs_game.turns[Turns.ALIEN_MOVE]
        )

        # Alien is the last to move. Used to declare the winner if the distance is 0.
        self.cs_game.turns[Turns.WHO_LAST] = Chars.ALIEN.value

    def _decide_move(self) -> list[Callable[[], Any]]:
        """Determines the alien's move based on predefined conditions.

        Returns:
            A list of move functions selected according to the game strategy.
        """
        move_condition = self._move_conditions()
        alien_moves = self._alien_moves()

        if move_condition[AlienMovesCond.WIN_CONDITION]:
            return alien_moves[AlienMoves.CLOSE_TO_WIN]
        if move_condition[AlienMovesCond.CLOSE_TO_LOSE_CONDITION]:
            return self._select_close_to_lose_move(alien_moves)
        if move_condition[AlienMovesCond.AGGRESSIVE_FLEE_CONDITION]:
            return alien_moves[AlienMoves.AGGRESSIVE_FLEE]
        return alien_moves[AlienMoves.RANDOM]

    def _move_conditions(self) -> dict[AlienMovesCond, bool]:
        """Stores the Alien's movement conditions in a dictionary.

        The viability of each move strategy is based on the distances between
        the Captain and Alien.

        Returns:
            A dictionary with the conditions to be met for the alien to move.
        """
        distances = self.cs_game.retrieve_distances()

        return {
            AlienMovesCond.WIN_CONDITION: NCons.WIN_DIST.value in distances,
            AlienMovesCond.CLOSE_TO_LOSE_CONDITION: NCons.LOSE_DIST.value in distances,
            AlienMovesCond.AGGRESSIVE_FLEE_CONDITION: any(
                NCons.LOSE_DIST.value < dist < self.cs_game.board_config[BConfig.START_DIST]
                for dist in distances
            ),
        }

    def _alien_moves(self) -> dict[AlienMoves, list[Callable[[], Any]]]:
        """Stores the Alien's move strategies in a dictionary.

        Returns:
            A dictionary mapping each move strategy to its corresponding list
            of functions that implement them.
        """
        return {
            AlienMoves.CLOSE_TO_WIN: [self._close_to_win],
            AlienMoves.NOT_AFRAID_TO_LOSE: [self._attack, self._chase, self._random],
            AlienMoves.AFRAID_TO_LOSE: [self._flee, self._freeze_move],
            AlienMoves.AGGRESSIVE_FLEE: [self._attack, self._chase, self._flee],
            AlienMoves.RANDOM: [self._random],
        }

    def _select_close_to_lose_move(
        self, alien_moves: dict[AlienMoves, list[Callable[[], Any]]]
    ) -> list[Callable[[], Any]]:
        """Selects a list of moves when the Alien is at risk of losing.

        Args:
            alien_moves: A dictionary containing lists of functions for each
                move strategy.

        Returns:
            A list of functions representing the Alien's selected move, based
                on a bold or defensive strategy.
        """
        if random.random() <= NCons.NOT_AFRAID_PROBABILITY.value:
            return alien_moves[AlienMoves.NOT_AFRAID_TO_LOSE]
        return alien_moves[AlienMoves.AFRAID_TO_LOSE]

    def _close_to_win(self) -> None:
        """Determines the Alien's move when it is close to winning.

        If the Alien is exactly one unit away from the Captain, it moves
        toward the Captain to secure victory.
        """
        if self.cs_game.distance[Dist.Y_DIST] == NCons.WIN_DIST.value:
            self._pursue_captain(Moves.DOWN, Moves.UP, Coords.Y_COORD)
        elif self.cs_game.distance[Dist.X_DIST] == NCons.WIN_DIST.value:
            self._pursue_captain(Moves.LEFT, Moves.RIGHT, Coords.X_COORD)

    def _pursue_captain(self, move_neg: Moves, move_pos: Moves, coord: Coords) -> None:
        """Determines and stores the Alien's movement toward the Captain.

        Args:
            move_neg: The move (Moves.DOWN or Moves.LEFT) to take if the Alien's
                position on the given coordinate is greater than the Captain's.
            move_pos: The move (Moves.UP or Moves.RIGHT) to take if the Alien's
                position on the given coordinate is lesser than the Captain's.
            coord: The coordinate (Coords.X_COORD or Coords.Y_COORD) used for
                comparison.
        """
        self.cs_game.turns[Turns.ALIEN_MOVE] = (
            move_neg.value
            if self.cs_game.board[Chars.ALIEN][coord] > self.cs_game.board[Chars.CAP][coord]
            else move_pos.value
        )

    def _freeze_move(self) -> None:
        """Sets the Alien's move to 'Moves.STILL', indicating no movement."""
        self.cs_game.turns[Turns.ALIEN_MOVE] = Moves.STILL.value

    def _random(self) -> None:
        """Moves the Alien in a random direction."""
        movements = [move.value for move in Moves]
        self.cs_game.turns[Turns.ALIEN_MOVE] = random.choice(movements)

    def _attack(self) -> None:
        """Moves the Alien in direct response to the Captain's movement."""
        match self.cs_game.turns[Turns.CAP_MOVE]:
            case Moves.UP.value:
                self.cs_game.turns[Turns.ALIEN_MOVE] = Moves.DOWN.value
            case Moves.DOWN.value:
                self.cs_game.turns[Turns.ALIEN_MOVE] = Moves.UP.value
            case Moves.LEFT.value:
                self.cs_game.turns[Turns.ALIEN_MOVE] = Moves.RIGHT.value
            case Moves.RIGHT.value:
                self.cs_game.turns[Turns.ALIEN_MOVE] = Moves.LEFT.value
            case Moves.STILL.value:
                self._random()
            case _:
                logging.warning(
                    "Unexpected Captain move: %s in %s.",
                    self.cs_game.turns[Turns.CAP_MOVE],
                    self._attack.__name__,
                )

    def _chase(self) -> None:
        """Moves the Alien toward the Captain based on their distances.

        The Alien moves along the axis where the distance to the Captain
        is greatest. If both distances are equal, it randomly chooses
        between the X or Y direction.
        """
        move_x = (Moves.LEFT, Moves.RIGHT, Coords.X_COORD)
        move_y = (Moves.DOWN, Moves.UP, Coords.Y_COORD)

        if self.cs_game.distance[Dist.X_DIST] > self.cs_game.distance[Dist.Y_DIST]:
            self._pursue_captain(*move_x)
        elif self.cs_game.distance[Dist.X_DIST] < self.cs_game.distance[Dist.Y_DIST]:
            self._pursue_captain(*move_y)
        else:
            self._pursue_captain(*random.choice((move_x, move_y)))

    def _flee(self) -> None:
        """Moves the Alien away from the Captain."""
        cap_move = self.cs_game.turns[Turns.CAP_MOVE]
        if cap_move != Moves.STILL.value:
            self.cs_game.turns[Turns.ALIEN_MOVE] = cap_move
        else:
            self._random()

    def _render_alien_move(self) -> None:
        """Displays the Alien new positions to the player."""
        alien_move = self.cs_game.turns[Turns.ALIEN_MOVE]

        if alien_move == Moves.STILL.value:
            print(f"\nAlien stayed '{alien_move}'.")
            print("The positions did not change, Captain:")
        else:
            print(f"\nThe Alien has moved '{alien_move}'.")
            print("Here are the updated positions, Captain:")

        self.cs_game.display_board()
