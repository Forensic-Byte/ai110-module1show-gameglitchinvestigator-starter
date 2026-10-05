# Reflection: Game Glitch Investigator

## 1. What was broken when you started?

The starter was a Streamlit number-guessing game, but its hints contradicted the comparison outcome. The initial AppTest reproduction showed a low guess paired with “Go LOWER!”; the score also became negative for an incorrect guess. The code changed the secret's type on alternating attempts, which made some comparisons lexicographic, and New Game left terminal status and prior score/history in place.

### Bug Reproduction Log

| Input / setup | Expected behavior | Actual behavior | Evidence |
|---|---|---|---|
| Secret 50, guess 40 | Too Low; hint says guess higher; score stays non-negative | Hint said “Go LOWER!”; score changed to -5 | Streamlit AppTest output: `guess 40 vs 50: outcome hint = Go LOWER!`, `score after Too Low = -5` |
| Secret 100, even attempt, guess 60 | Numeric comparison returns Too Low | Secret was cast to `"100"`; string comparison can classify `"60"` as higher | Reproduced from the starter's alternating `str(secret)` branch and fallback comparison |
| After a win, click New Game | Status returns to playing; score/history clear; secret uses selected difficulty range | Status remained won; score/history remained; reset used 1–100 | Streamlit AppTest output: `status = won`, `attempts = 0`, prior score persisted |
| Select Hard | Prompt and generated secret use the same range | Hard range was 1–50, prompt/reset said 1–100 | Source trace of difficulty range, prompt, and reset code |

## 2. How did you use AI as a teammate?

I used ChatGPT to inspect the starter, propose a small `logic_utils.py` API, and draft tests for the game rules. I accepted the suggestion to normalize guesses and secrets as integers at the boundary and keep the UI in `app.py`; unit tests confirmed numeric high/low outcomes and stable scoring. I did not accept the initial “secret changes on every click” diagnosis: source inspection showed `st.session_state` already held it across reruns, so I focused on the inconsistent type conversion and the incomplete New Game reset instead. I also kept the existing difficulty ranges rather than inventing new ones, and made the prompt/reset follow those ranges. One generated reset draft cleared the first guess after a difficulty change; AppTest caught that behavior, so the final reset clears input only for an explicit New Game action.

## 3. Debugging and testing your fixes

The AI-assisted work used deterministic tests with a secret of 50 so each outcome was predictable, plus Streamlit AppTest to reproduce the starter's incorrect hint, score, and reset state. After the fixes, all 20 pytest tests passed, covering all three outcomes, score behavior, difficulty ranges, invalid and out-of-range guesses, and clean game resets. AppTest verified the Streamlit widgets and state transitions, including the previously missed input-clear regression. The original source review also showed that ordinary reruns preserve `st.session_state`; the bug was reset logic, not randomizing on every click.

## 4. What did you learn about Streamlit and state?

Streamlit reruns the script from top to bottom after a widget interaction. Values kept only in ordinary local variables are recreated on each run, while `st.session_state` persists between reruns for that browser session. State still needs a complete initialization and reset path: retaining a terminal status or stale score can make a newly randomized game unplayable.
