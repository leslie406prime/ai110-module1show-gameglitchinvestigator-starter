# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess 60, secret 50 | "Go LOWER!" | "Go HIGHER!" (hints backwards) | none |
| Guess 9, secret 50, on an even attempt | "Go HIGHER!" | Compared as strings ("9" > "50"), wrong hint | none |
| Press New Game / pick Easy | Range matches difficulty | Info text always says 1 to 100; New Game always uses 1-100 | none |

---

## 2. How did you use AI as a teammate?

- **Tool:** Claude Code (agent mode) in VS Code.
- **Correct suggestion:** Claude pointed out that `app.py` cast the secret to `str` on even attempts, pushing `check_guess` into its `TypeError` fallback that compares strings. That was correct because `"9" > "50"` is True in Python. I verified it with a new test (`check_guess(9, 50)` returns "Too Low") and by running the app headless: on attempt 2 with secret 50, guessing 9 now says "Go HIGHER!".
- **Suggestion I did not accept as written:** The existing `try/except TypeError` fallback in `check_guess` could have been patched to convert types safely. I removed it instead and made the caller always pass an int. A fallback that silently changes types hides bugs and is harder to read. I verified by re-running pytest (6 passed) and the headless app run. Also, the starter tests compared the whole `(outcome, message)` tuple to a string, so I changed them to unpack the outcome rather than change `check_guess`'s return shape.

---

## 3. Debugging and testing your fixes

- **Deciding a bug was fixed:** a failing test turned green, then I confirmed the same behavior in the running app.
- **Tests:** `pytest` runs 6 tests, all passing. `test_too_high_hint_says_lower` and `test_too_low_hint_says_higher` cover the backwards hints. `test_numeric_comparison_not_string` covers the string bug. The three starter tests were fixed to unpack the `(outcome, message)` tuple. Streamlit's `AppTest` ran the app headless with secret 50: guesses 60, 9, 40 gave LOWER, HIGHER, HIGHER, with no exceptions.
- **AI help:** Claude wrote the tests and spotted that the starter tests could never pass because of the tuple return.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
