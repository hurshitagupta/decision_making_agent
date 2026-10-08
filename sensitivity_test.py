import csv
from pathlib import Path
from weighted_scoring import Option, WEIGHTS, total
from decision_rules import decide

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

MAX_SCENARIOS = 20

def change_weight(weights: dict[str, float], criterion: str, new_weight: float) -> dict[str, float]:
    """Change one weight and redistribute the remaining weights."""

    if criterion not in weights:
        raise ValueError(f"Unknown criterion: {criterion}")

    if not 0 <= new_weight <= 1:
        raise ValueError("Weight must be between 0 and 1")

    remaining = 1 - new_weight
    other_total = sum(weight for name, weight in weights.items() if name != criterion)

    if other_total == 0 and remaining > 0:
        raise ValueError("Cannot redistribute weights")

    updated = {}

    for name, weight in weights.items():
        if name == criterion:
            updated[name] = new_weight
        else:
            updated[name] = (weight / other_total * remaining if other_total > 0 else 0.0)

    return updated

def analyze_sensitivity(options: list[Option], changes: list[tuple[str, float]]) -> list[dict]:

    if not options:
        raise ValueError("At least one option is required")

    if len(changes) > MAX_SCENARIOS:
        raise ValueError("Too many sensitivity scenarios")

    # Baseline decision from Task 2
    baseline = decide(options)
    baseline_winner = baseline.selected

    results = []

    for criterion, new_weight in changes:
        updated_weights = change_weight(WEIGHTS, criterion, new_weight)

        # Score using the new weights
        scores = [(total(option, updated_weights), option.name) for option in options]

        ranking = sorted(scores, key=lambda item: (-item[0], item[1]))

        winner = ranking[0][1]
        winner_score = ranking[0][0]

        results.append({
            "criterion": criterion,
            "new_weight": new_weight,
            "winner": winner,
            "winner_score": winner_score,
            "winner_changed": winner != baseline_winner
        })

    return results

def save_results(results: list[dict]) -> None:
    file_path = OUTPUT_DIR / "sensitivity_table.csv"

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["criterion", "new_weight", "winner", "winner_score", "winner_changed"])
        writer.writeheader()
        writer.writerows(results)

def save_conclusion(results: list[dict]) -> str:
    changed = [result for result in results if result["winner_changed"]]

    if changed:
        conclusion = "The sensitivity analysis shows that changing criterion weights can change the highest-scoring vendor. Therefore, weight selection should reflect the actual decision priorities."
        
    else:
        conclusion = "The highest-scoring vendor remained unchanged across all tested weight adjustments. This suggests that the ranking is stable within the tested scenarios."

    path = OUTPUT_DIR / "sensitivity_conclusion.txt"
    path.write_text(conclusion, encoding="utf-8")

    return conclusion

if __name__ == "__main__":

    options = [
        Option("vendor_a", {"cost": 8, "speed": 6, "risk": 7}),
        Option("vendor_b", {"cost": 5, "speed": 9, "risk": 6}),
        Option("vendor_c", {"cost": 3, "speed": 4, "risk": 4}),
    ]

    changes = [("cost", 0.2), ("cost", 0.6),
        ("speed", 0.2), ("speed", 0.6),
        ("risk", 0.2), ("risk", 0.6)]

    results = analyze_sensitivity(options, changes)

    print("Sensitivity Analysis")
    print("-" * 65)

    for result in results:
        print(result)

    save_results(results)

    print("\nConclusion:")
    print(save_conclusion(results))
