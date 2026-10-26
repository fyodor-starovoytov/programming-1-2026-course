import re
from pathlib import Path
from tqdm import tqdm

def load(path):
    """ Opens a keyword file and turns it into a list. It reads one line at a time,
        strips spaces, lowercases it, and skips empty lines."""
    with open(path, encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

SENSITIVE      = load(Path(__file__).resolve().parent.parent / "data" /"keywords_sensitive.txt")
VERY_SENSITIVE = load(Path(__file__).resolve().parent.parent / "data" / "keywords_very_sensitive.txt")

def contains(text, keywords):
    '''Checks if the text contains any keywords '''
    text = text.lower()
    return any(re.search(rf"\b{re.escape(k)}\b", text) for k in keywords)

def level_score(text):
    """
    Turns one search into a risk number. It checks the very sensitive list first and returns 0.2.
    If nothing matches there, it checks the sensitive list and returns 0.6. Otherwise it returns 1.0, meaning no risk. 
    Lower means riskier."""
    if contains(text, VERY_SENSITIVE): return 0.2
    if contains(text, SENSITIVE):      return 0.6
    return 1.0

def privacy_probability(session, pii_seen=False):
    """ 
    Gives overall probability score for the searches. It is based on equation no.2 in the paper. 
    Start with the personal-info prior, 0.5 if the user has already revealed personal details and 1.0 if not.
    For each search, multiply in its level_score
    Multiply in a history penalty that shrinks as the user repeats sensitive searches.
    This is from the paper’s uniformity idea: the more you return to a topic, the more it says about you.
    """
    prob = 0.5 if pii_seen else 1.0              # linkability prior
    sensitive_hits = 0
    for query in tqdm(session,  desc="Loading"):
        score = level_score(query)
        if score < 1.0:
            sensitive_hits += 1
        history = 1 / (1 + max(0, sensitive_hits - 1))  
        prob *= score * history
    return prob

def similarity(a, b):                            
    """
    Measures how close in meaning two searches are, from 0 (nothing in common) to 1 (identical).
    It compares the sets of words in each. 
    The score is the number of shared words divided by the number of different words overall. 
    
    """
    a, b = set(a.lower().split()), set(b.lower().split())
    return len(a & b) / len(a | b) if a | b else 0.0
