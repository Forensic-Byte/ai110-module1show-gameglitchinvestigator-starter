from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    reset_game_state,
    update_score,
)


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


@pytest.mark.parametrize(
    ("difficulty", "expected"),
    [("Easy", (1, 20)), ("Normal", (1, 100)), ("Hard", (1, 50))],
)
def test_difficulty_ranges(difficulty, expected):
    assert get_range_for_difficulty(difficulty) == expected


def test_unknown_difficulty_is_rejected():
    with pytest.raises(ValueError, match="Unsupported difficulty"):
        get_range_for_difficulty("Impossible")


@pytest.mark.parametrize(
    ("guess", "secret", "expected"),
    [(50, 50, "Win"), (60, 50, "Too High"), (40, 50, "Too Low")],
)
def test_guess_outcome_and_hint(guess, secret, expected):
    outcome, message = check_guess(guess, secret)

    assert outcome == expected
    if expected == "Too High":
        assert "lower" in message.lower()
    elif expected == "Too Low":
        assert "higher" in message.lower()


@pytest.mark.parametrize("raw", [None, "", "   "])
def test_empty_guess_is_rejected(raw):
    assert parse_guess(raw) == (False, None, "Enter a guess.")


@pytest.mark.parametrize("raw", ["4.5", "abc", "--2"])
def test_non_integer_guess_is_rejected(raw):
    valid, guess, error = parse_guess(raw)

    assert not valid
    assert guess is None
    assert error == "Enter a whole number."


def test_whitespace_around_integer_is_accepted():
    assert parse_guess(" 42 ") == (True, 42, None)


@pytest.mark.parametrize("raw", ["-1", "1000000000000000000000000"])
def test_integer_edge_cases_parse_without_crashing(raw):
    valid, guess, error = parse_guess(raw)

    assert valid
    assert isinstance(guess, int)
    assert error is None
    assert not 1 <= guess <= 100


def test_misses_do_not_change_score_and_win_awards_more_on_early_attempts():
    assert update_score(20, "Too Low", 1) == 20
    assert update_score(20, "Too High", 2) == 20
    assert update_score(20, "Win", 1) == 120
    assert update_score(20, "Win", 20) == 30


def test_reset_game_state_clears_everything_and_respects_difficulty():
    state = {
        "attempts": 4,
        "score": 15,
        "status": "won",
        "history": [20, 30],
    }

    reset_game_state(state, "Hard")

    assert 1 <= state["secret"] <= 50
    assert state["attempts"] == 0
    assert state["score"] == 0
    assert state["status"] == "playing"
    assert state["history"] == []
    assert state["game_difficulty"] == "Hard"


def test_new_game_resets_a_finished_streamlit_session():
    app = AppTest.from_file(APP_PATH).run(timeout=15)
    app.session_state["status"] = "won"
    app.session_state["score"] = 70
    app.session_state["attempts"] = 3
    app.session_state["history"] = [12, 42]

    app.button[1].click().run(timeout=15)

    assert app.session_state["status"] == "playing"
    assert app.session_state["score"] == 0
    assert app.session_state["attempts"] == 0
    assert app.session_state["history"] == []
    assert 1 <= app.session_state["secret"] <= 100


def test_out_of_range_guess_does_not_consume_an_attempt():
    app = AppTest.from_file(APP_PATH).run(timeout=15)
    app.selectbox[0].set_value("Easy").run(timeout=15)
    app.text_input[0].set_value("21")
    app.button[0].click().run(timeout=15)

    assert app.session_state["attempts"] == 0
    assert "from 1 to 20" in app.error[0].value
