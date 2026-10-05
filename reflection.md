# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Code-level cause |
|-------|-------------------|-----------------|------------------|
| Guess 60, secret 50 (attempt 4) | "Go LOWER!" | "Go HIGHER!" (hints backwards) | `check_guess` returned the HIGHER message for "Too High" and the LOWER message for "Too Low" |
| Guess 9, secret 50, on an even attempt (attempt 2) | Outcome "Too Low", score -5 | Outcome "Too High", score +5. The message happened to read "Go HIGHER!" only because the messages were also swapped, so the string bug was hidden | `app.py` passed `str(secret)` on even attempts, so `check_guess` hit its `TypeError` fallback and compared strings (`"9" > "50"`) |
| Pick Easy (range 1-20), then press New Game | Info text says 1 to 20 and New Game draws from 1-20 | Info text says 1 to 100 and New Game drew 35 from 1-100 | The info text was hard-coded and New Game called `random.randint(1, 100)` instead of using `low, high` |
| Win, then press New Game | A fresh game starts | Screen still says "You already won. Start a new game to play again." and the status stays "won" | The New Game handler reset `attempts` and `secret` but not `status`, `score` or `history` |

**Terminal trace of the starter code** (also committed as [bug_trace.txt](bug_trace.txt)). I ran the starter `app.py` (commit `f651d72`) headless with Streamlit's `AppTest`:

```
Starter code (commit f651d72), run headless with Streamlit AppTest
Run 1: secret forced to 50, Normal difficulty
  attempt 2 (even): guess  9, secret 50 -> ['Go HIGHER!'], score 0 -> 5
  attempt 3 (odd): guess  9, secret 50 -> ['Go LOWER!'], score 5 -> 0
  attempt 4 (even): guess 60, secret 50 -> ['Go HIGHER!'], score 0 -> 5
Run 2: Easy difficulty selected
  sidebar: Range: 1 to 20 | main text: Guess a number between 1 and 100. Attempts left: 5
  New Game secret: 35 (drawn from 1-100)
Run 3: win, then click New Game
  status after win: won
  status after New Game: won | screen: ['You already won. Start a new game to play again.']
```

---

## 2. How did you use AI as a teammate?

- **Tool:** Claude Code (agent mode) in VS Code.
- **Correct suggestion:** Claude pointed out that `app.py` cast the secret to `str` on even attempts, pushing `check_guess` into its `TypeError` fallback that compares strings. That was correct because `"9" > "50"` is True in Python. I verified it with a new test (`check_guess(9, 50)` returns "Too Low") and by running the app headless: on attempt 2 with secret 50, guessing 9 now says "Go HIGHER!".
- **Suggestion I did not accept as written:** The existing `try/except TypeError` fallback in `check_guess` could have been patched to convert types safely. I removed it instead and made the caller always pass an int. A fallback that silently changes types hides bugs and is harder to read. I verified by re-running pytest (7 passed) and the headless app run. Also, the starter tests compared the whole `(outcome, message)` tuple to a string, so I changed them to unpack the outcome rather than change `check_guess`'s return shape.

---

## 3. Debugging and testing your fixes

- **Deciding a bug was fixed:** a failing test turned green, then I confirmed the same behavior in the running app.
- **Tests:** `pytest` runs 15 tests, all passing. `test_too_high_hint_says_lower` and `test_too_low_hint_says_higher` cover the backwards hints. `test_numeric_comparison_not_string` covers the string bug. The three starter tests were fixed to unpack the `(outcome, message)` tuple. Eight more cover `parse_guess` edge cases (negatives, decimals, huge and non-numeric input), and `parse_guess` now rejects out-of-range guesses. Streamlit's `AppTest` ran the app headless with secret 50: guesses 60, 9, 40 gave LOWER, HIGHER, HIGHER, with no exceptions.
- **AI help:** Claude wrote the tests and spotted that the starter tests could never pass because of the tuple return.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  - Streamlit re-runs the whole script from top to bottom every time you click a button or change an input. Normal variables get reset on each rerun, so the game would forget the secret number. `st.session_state` is a dictionary that survives reruns, so the secret, attempts, score and history live there. The `if "secret" not in st.session_state` checks make sure they are only set once, on the first run.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  - Writing a failing test first, then fixing the code until it passes, and then checking the same behavior in the running app.
- What is one thing you would do differently next time you work with AI on a coding task?
  - I would read each change before accepting it and ask the AI to explain why it made it. I let Claude Code do most of the work here, so I want to understand every line myself next time.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - AI generated code can look fine and still be wrong, such as the backwards hints and the string comparison. It is a fast teammate, but I still have to test and verify its work.
