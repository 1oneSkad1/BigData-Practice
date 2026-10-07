"""Extra evidence for Task 1 and Task 3; does not modify the benchmark."""
import json
import random
import time
import tracemalloc
from pathlib import Path
import bench
from task1_apriori import frequent_singletons, association_rules, frequent_pairs
from task3_pcy import PlainApriori, YourAlgorithm


def measure(cls, baskets, **options):
    algorithm = cls(50, **options)
    tracemalloc.start()
    started = time.perf_counter()
    pairs = algorithm.run(baskets)
    seconds = time.perf_counter() - started
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return pairs, {"baskets": len(baskets), "peak_counters": algorithm.peak_counters,
                   "peak_bytes": peak, "seconds": seconds,
                   "bucket_count": getattr(algorithm, "bucket_count", 0),
                   "bucket_bytes": getattr(algorithm, "bucket_bytes", 0),
                   "bitmap_bytes": getattr(algorithm, "bitmap_bytes", 0)}


def main():
    baskets = bench.build()
    singles = frequent_singletons(baskets, 50)
    rules = association_rules(baskets, 50, 0)
    pair = frequent_pairs(baskets, 50)
    top = rules[0]
    reverse = next(r for r in rules if r[:2] == (top[1], top[0]))
    evidence = {"task1": {"frequent_items": len(singles),
                          "possible_survivor_pairs": len(singles) * (len(singles)-1)//2,
                          "top_rule": top, "reverse_rule": reverse,
                          "pair_support": pair[frozenset(top[:2])]},
                "bucket_experiments": [], "crossover": []}
    baseline, base_row = measure(PlainApriori, baskets)
    evidence["baseline"] = base_row
    for count in (1_000_003, 100_003, 10_007):
        pairs, row = measure(YourAlgorithm, baskets, bucket_count=count)
        assert pairs == baseline, "Pair counts must also match, not just pair keys"
        row["exact_counts_match"] = True
        evidence["bucket_experiments"].append(row)
        print(row, flush=True)
    for size in (100, 500, 1000, 2000, 5000):
        baseline, base = measure(PlainApriori, baskets[:size])
        pairs, mine = measure(YourAlgorithm, baskets[:size])
        assert pairs == baseline
        evidence["crossover"].append({"baskets": size, "baseline": base, "pcy": mine})
        print("crossover", size, base["peak_bytes"], mine["peak_bytes"], flush=True)
    # Randomized, independent brute force catches counts, duplicate basket items,
    # arbitrary item labels, and repeated use of an algorithm instance.
    rng = random.Random(246)
    for trial in range(50):
        sample = [set(rng.sample(list("abcdefghi"), rng.randrange(0, 8)))
                  for _ in range(rng.randrange(1, 35))]
        support = rng.randrange(1, 8)
        from collections import Counter
        from itertools import combinations
        expected = Counter(frozenset(p) for b in sample for p in combinations(b, 2))
        expected = {p: c for p, c in expected.items() if c >= support}
        algo = YourAlgorithm(support, bucket_count=17)
        assert algo.run(sample) == expected
        assert algo.run(sample) == expected
        assert frequent_pairs(sample, support) == expected
    evidence["randomized_bruteforce_cases"] = 50
    (Path(__file__).resolve().parent / "out/experiments.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
