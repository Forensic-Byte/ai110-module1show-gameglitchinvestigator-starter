# Game Glitch Investigator: The Impossible Guesser

## Purpose

A small Streamlit number-guessing game. The player chooses a difficulty, guesses a secret integer, receives higher/lower hints, and tries to win within the attempt limit.

## Setup

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Phase 1: Glitch Hunt

The starter app had several reproducible issues. In this collaboration, ChatGPT used Streamlit's `AppTest` to set known game state and inspect the result instead of guessing at random secrets.

| Reproduction | Expected | Observed |
|---|---|---|
| Secret `50`, guess `40` | “Too Low” and a hint to guess higher | Outcome was Too Low, but the hint said “Go LOWER!” and the score dropped to `-5`. |
| Secret `100`, guess `60` on an even attempt | “Too Low” | The code converted the secret to a string and compared `"60"` to `"100"` lexicographically, so the outcome could be wrong. |
| Win or lose, then choose New Game | Fresh playable game, zero score/history, selected difficulty range | Status stayed terminal, score/history were retained, and the secret was reset to 1–100 regardless of difficulty. |
| Choose Hard | Display and secret range should match | Hard used 1–50, while the guess prompt and New Game reset used 1–100. |

The secret was stored in `st.session_state`, so it did not actually change on every ordinary rerun. The real state defect was incomplete initialization/reset behavior and a type conversion that made comparisons inconsistent.

## Demo Walkthrough

1. Select a difficulty; the displayed range and allowed attempts match that setting.
2. Open Developer Debug Info to inspect the secret for a deterministic demo.
3. Enter a number below the secret; the game says “Too Low” and hints to guess higher.
4. Enter a number above the secret; the game says “Too High” and hints to guess lower.
5. Guess the secret to win, or use the attempt limit; choose New Game to start cleanly.

## Document Your Experience

The game is a Streamlit number-guessing game with Easy, Normal, and Hard ranges, a limited number of attempts, directional hints, and a score. The repaired version corrects the reversed hints, inconsistent numeric/string comparison, invalid-input attempt handling, score changes on incorrect guesses, mismatched range display/reset, and incomplete New Game reset. The game logic now lives in `logic_utils.py`, separate from the Streamlit UI.

## Test Results

The suite includes the original win/high/low checks, validation and range boundaries, scoring, difficulty changes, and Streamlit session resets. The optional **Challenge 1: Advanced Edge-Case Testing** is included.

```text
$ python -m pytest tests/
============================= test session starts ==============================
platform darwin -- Python 3.13.15, pytest-9.1.1, pluggy-1.6.0
rootdir: game_glitch_investigator
plugins: anyio-4.15.1
collected 20 items

tests/test_game_logic.py ....................                            [100%]

============================== 20 passed in 0.85s ==============================
```

The tests ran with the VS Code Python environment. `AppTest` exercised the Streamlit widgets and state without needing a separate browser server.
