# AI Interactions

## Challenge 1: Advanced Edge-Case Testing

**Prompts used (Claude Code, agent mode):**
1. "Identify three potential edge-case inputs that might still break the game, then generate pytest cases that verify the game handles them gracefully."
2. "Fix `parse_guess` so the edge cases are handled and wire the range through `app.py`."

Before writing tests, Claude ran `parse_guess` on a batch of odd inputs. Nothing crashed, but out-of-range numbers were accepted as valid guesses (`-5`, `0` and `99999999999999999999999` all returned `ok=True`), and each one used up an attempt and changed the score. Decimals were silently truncated (`-0.5` became `0`).

| Edge case | Why it was chosen |
|-----------|-------------------|
| Negative numbers and zero (`-5`, `0`) | They are never the secret, but the old code accepted them as guesses and charged an attempt. |
| Decimals (`3.7`, `-0.5`) | The code casts with `int(float(raw))`, which truncates silently, so `-0.5` becomes `0`. The test documents this behavior. |
| Huge or special values (`"9" * 30`, `nan`, `inf`, `1e5`, a 400-digit decimal) | Checks that large numbers and float oddities are rejected cleanly rather than raising an `OverflowError` or passing as a guess. |

**Fix:** `parse_guess(raw, low, high)` now takes the difficulty range and returns "Enter a number between low and high." for anything outside it. `app.py` passes `low, high`.

**Verification:** 15 pytest tests pass (output is in the README). A headless Streamlit run with secret 50 showed guesses `-5` and `500` both give the range error with no exceptions.

**Not changed:** `app.py` still increments `attempts` before parsing, so an invalid guess (for example, text) still uses up an attempt.
