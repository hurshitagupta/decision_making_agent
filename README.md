# Decision Making in Code

## Project Overview

This project implements a weighted decision-making system that evaluates multiple options, ranks them based on predefined criteria, and makes explainable decisions.

The system uses minimum score thresholds and tie margins to determine whether to select an option, reject all options, or request human intervention.

The project also includes sensitivity analysis, decision logging, and a practical laptop-selection example.

## Project Structure

```text
decision_making/
│
├── weighted_scoring.py
├── decision_rules.py
├── sensitivity_test.py
├── decision_log.py
├── real_choice.py
│
├── tests/
│   ├── test_weighted_scoring.py
│   ├── test_decision_rules.py
│   ├── test_sensitivity_test.py
│   ├── test_decision_log.py
│   └── test_real_choice.py
│
├── outputs/
│   ├── sensitivity_table.csv
│   ├── sensitivity_conclusion.txt
│   ├── decision_log.jsonl
│   ├── laptop_decision.json
│   └── pytest_output.txt
│
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.11 or newer
- pytest

Install dependencies:

```bash
pip install -r requirements.txt
```

**requirements.txt**

```text
pytest
```

No API keys or external LLM services are required.

## Implementation

### Task 1 — Weighted Scoring

**File:** `weighted_scoring.py`

- Defines options and their criterion scores.
- Uses weights that sum to 1.
- Calculates weighted scores for each option.
- Validates missing criteria, invalid weights, and score ranges.
- Limits the number of options to 10.

Run:

```bash
python weighted_scoring.py
```

### Task 2 — Decision Rules

**File:** `decision_rules.py`

Implements three decision outcomes:

| Outcome | Condition |
|---|---|
| choose | Best option passes the minimum score and tie margin |
| reject_all | All options score below the minimum |
| ask_human | Top two scores are too close |

Every decision includes the ranking, selected option (if applicable), and reason.

Run:

```bash
python decision_rules.py
```

### Task 3 — Sensitivity Analysis

**File:** `sensitivity_test.py`

- Changes one weight at a time.
- Redistributes the remaining weights proportionally.
- Recalculates scores and identifies changes in the highest-ranked option.
- Limits sensitivity scenarios to 20.

Generated outputs:

- `outputs/sensitivity_table.csv`
- `outputs/sensitivity_conclusion.txt`

Run:

```bash
python sensitivity_test.py
```

### Task 4 — Decision Logging

**File:** `decision_log.py`

Records decisions in JSON-lines format.

Each record contains:

- UTC timestamp
- Decision outcome
- Selected option
- Full ranking
- Decision reason

The log uses append mode and has a maximum limit of 100 records.

Generated output:

`outputs/decision_log.jsonl`

Run:

```bash
python decision_log.py
```

### Task 5 — Real-World Decision

**File:** `real_choice.py`

Applies the weighted decision-making approach to selecting a laptop for software development.

Four laptop options are evaluated using the following criteria:

| Criterion | Weight | Reason |
|---|---:|---|
| Performance | 40% | Important for development tasks |
| Cost | 30% | Maintains affordability |
| Battery | 20% | Supports working without charging |
| Portability | 10% | Useful for travel |

The example uses illustrative scores rather than actual product benchmarks.

**Final result:**

| Laptop | Weighted Score |
|---|---:|
| Laptop A | 8.3 |
| Laptop B | 7.7 |
| Laptop C | 7.7 |
| Laptop D | 6.9 |

- Minimum score: 7.0
- Tie margin: 0.3
- Outcome: `choose`
- Selected option: `Laptop A`

Laptop A is selected because it meets the minimum score and has a sufficient lead over the other options.

Generated output:

`outputs/laptop_decision.json`

Run:

```bash
python real_choice.py
```

## Testing

Each task includes pytest tests covering normal execution, validation, error handling, and decision outcomes.

Run all tests:

```bash
pytest tests/ -v
```

Run an individual task's tests:

```bash
pytest tests/test_weighted_scoring.py -v
pytest tests/test_decision_rules.py -v
pytest tests/test_sensitivity_analysis.py -v
pytest tests/test_decision_log.py -v
pytest tests/test_real_choice.py -v
```

## Guardrails and Error Handling

The implementation includes:

- **Input validation:** Rejects missing criteria, invalid scores, and incorrect weights.
- **Execution limits:** Restricts option counts, sensitivity scenarios, and log entries.
- **Safe stopping:** Every valid decision produces a terminal outcome.
- **Human review:** Requests human intervention when scores are too close.
- **Error handling:** Raises clear exceptions for invalid input and logging failures.
- **Deterministic behaviour:** Uses fixed inputs and calculations for repeatable results.
- **Safe execution:** Does not execute untrusted inputs using `eval()` or `exec()`.
- **Secret hygiene:** No API keys or credentials are used.

## Evidence

The `outputs/` folder contains the generated evidence.

| File | Description |
|---|---|
| sensitivity_table.csv | Results of weight adjustments |
| sensitivity_conclusion.txt | Two-sentence sensitivity conclusion |
| decision_log.jsonl | Timestamped decision records |
| laptop_decision.json | Laptop options, criteria, ranking, and final decision |
| pytest_output.txt | Automated test results |
