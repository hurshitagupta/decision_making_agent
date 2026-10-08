from datetime import datetime
import pytest
from weighted_scoring import Option
from decision_rules import Decision, decide
from decision_log import log_decision, read_logs, MAX_LOG_ENTRIES

@pytest.fixture
def vendors():
    return [
        Option("vendor_a", {"cost": 8, "speed": 6, "risk": 7}),
        Option("vendor_b", {"cost": 5, "speed": 9, "risk": 6}),
        Option("vendor_c", {"cost": 3, "speed": 4, "risk": 4}),
    ]

def test_log_single_decision(vendors, tmp_path):
    log_file = tmp_path / "decisions.jsonl"
    result = decide(vendors)
    record = log_decision(result, log_file)

    assert log_file.exists()
    assert record["outcome"] == "choose"
    assert record["selected"] == "vendor_a"

def test_log_contains_timestamp(vendors, tmp_path):
    log_file = tmp_path / "decisions.jsonl"
    record = log_decision(decide(vendors), log_file)
    timestamp = datetime.fromisoformat(record["timestamp"])

    assert timestamp.tzinfo is not None

def test_three_decisions_logged(vendors, tmp_path):
    log_file = tmp_path / "decisions.jsonl"

    decisions = [decide(vendors), decide(vendors, min_score=9), decide(vendors, margin=0.8)]

    for result in decisions:
        log_decision(result, log_file)

    records = read_logs(log_file)

    assert len(records) == 3

    outcomes = [record["outcome"] for record in records]

    assert outcomes == ["choose", "reject_all", "ask_human"]

def test_ranking_and_reason_saved(vendors, tmp_path):
    log_file = tmp_path / "decisions.jsonl"
    log_decision(decide(vendors), log_file)
    records = read_logs(log_file)

    assert records[0]["ranking"]
    assert records[0]["reason"]

def test_append_does_not_overwrite(vendors, tmp_path):
    log_file = tmp_path / "decisions.jsonl"

    log_decision(decide(vendors), log_file)
    log_decision(decide(vendors, min_score=9), log_file)

    with log_file.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    assert len(lines) == 2

def test_invalid_decision_rejected(tmp_path):
    log_file = tmp_path / "decisions.jsonl"

    invalid = Decision(outcome="unknown", selected=None, ranking=[(7.0, "vendor_a")], reason="Invalid result")

    with pytest.raises(ValueError, match="Invalid decision"):
        log_decision(invalid, log_file)

def test_missing_reason_rejected(tmp_path):
    invalid = Decision(outcome="choose", selected="vendor_a", ranking=[(7.0, "vendor_a")], reason="")

    with pytest.raises(ValueError, match="ranking and reason"):
        log_decision(invalid, tmp_path / "decisions.jsonl")

def test_log_limit(vendors, tmp_path):
    log_file = tmp_path / "decisions.jsonl"
    result = decide(vendors)

    for _ in range(MAX_LOG_ENTRIES):
        log_decision(result, log_file)

    with pytest.raises(ValueError, match="limit reached"):
        log_decision(result, log_file)

def test_corrupted_log_rejected(tmp_path):
    log_file = tmp_path / "decisions.jsonl"
    log_file.write_text("{invalid json}\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Failed to read"):
        read_logs(log_file)

def test_missing_log_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_logs(tmp_path / "missing.jsonl")