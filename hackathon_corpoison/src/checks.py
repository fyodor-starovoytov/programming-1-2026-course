import logic_weighting as lw
import logic_data_injection as injection

sens = lw.SENSITIVE[0]
very = lw.VERY_SENSITIVE[0]

print("--- logic_weighting ---")
assert lw.level_score("hello world") == 1.0
assert lw.level_score(f"about {sens}") == 0.6
assert lw.level_score(f"about {very}") == 0.2
print("level_score OK")

assert lw.privacy_probability(["hello", "world"]) == 1.0
assert lw.privacy_probability(["hello"], pii_seen=True) == 0.5
assert lw.privacy_probability([very]) < lw.privacy_probability([sens]) < 1.0
print("privacy_probability OK")

assert lw.similarity("a b c", "a b c") == 1.0
assert lw.similarity("a b", "c d") == 0.0
print("similarity OK")

print("--- injection ---")
safe = ["hello", "world"]
risky = [very, very, very, sens]

assert injection.search_injection(safe) == []
decoys = injection.search_injection(risky)
assert len(decoys) > 0
print("search_injection OK:", len(decoys), "decoys")

assert injection.inject_searches(safe) is None
out = injection.inject_searches(risky)
assert out is not None
print("inject_searches OK, wrote", out)

print("\nAll checks passed.")