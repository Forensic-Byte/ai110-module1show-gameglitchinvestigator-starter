"""Pure game rules used by both the Streamlit app and its tests."""

from collections.abc import MutableMapping
import random


DIFFICULTY_RANGES = {
    "Easy": (1, 20),
    "Normal": (1, 100),
    "Hard": (1, 50),
}


def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive secret-number range for a supported difficulty."""
    try:
        return DIFFICULTY_RANGES[difficulty]
    except KeyError as exc:
        raise ValueError(f"Unsupported difficulty: {difficulty}") from exc


def parse_guess(raw: str | None) -> tuple[bool, int | None, str | None]:
    """Parse a non-empty whole-number string without silently truncating it."""
    if raw is None or not raw.strip():
        return False, None, "Enter a guess."
    try:
        return True, int(raw.strip()), None
    except ValueError:
        return False, None, "Enter a whole number."


def check_guess(guess: int, secret: int) -> tuple[str, str]:
    """Return a stable outcome code and a correctly directed player hint."""
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go lower."
    return "Too Low", "📈 Go higher."


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Award points only for wins, with a floor of 10 points."""
    if outcome != "Win":
        return current_score
    points = max(10, 100 - 10 * (attempt_number - 1))
    return current_score + points


def reset_game_state(
    state: MutableMapping,
    difficulty: str,
    low: int | None = None,
    high: int | None = None,
) -> None:
    """Start a clean game and keep its secret within the selected range."""
    if low is None or high is None:
        low, high = get_range_for_difficulty(difficulty)
    state["secret"] = random.randint(low, high)
    state["attempts"] = 0
    state["score"] = 0
    state["status"] = "playing"
    state["history"] = []
    state["game_difficulty"] = difficulty
