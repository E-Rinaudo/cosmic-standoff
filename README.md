# Cosmic Standoff

[![Stargazers][stars-shield]][stars-url]
[![MIT License][license-shield]][license-url]
[![Gmail][Gmail-shield]][Gmail-url]

**Cosmic Standoff** is a terminal-based, turn-based strategy game written in Python.
The goal is to outmaneuver the Alien on a customizable board and reach its position before it reaches yours.

---

## Table of Contents

- [Cosmic Standoff](#cosmic-standoff)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Features](#features)
  - [Built With](#built-with)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
    - [Run the Game](#run-the-game)
  - [Usage](#usage)
    - [Sample Output](#sample-output)
    - [Code Example](#code-example)
  - [License](#license)
  - [Contact](#contact)

---

## About

Play as the Captain, facing off against a computer-controlled Alien. Each turn, you and the Alien move across a customizable board. The Alien uses different movement strategies to challenge you. The first to reach the other's position wins.

[back to top](#cosmic-standoff)

---

## Features

- Customizable board size
- Multiple Alien movement strategies (aggressive, defensive, random)
- High score tracking (JSON)
- Fully terminal-based

[back to top](#cosmic-standoff)

---

## Built With

- [![Python][Python-badge]][Python-url]
- [![Visual Studio Code][VSCode-badge]][VSCode-url]
- [![PyInputPlus][PyInputPlus-badge]][PyInputPlus-url]
- [![Mypy][Mypy-badge]][Mypy-url]
- [![Black][Black-badge]][Black-url]
- [![Docformatter][Docformatter-badge]][Docformatter-url]
- [![Pylint][Pylint-badge]][Pylint-url]
- [![Flake8][Flake8-badge]][Flake8-url]
- [![Ruff][Ruff-badge]][Ruff-url]
  
[back to top](#cosmic-standoff)

---

## Getting Started

### Prerequisites

- [Python][Python-download]
- [Git][Git-download]
  
### Setup

```bash
# Clone the repository
git clone https://github.com/E-Rinaudo/cosmic_standoff.git # Using Git
gh repo clone E-Rinaudo/cosmic_standoff # Using GitHub CLI

# Create a virtual environment
cd cosmic_standoff
python -m venv venv

# Activate the virtual environment (all platforms)
source venv/bin/activate # On macOS/Linux
venv\Scripts\activate # On Windows
.\venv\Scripts\activate.bat # On Windows with CMD
.\venv\Scripts\activate.ps1 # On Windows with PowerShell
source venv/Scripts/activate # On Windows with Unix-like shells (e.g. Git Bash)

# Install dependencies
pip install -r requirements.txt
```

### Run the Game

```bash
python cosmic_standoff.py
```

[back to top](#cosmic-standoff)

---

## Usage

- On launch, follow the prompts to set up your board.
- Take turns moving as the Captain; the Alien will respond.
- The game ends when either you or the Alien reach the same X or Y coordinate.

### Sample Output

```text
How large should the board be at the start of the game?
Provide the minimum and maximum coordinates, at least 10 units apart.
...
Captain, where do you want to move?
Type Up, Down, Left, Right to move, or Still to stay in place.
...
The Alien is deciding its move.
...
Congratulations Captain, you destroyed the alien and saved your species.
```

### Code Example

An example from the `cosmic_standoff.py`  module, which demonstrates the main game loop and how the game manages its lifecycle:

```py
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
```

[back to top](#cosmic-standoff)

---

## License

Distributed under the MIT License. See [`LICENSE.txt`](LICENSE.txt) for details.

[back to top](#cosmic-standoff)

## Contact

If you have any questions, feedback, or just want to get in touch, feel free to reach out to me via email. Your feedback is appreciated as it helps me to continue improving.

- Email: <enricorinaudo91@gmail.com>  

You can also explore my GitHub profile.

- GitHub: [E-Rinaudo](https://github.com/E-Rinaudo)

[back to top](#cosmic-standoff)

---

**Happy coding!**

<!-- SHIELDS -->
[stars-shield]: https://img.shields.io/github/stars/E-Rinaudo/cosmic_standoff.svg?style=flat
[stars-url]: https://github.com/E-Rinaudo/cosmic-standoff/stargazers
[license-shield]: https://img.shields.io/github/license/E-Rinaudo/cosmic_standoff.svg?style=flat
[license-url]: https://github.com/E-Rinaudo/cosmic-standoff/blob/main/LICENSE.txt
[Gmail-shield]: https://img.shields.io/badge/Gmail-D14836?style=flat&logo=gmail&logoColor=white
[Gmail-url]: mailto:enricorinaudo91@gmail.com

<!-- BADGES -->
[Python-badge]: https://img.shields.io/badge/python-3670A0?logo=python&logoColor=ffdd54&style=flat
[Python-url]: https://docs.python.org/3/
[VSCode-badge]: https://img.shields.io/badge/Visual%20Studio%20Code-007ACC?logo=visualstudiocode&logoColor=fff&style=flat
[VSCode-url]: https://code.visualstudio.com/docs
[PyInputPlus-badge]:https://img.shields.io/badge/PyInputPlus-4caf50?logo=python&logoColor=ffdd54&style=flat
[PyInputPlus-url]: https://pyinputplus.readthedocs.io/en/latest/
[Mypy-badge]: https://img.shields.io/badge/mypy-checked-blue?style=flat
[Mypy-url]: https://mypy.readthedocs.io/
[Black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[Black-url]: https://black.readthedocs.io/en/stable/
[Pylint-badge]: https://img.shields.io/badge/linting-pylint-yellowgreen?style=flat
[Pylint-url]: https://pylint.readthedocs.io/
[Ruff-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
[Ruff-url]: https://docs.astral.sh/ruff/tutorial/
[Flake8-badge]: https://img.shields.io/badge/linting-flake8-blue?style=flat
[Flake8-url]: https://flake8.pycqa.org/en/latest/
[Docformatter-badge]: https://img.shields.io/badge/formatter-docformatter-fedcba.svg
[Docformatter-url]: https://github.com/PyCQA/docformatter

<!-- PREREQUISITES LINKS -->
[Python-download]: https://www.python.org/downloads/
[Git-download]: https://git-scm.com
