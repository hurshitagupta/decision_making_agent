from dataclasses import dataclass
from math import isfinite

WEIGHTS = {"cost": 0.4, "speed": 0.3, "risk": 0.3}
MAX_OPTIONS = 10

@dataclass(frozen=True)
class Option:
    name: str
    scores: dict[str, float]

def total(option: Option, weights: dict[str, float] = WEIGHTS) -> float:
    # Validate weights
    if not weights:
        raise ValueError("Weights cannot be empty")

    if any(not isfinite(w) or w < 0 for w in weights.values()):
        raise ValueError("Weights must be finite and non-negative")

    if abs(sum(weights.values()) - 1.0) > 1e-9:
        raise ValueError("Weights must sum to 1")

    # Check required criteria
    missing = set(weights) - set(option.scores)
    if missing:
        raise ValueError(f"Missing criteria: {sorted(missing)}")

    # Validate scores
    for criterion in weights:
        score = option.scores[criterion]
        if not isfinite(score) or not 0 <= score <= 10:
            raise ValueError(f"Invalid score for {criterion}")

    return round(sum(option.scores[c] * w for c, w in weights.items()), 3)

def score_options(options: list[Option]) -> list[tuple[str, float]]:
    if not options:
        raise ValueError("At least one option is required")

    if len(options) > MAX_OPTIONS:
        raise ValueError(f"Maximum {MAX_OPTIONS} options allowed")

    return [(option.name, total(option)) for option in options]

if __name__ == "__main__":
    options = [
        Option("vendor_a", {"cost": 8, "speed": 6, "risk": 7}),
        Option("vendor_b", {"cost": 5, "speed": 9, "risk": 6}),
        Option("vendor_c", {"cost": 3, "speed": 4, "risk": 4}),
    ]

    print("Weights:", WEIGHTS)
    print("Weighted Scores:")

    for name, score in score_options(options):
        print(f"{name}: {score}")
