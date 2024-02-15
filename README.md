# Guide

### Python
- Use pygame-ce, not pygame (already configured)
- For general settings (eg. window size) use one `config.py` file
- When dealing with file paths, create them in one `paths.py` file and import from it
- Writing tests is optional but encouraged
- Type hints should generally be used
- Docstrings for methods which are not 100% self explanatory
- Imports should always be relative (except for main file)
- Avoid `*` imports

### Git
- always work on a branch (never on master)
- use issues (and labels)
- write meaningful commit messages

# Launching
- To start the game, run `poetry run python main/PocketLeague/run_game.py`
- To start the demo, run `poetry run python main/PocketLeague/run_demo.py`
