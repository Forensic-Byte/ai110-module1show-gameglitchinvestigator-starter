"""Streamlit interface for the Game Glitch Investigator guessing game."""

import streamlit as st

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    reset_game_state,
    update_score,
)


st.set_page_config(page_title="Game Glitch Investigator", page_icon="🎮")
st.title("🎮 Game Glitch Investigator")
st.caption("A number-guessing game with clear hints and predictable rules.")

st.sidebar.header("Settings")
difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Normal", "Hard"], index=1)
attempt_limit_map = {"Easy": 6, "Normal": 8, "Hard": 5}
attempt_limit = attempt_limit_map[difficulty]
low, high = get_range_for_difficulty(difficulty)
st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if st.session_state.get("game_difficulty") != difficulty:
    # FIX: Reset the complete session when a new difficulty is selected.
    reset_game_state(st.session_state, difficulty, low, high)
    st.session_state[f"guess_input_{difficulty}"] = ""
elif st.session_state.pop("clear_guess_on_next_run", False):
    st.session_state[f"guess_input_{difficulty}"] = ""

st.subheader("Make a guess")
st.info(
    f"Guess an integer from {low} to {high}. "
    f"Attempts left: {max(0, attempt_limit - st.session_state.attempts)}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input("Enter your guess:", key=f"guess_input_{difficulty}")
col1, col2 = st.columns(2)
with col1:
    submit = st.button("Submit Guess 🚀", disabled=st.session_state.status != "playing")
with col2:
    new_game = st.button("New Game 🔁")
show_hint = st.checkbox("Show directional hint", value=True)

if new_game:
    reset_game_state(st.session_state, difficulty, low, high)
    st.session_state["clear_guess_on_next_run"] = True
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You won! Start a new game when you're ready to play again.")
    else:
        st.error(f"Game over. The secret was {st.session_state.secret}.")
else:
    if submit:
        valid, guess, error = parse_guess(raw_guess)
        if not valid:
            st.error(error)
        elif not low <= guess <= high:
            st.error(f"Enter a number from {low} to {high}.")
        else:
            # FIX: Count only valid in-range guesses and compare integers consistently.
            st.session_state.attempts += 1
            st.session_state.history.append(guess)
            outcome, message = check_guess(guess, st.session_state.secret)
            st.session_state.score = update_score(
                st.session_state.score, outcome, st.session_state.attempts
            )
            if outcome == "Win":
                st.session_state.status = "won"
                st.balloons()
                st.success(f"{message} Final score: {st.session_state.score}")
            elif st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"{outcome}. No attempts left; the secret was "
                    f"{st.session_state.secret}."
                )
            elif show_hint:
                st.warning(f"{outcome}. {message}")
            else:
                st.info(outcome)

st.divider()
st.caption("Built with human-in-the-loop debugging and verification.")
