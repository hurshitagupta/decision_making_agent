import json
import pytest
from real_choice import WEIGHTS, select_laptop, save_result

def test_weights_sum_to_one():
    assert sum(WEIGHTS.values()) == pytest.approx(1.0)
    assert len(WEIGHTS) == 4

def test_four_options_ranked():
    result = select_laptop()

    assert len(result["ranking"]) == 4

def test_laptop_scores():
    result = select_laptop()

    scores = {name: score for score, name in result["ranking"]}

    assert scores["Laptop A"] == 8.3
    assert scores["Laptop B"] == 7.7
    assert scores["Laptop C"] == 7.7
    assert scores["Laptop D"] == 6.9

def test_ranking_and_reason():
    result = select_laptop()

    assert result["ranking"]
    assert result["reason"]

def test_clear_winner():
    result = select_laptop()

    assert result["outcome"] == "choose"
    assert result["selected"] == "Laptop A"

def test_saved_report(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = select_laptop()
    path = save_result(result)

    assert path.exists()

    report = json.loads(path.read_text(encoding="utf-8"))

    assert len(report["options"]) == 4
    assert len(report["weights"]) == 4
    assert len(report["weight_justification"]) == 4
    assert report["decision"]["outcome"] == "choose"
    assert report["decision"]["selected"] == "Laptop A"
