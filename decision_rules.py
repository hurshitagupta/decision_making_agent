from dataclasses import dataclass
from math import isfinite
from weighted_scoring import Option, score_options

@dataclass(frozen=True)
class Decision:
    outcome: str
    selected: str | None
    ranking: list[tuple[float, str]]
    reason: str

def decide(options: list[Option], min_score: float = 6.0, margin: float = 0.5) -> Decision:

    # Validate decision settings
    if not isfinite(min_score) or not 0 <= min_score <= 10:
        raise ValueError("min_score must be between 0 and 10")

    if not isfinite(margin) or not 0 <= margin <= 10:
        raise ValueError("margin must be between 0 and 10")

    scored = score_options(options)

    ranking = sorted([(score, name) for name, score in scored],
        key=lambda item: (-item[0], item[1]))

    best_score, best_name = ranking[0]

    # Rule 1: Reject if even the best option is too weak
    if best_score < min_score:
        return Decision(outcome="reject_all", selected=None, ranking=ranking,
            reason="All options are below the minimum score")

    # Rule 2: Ask a human if top scores are too close
    if len(ranking) > 1:
        second_score = ranking[1][0]

        if round(best_score - second_score, 3) < margin:
            return Decision(outcome="ask_human", selected=None, ranking=ranking, reason="Top two options are too close to call")

    # Rule 3: Choose the clear winner
    return Decision(outcome="choose", selected=best_name, ranking=ranking,
        reason=f"{best_name} meets the minimum score and margin")


if __name__ == "__main__":
    options = [
        Option("vendor_a", {"cost": 8, "speed": 6, "risk": 7}),
        Option("vendor_b", {"cost": 5, "speed": 9, "risk": 6}),
        Option("vendor_c", {"cost": 3, "speed": 4, "risk": 4}),
    ]

    print("CASE 1: Clear winner")
    print(decide(options))

    print("\nCASE 2: Reject all")
    print(decide(options, min_score=9.0))

    print("\nCASE 3: Ask human")
    print(decide(options, margin=0.8))
