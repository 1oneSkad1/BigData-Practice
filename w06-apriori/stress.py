"""Controlled extension: stop counting at a measured allocation budget.

This is an artificial experiment budget, never a claim of host RAM exhaustion.
The supplied bench.py and its standard data are unchanged.
"""
from bisect import bisect
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import random
import time
import tracemalloc


def main():
    rng = random.Random(246)
    item_count, basket_count, basket_size = 20_000, 40_000, 40
    total = 0.0
    cumulative = []
    for i in range(item_count):
        total += 1 / (i + 1) ** 0.8
        cumulative.append(total)
    baskets = [{bisect(cumulative, rng.random() * total) for _ in range(basket_size)}
               for _ in range(basket_count)]
    budget = 256 * 1024**2
    rows = []
    for support in (400, 200, 100, 50, 25, 12, 6, 3, 1):
        tracemalloc.start()
        start = time.perf_counter()
        singles = Counter(item for b in baskets for item in b)
        frequent = {i for i, c in singles.items() if c >= support}
        counts = Counter()
        reason = "completed"
        processed = 0
        for processed, basket in enumerate(baskets, 1):
            counts.update(combinations(sorted(basket & frequent), 2))
            if processed % 100 == 0:
                _, peak = tracemalloc.get_traced_memory()
                if peak >= budget:
                    reason = "stopped at artificial 256 MiB allocation budget"
                    break
                if time.perf_counter() - start >= 30:
                    reason = "stopped at artificial 30 second counting budget"
                    break
        _, peak = tracemalloc.get_traced_memory()
        row = {"support": support, "processed_baskets": processed,
               "peak_counters": len(counts), "peak_bytes": peak,
               "seconds": time.perf_counter()-start, "status": reason,
               "frequent_pairs": sum(c >= support for c in counts.values()) if reason == "completed" else None}
        tracemalloc.stop()
        rows.append(row)
        print(row, flush=True)
        del counts
        if reason != "completed":
            break
    (Path(__file__).resolve().parent / 'out/stress.json').write_text(json.dumps({
        "seed":246, "items":item_count, "baskets":basket_count,
        "draws_per_basket":basket_size, "memory_budget_bytes":budget,
        "time_budget_seconds":30, "runs":rows,
        "note":"Expanded data; a controlled budget stop is not physical RAM exhaustion. Basket storage is outside tracing."
    }, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
