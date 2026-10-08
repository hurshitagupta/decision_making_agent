import pytest
from weighted_scoring import Option
from decision_rules import decide

@pytest.fixture
def vendors():
    return [
        Option("vendor_a", {"cost": 8, "speed": 6, "risk": 7}),
        Option("vendor_b", {"cost": 5, "speed": 9, "risk": 6}),
        Option("vendor_c", {"cost": 3, "speed": 4, "risk": 4}),
    ]

def test_choose_winner(vendors):
    result = decide(vendors)

    assert result.outcome == "choose"
    assert result.selected == "vendor_a"
    assert result.ranking[0] == (7.1, "vendor_a")
    assert result.reason

def test_reject_all(vendors):
    result = decide(vendors, min_score=9.0)

    assert result.outcome == "reject_all"
    assert result.selected is None
    assert len(result.ranking) == 3
    assert result.reason

def test_ask_human(vendors):
    result = decide(vendors, margin=0.8)

    assert result.outcome == "ask_human"
    assert result.selected is None
    assert result.reason

def test_exact_minimum_score():
    options = [Option("vendor_a", {"cost": 6, "speed": 6, "risk": 6})]
    result = decide(options, min_score=6.0)

    assert result.outcome == "choose"
    assert result.selected == "vendor_a"

def test_exact_margin(vendors):
    result = decide(vendors, margin=0.6)

    assert result.outcome == "choose"

def test_invalid_min_score(vendors):
    with pytest.raises(ValueError, match="min_score"):
        decide(vendors, min_score=11)

def test_invalid_margin(vendors):
    with pytest.raises(ValueError, match="margin"):
        decide(vendors, margin=-1)

def test_empty_options():
    with pytest.raises(ValueError, match="At least one"):
        decide([])

def test_option_limit():
    options = [Option(f"vendor_{i}", { "cost": 8, "speed": 6, "risk": 7})
              for i in range(11)]

    with pytest.raises(ValueError, match="Maximum"):
        decide(options)

def test_ranking_and_reason_always_present(vendors):
    results = [decide(vendors), decide(vendors, min_score=9), decide(vendors, margin=0.8)]

    for result in results:
        assert result.ranking
        assert result.reason
