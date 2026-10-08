import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from weighted_scoring import Option
from decision_rules import decide, Decision

OUTPUT_DIR = Path("outputs")
LOG_FILE = OUTPUT_DIR / "decision_log.jsonl"

MAX_LOG_ENTRIES = 100

def log_decision(result: Decision, log_file: Path = LOG_FILE) -> dict:
    """Append a decision with its ranking, reason and timestamp."""

    log_file = Path(log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    if result.outcome not in {"choose", "reject_all", "ask_human"}:
        raise ValueError("Invalid decision outcome")

    if not result.ranking or not result.reason:
        raise ValueError("Decision must include ranking and reason")

    if log_file.exists():
        with log_file.open("r", encoding="utf-8") as file:
            count = sum(1 for _ in file)

        if count >= MAX_LOG_ENTRIES:
            raise ValueError("Decision log limit reached")

    record = {"timestamp": datetime.now(timezone.utc).isoformat(), **asdict(result)}

    try:
        with log_file.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record) + "\n")
    except OSError as error:
        raise OSError(f"Failed to write decision log: {error}") from error

    return record

def read_logs(log_file: Path = LOG_FILE) -> list[dict]:
    """Read and return saved decision records."""

    log_file = Path(log_file)

    if not log_file.exists():
        raise FileNotFoundError("Decision log does not exist")

    try:
        with log_file.open("r", encoding="utf-8") as file:
            records = [json.loads(line) for line in file if line.strip()]
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Failed to read decision log: {error}") from error

    return records

if __name__ == "__main__":

    options = [
        Option("vendor_a", {"cost": 8, "speed": 6, "risk": 7}),
        Option("vendor_b", {"cost": 5, "speed": 9, "risk": 6}),
        Option("vendor_c", {"cost": 3, "speed": 4, "risk": 4}),
    ]

    decisions = [decide(options), decide(options, min_score=9.0), decide(options, margin=0.8)]

    for result in decisions:
        record = log_decision(result)
        print(f"Logged: {record['outcome']} | Reason: {record['reason']}")

    print("\nSaved Decision Logs:")

    for record in read_logs():
        print(json.dumps(record, indent=2))
