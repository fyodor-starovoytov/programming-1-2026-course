from pathlib import Path
import random
import math

from nltk import data

import logic_weighting


base = Path(__file__).resolve().parent.parent / "data" / "injection.txt"

def utility_loss(decoy, session):
    """ul(Xx, Xy) = 1.0 - sim(Xx, Xy), using the most similar original search."""
    return 1.0 - max((logic_weighting.similarity(decoy, s) for s in session), default=0.0)

def search_injection(session, threshold=0.3, threshhold2 = 0.7 ):
    """Return n decoy searches if the session is risky, else an empty list."""
    prob = logic_weighting.privacy_probability(session, pii_seen=False)
    if prob >= threshhold2:
        return []
    if prob >= threshold:
        with open(base, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        ranked = sorted(lines, key=lambda d: utility_loss(d, session))
        pool = ranked[:max(1, len(session))]
        avg_ul = sum(utility_loss(d, session) for d in pool) / len(pool)

        n = max(1, math.ceil(len(session) * (1.0 - avg_ul)))
        return pool[:min(n, len(pool))]


    with open(base, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    ranked = sorted(lines, key=lambda d: utility_loss(d, session))
    pool = ranked[:max(1, len(session))]
    avg_ul = sum(utility_loss(d, session) for d in pool) / len(pool)

    n = max(1, math.ceil(len(session) * (1.0 - avg_ul)))
    return pool[:max(n, len(pool))]

def inject_searches(session):
    """Mix decoys randomly into the session and save to a new file."""
    decoys = search_injection(session)
    if not decoys:
        print("Privacy score is fine, nothing injected.")
        return None

    mixed = list(session)
    for search in decoys:
        mixed.insert(random.randint(0, len(mixed)), search)

    target_path = Path(base.parent.parent / "input_data" / "data")
    out_path = target_path.with_name(f"{target_path.stem}_injected{target_path.suffix}")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(mixed) + "\n")

    for search in decoys:
        print(f"Injected search: {search}")
    print(f"Saved to: {out_path}")
    return out_path

