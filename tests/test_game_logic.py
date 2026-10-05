from logic_utils import check_guess, get_range_for_difficulty, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


def test_too_high_hint_says_lower():
    _, message = check_guess(60, 50)
    assert "LOWER" in message

def test_too_low_hint_says_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message

def test_numeric_comparison_not_string():
    # "9" > "50" as strings; as ints 9 is Too Low
    outcome, _ = check_guess(9, 50)
    assert outcome == "Too Low"


def test_range_matches_difficulty():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 50)


# --- Edge cases for parse_guess ---

def test_negative_guess_rejected_when_out_of_range():
    ok, value, err = parse_guess("-5", 1, 100)
    assert not ok and value is None and "between 1 and 100" in err


def test_negative_guess_parses_without_range():
    assert parse_guess("-5") == (True, -5, None)


def test_zero_and_above_high_rejected():
    assert parse_guess("0", 1, 20)[0] is False
    assert parse_guess("21", 1, 20)[0] is False
    assert parse_guess("1", 1, 20)[0] is True
    assert parse_guess("20", 1, 20)[0] is True


def test_decimal_guess_truncated_toward_zero():
    assert parse_guess("3.7", 1, 100) == (True, 3, None)
    # -0.5 truncates to 0, which is then out of range
    assert parse_guess("-0.5", 1, 100)[0] is False


def test_huge_number_rejected_without_crashing():
    ok, value, _ = parse_guess("9" * 30, 1, 100)
    assert not ok and value is None


def test_non_numeric_and_special_inputs_do_not_crash():
    for raw in ["nan", "inf", "1e5", "abc", " ", "1,000", "9" * 400 + ".0"]:
        assert parse_guess(raw, 1, 100)[0] is False


def test_blank_and_none_ask_for_a_guess():
    assert parse_guess("") == (False, None, "Enter a guess.")
    assert parse_guess(None) == (False, None, "Enter a guess.")


def test_whitespace_around_number_is_accepted():
    assert parse_guess("  7 ", 1, 100) == (True, 7, None)
