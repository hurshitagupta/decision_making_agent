import json
from pathlib import Path
from weighted_scoring import Option, total

WEIGHTS = {
    "performance": 0.4,
    "cost": 0.3,
    "battery": 0.2,
    "portability": 0.1
}

MAX_OPTIONS = 10

def select_laptop():
    laptops = [
        Option("Laptop A", {"performance": 9, "cost": 8, "battery": 8, "portability": 7}),
        Option("Laptop B", {"performance": 7, "cost": 9, "battery": 7, "portability": 8}),
        Option("Laptop C", {"performance": 8, "cost": 7, "battery": 9, "portability": 6}),
        Option("Laptop D", {"performance": 6, "cost": 8, "battery": 6, "portability": 9})
    ]

    if not laptops or len(laptops) > MAX_OPTIONS:
        raise ValueError("Number of options must be between 1 and 10")

    ranking = sorted([(total(laptop, WEIGHTS), laptop.name) for laptop in laptops],
        key=lambda item: (-item[0], item[1]))

    min_score = 7.0
    margin = 0.3
    best_score, best_name = ranking[0]

    if best_score < min_score:
        outcome = "reject_all"
        selected = None
        reason = "All laptops are below the minimum score"

    elif len(ranking) > 1 and best_score - ranking[1][0] < margin:
        outcome = "ask_human"
        selected = None
        reason = "Top two laptops have scores too close to call"

    else:
        outcome = "choose"
        selected = best_name
        reason = f"{best_name} is the clear winner"

    return {
        "outcome": outcome,
        "selected": selected,
        "ranking": ranking,
        "reason": reason
    }

def save_result(result):
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    report = {
        "weights": WEIGHTS,
        "weight_justification": {
            "performance": "Important for coding and development",
            "cost": "Helps maintain affordability",
            "battery": "Supports working without charging",
            "portability": "Useful for travel"},
        "options": [
            {"name": "Laptop A", "performance": 9, "cost": 8, "battery": 8, "portability": 7},
            {"name": "Laptop B", "performance": 7, "cost": 9, "battery": 7, "portability": 8},
            {"name": "Laptop C", "performance": 8, "cost": 7, "battery": 9, "portability": 6},
            {"name": "Laptop D", "performance": 6, "cost": 8, "battery": 6, "portability": 9}],
            "decision": result}

    path = output_dir / "laptop_decision.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return path

if __name__ == "__main__":
    result = select_laptop()

    print("Laptop Selection Results")

    for score, name in result["ranking"]:
        print(f"{name}: {score}")

    print("\nOutcome:", result["outcome"])
    print("Selected:", result["selected"])
    print("Reason:", result["reason"])

    print("\nSaved to:", save_result(result))
