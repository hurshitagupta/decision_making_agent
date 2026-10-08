import pytest
from weighted_scoring import Option, WEIGHTS
from sensitivity_test import change_weight, analyze_sensitivity, save_results, save_conclusion

@pytest.fixture
def vendors():
    return [
        Option("vendor_a", {"cost": 8, "speed": 6, "risk": 7}),
        Option("vendor_b", {"cost": 5, "speed": 9, "risk": 6}),
        Option("vendor_c", {"cost": 3, "speed": 4, "risk": 4})
    ]

def test_weights_sum_to_one():
    updated = change_weight(WEIGHTS, "cost", 0.6)
    assert sum(updated.values()) == pytest.approx(1.0)
    assert updated["cost"] == pytest.approx(0.6)

def test_other_weights_redistributed():
    updated = change_weight(WEIGHTS, "speed", 0.6)
    assert updated["speed"] == pytest.approx(0.6)
    assert sum(updated.values()) == pytest.approx(1.0)

def test_winner_changes(vendors):
    results = analyze_sensitivity(vendors, [("speed", 0.6)])
    assert results[0]["winner"] == "vendor_b"
    assert results[0]["winner_changed"] is True

def test_winner_remains_same(vendors):
    results = analyze_sensitivity(vendors, [("cost", 0.6)])

    assert results[0]["winner"] == "vendor_a"
    assert results[0]["winner_changed"] is False

def test_invalid_criterion():
    with pytest.raises(ValueError, match="Unknown criterion"):
        change_weight(WEIGHTS, "quality", 0.5)

def test_invalid_weight():
    with pytest.raises(ValueError, match="between 0 and 1"):
        change_weight(WEIGHTS, "cost", 1.5)

def test_scenario_limit(vendors):
    changes = [("cost", 0.5)] * 21

    with pytest.raises(ValueError, match="Too many"):
        analyze_sensitivity(vendors, changes)

def test_empty_options():
    with pytest.raises(ValueError, match="At least one"):
        analyze_sensitivity([], [("cost", 0.5)])

def test_saved_outputs(vendors, tmp_path, monkeypatch):
    import sensitivity_test

    monkeypatch.setattr(sensitivity_test, "OUTPUT_DIR", tmp_path)

    results = analyze_sensitivity(vendors, [("speed", 0.6)])

    save_results(results)
    save_conclusion(results)

    assert (tmp_path / "sensitivity_table.csv").exists()
    assert (tmp_path / "sensitivity_conclusion.txt").exists()

    content = (tmp_path / "sensitivity_table.csv").read_text(encoding="utf-8")

    assert "vendor_b" in content
