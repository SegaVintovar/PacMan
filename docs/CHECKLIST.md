# Pac-Man: task checklist (subject v1.4)

Status per task. `[x]` = done, `[ ]` = todo. Update this file as work
progresses and keep it in the project management folder.

## Done

- [x] 10 levels, fixed seed on level 1, random seeds after
- [x] Score and lives carry over between levels
- [x] Per-level timer (timeout ends the game)
- [x] Win condition (all gums eaten, all levels completed)
- [x] Pacman and ghost movement
- [x] A-Maze-ing integration and maze rendering
- [x] Super-pacgums in the 4 corners, 4 ghosts in the corners, Pacman in the middle
- [x] Main menu (Start, Highscores, Instructions, Exit)
- [x] Pause screen (resume, return to menu)
- [x] Instructions screen
- [x] HUD: score, lives, level, time
- [x] Win / lose screen with name entry (max 10 chars, alphanumeric + spaces)
- [x] Highscore file, top 10, shown in the menu
- [x] Config loading with pydantic and default fallback (needs fixes, see Config)

## Gameplay

- [ ] Lose a life on ghost touch; Pacman respawns in the middle; ghosts reset to corners
- [ ] Game over at 0 lives
- [ ] Super-pacgum makes ghosts edible for a limited time
- [ ] Edible ghosts flee; eating one gives `points_per_ghost`
- [ ] Eaten ghost respawns in its corner after a few seconds
- [ ] Ghost AI: chase the player (e.g. BFS); `Behaviour.a_star` is an empty stub (can be done after publishing)
- [ ] Fix `Level.show_gums`: do not remove from the list while looping over it
- [ ] Optional: arrow keys next to WASD

## Config

- [ ] Ignore lines starting with `#` (optionally `//` and `/* */`)
- [ ] Launch with `python3 pac-man.py config.json` (add `pac-man.py` at root)
- [ ] Clamp invalid values one by one to defaults, log a clear message, continue
- [ ] Unknown keys ignored, no traceback anywhere
- [ ] Remove dependency on `storage/config.json`; no `sys.exit(1)` on bad config
- [ ] Fix `GameConfig.load` and the "at least 15" vs `< 10` message mismatch
- [x] `highscore_filename` key (in highscore fix patch)
- [ ] Test odd values: missing keys, strings instead of ints, tiny/huge sizes

## Highscore

- [x] Share one module for loading/saving (`highscores.py`)
- [x] Scoreboard reloads every time it is opened
- [x] Names of 1-2 characters no longer break the whole list
- [x] Entries validated one by one (bad ones skipped, good ones kept)
- [x] Name field cleared after saving / leaving the name screen
- [ ] Store the file in a user-writable directory for the packaged build
- [ ] Manual test: save score, open scoreboard without restart; broken file; read-only dir

## Cheat mode

- [ ] Activation method (config flag or key) and mention on instructions screen
- [ ] Invincibility
- [ ] Skip level
- [ ] Freeze ghosts
- [ ] Extra lives
- [ ] Speed boost
- [ ] Make ghosts edible (to test ghost eating quickly)

## Maze generator

- [ ] Set `PERFECT = False` according to the assigned package's interface
- [ ] Handle generator failure cleanly (message, no traceback)

## Robustness

- [ ] Load Pacman sprites once instead of every frame
- [ ] Asset paths independent of the working directory (needed for packaging)
- [ ] Edge cases: empty name, Escape in name entry, closing the window in every state

## Linting and code quality

- [ ] flake8 clean
- [ ] mypy clean (`lint` flags), try `--strict`
- [ ] Type hints everywhere, PEP 257 docstrings
- [ ] Remove dead code (`if __name__` block in `game.py`, unused imports, stubs)

## Root files and README

- [ ] `Makefile`: `install`, `run`, `debug`, `clean`, `lint`, optional `lint-strict`
- [ ] `.gitignore`
- [ ] `requirements.txt` or `pyproject.toml`
- [ ] `README.md`, first line in italics: *This project has been created as part of the 42 curriculum by vsudak, brogaar* (check logins)
- [ ] README sections: Description, Instructions, Resources (incl. AI use), Configuration, Highscore, Maze Generation, Implementation, General Software Architecture, Project Management

## Project management folder

- [ ] Task list (this file)
- [ ] Timeline and progress versus plan
- [ ] Risk analysis
- [ ] Team organisation (who did what, decisions, issues)
- [ ] Acceptance test plan (features tested, bugs found/fixed)
- [ ] Blocking points and conflicts

## Packaging and itch.io

- [ ] Packaging script/spec at repo root
- [ ] Linux build and Windows build (Windows machine or GitHub Actions)
- [ ] In-package instructions (controls, options, config) and default config
- [ ] Upload to itch.io as unlisted/restricted
- [ ] Test the downloaded build on a clean machine
- [ ] Be able to regenerate the package during the review

## Review preparation

- [ ] Both teammates can explain all code (recode step)
- [ ] Config changes during the defence tested
