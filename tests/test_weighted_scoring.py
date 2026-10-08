import pytest
from weighted_scoring import Option, total, score_options

def test_weighted_score():
    option = Option("vendor_a", {"cost": 8, "speed": 6, "risk": 7})
    assert total(option) == 7.1

def test_invalid_weights():
    option = Option("vendor_a", {"cost": 8, "speed": 6, "risk": 7})
    bad_weights = {"cost": 0.5, "speed": 0.3, "risk": 0.3}

    with pytest.raises(ValueError, match="sum to 1"):
        total(option, bad_weights)

def test_missing_criteria():
    option = Option("vendor_a", {"cost": 8, "speed": 6})

    with pytest.raises(ValueError, match="Missing criteria"):
        total(option)

def test_invalid_score():
    option = Option("vendor_a", {"cost": 12, "speed": 6, "risk": 7})

    with pytest.raises(ValueError, match="Invalid score"):
        total(option)

def test_empty_options():
    with pytest.raises(ValueError, match="At least one"):
        score_options([])

def test_option_limit():
    options = [Option(f"vendor_{i}", {"cost": 8, "speed": 6, "risk": 7}) for i in range(11)]

    with pytest.raises(ValueError, match="Maximum"):
        score_options(options)
