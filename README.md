# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Game purpose:** A Streamlit number-guessing game. The app picks a secret number in a range set by the difficulty (Easy 1-20, Normal 1-100, Hard 1-50). You guess within a limited number of attempts, get a Higher/Lower hint after each guess, and earn or lose points as you go.

**Bugs found:**
- The hints were backwards: a guess that was too high said "Go HIGHER!" and a guess that was too low said "Go LOWER!".
- On even attempts the secret was cast to a string, so guesses were compared as text (`"9" > "50"`) and gave wrong hints.
- The range was hard-coded to 1-100: the info text always said "1 and 100", and New Game ignored the difficulty.
- New Game did not reset the status, score or history, so after a win or loss the game stayed stuck on "Game over".

**Fixes applied:**
- Moved the game logic (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) into `logic_utils.py`, and corrected the hint messages in `check_guess`.
- Removed the `try/except TypeError` string fallback. `app.py` now always passes an int secret.
- The info text and New Game now use the range for the chosen difficulty.
- New Game resets the secret, status, score and history.
- `parse_guess` now takes the difficulty range and rejects out-of-range guesses (negative, zero, too high, huge) with a clear message instead of counting them as real guesses.
- Added tests in `tests/test_game_logic.py` for the hints, the string comparison, the difficulty ranges and edge-case inputs. The three starter tests were also fixed to unpack the `(outcome, message)` tuple.

## 📸 Demo Walkthrough

A sample game on Normal difficulty, where the secret number is 50:

1. The player enters a guess of 40. The game shows "Go HIGHER!" and the score drops to -5.
2. The player enters a guess of 70. The game shows "Go LOWER!" and the score drops to -10.
3. The player enters a guess of 50. The game shows "You won! The secret was 50. Final score: 40" and the score rises to 40.
4. Any further guess is blocked with "You already won. Start a new game to play again."
5. The player clicks New Game. The status goes back to "playing", the score and history reset, and a new secret is picked from the difficulty's range.

## 🧪 Test Results

Includes the Challenge 1 edge-case tests for `parse_guess` (negative, decimal, huge and non-numeric input).

```
$ python -m pytest tests/ -v
tests/test_game_logic.py::test_winning_guess PASSED                      [  6%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 13%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 20%]
tests/test_game_logic.py::test_too_high_hint_says_lower PASSED           [ 26%]
tests/test_game_logic.py::test_too_low_hint_says_higher PASSED           [ 33%]
tests/test_game_logic.py::test_numeric_comparison_not_string PASSED      [ 40%]
tests/test_game_logic.py::test_range_matches_difficulty PASSED           [ 46%]
tests/test_game_logic.py::test_negative_guess_rejected_when_out_of_range PASSED [ 53%]
tests/test_game_logic.py::test_negative_guess_parses_without_range PASSED [ 60%]
tests/test_game_logic.py::test_zero_and_above_high_rejected PASSED       [ 66%]
tests/test_game_logic.py::test_decimal_guess_truncated_toward_zero PASSED [ 73%]
tests/test_game_logic.py::test_huge_number_rejected_without_crashing PASSED [ 80%]
tests/test_game_logic.py::test_non_numeric_and_special_inputs_do_not_crash PASSED [ 86%]
tests/test_game_logic.py::test_blank_and_none_ask_for_a_guess PASSED     [ 93%]
tests/test_game_logic.py::test_whitespace_around_number_is_accepted PASSED [100%]
============================= 15 passed in 0.08s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
