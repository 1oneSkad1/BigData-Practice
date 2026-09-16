#!/usr/bin/env python3
"""Week 3 · Task 3 — Find the same pairs without comparing everything.

Textbook §3.4.

`BruteForce` compares every pair. On 3,000 documents that is 4.5 million
comparisons and it is completely correct. On 3 million documents it is 4.5
trillion and it is completely useless.

Beat it. Find the same near-duplicate pairs while making far fewer comparisons.

    python3 bench.py
    python3 bench.py --yours

The harness counts every call you make to `similarity()`. That is your score.
It also checks **recall** - which of the truly similar pairs you found. Skipping
comparisons is easy; skipping comparisons without losing the pairs is the task.
"""

from collections import defaultdict


class BruteForce:
    """Correct, and quadratic."""

    def __init__(self, threshold):
        self.threshold = threshold

    def find(self, docs, similarity):
        """docs is [set_of_shingles, ...]. Return {(i, j), ...} with i < j."""
        out = set()
        for i in range(len(docs)):
            for j in range(i + 1, len(docs)):
                if similarity(docs[i], docs[j]) >= self.threshold:
                    out.add((i, j))
        return out


class YourFinder:
    """Your near-duplicate finder.

        __init__(threshold)
        find(docs, similarity) -> {(i, j), ...}

    `similarity(a, b)` is the only way to compare two documents, and every call
    is counted. Everything else - signatures, banding, bucketing - is free, in
    the sense that the harness does not charge you for it. That is deliberate:
    it is also roughly true at scale, where the comparison is the expensive
    part and the hashing is linear.

    Two knobs decide everything:

        the number of hashes in a signature
        how many bands you split it into

    §3.4.2 gives you the relationship between those and the probability that a
    pair at similarity s becomes a candidate. It is an S-curve, and where its
    step sits is something you choose. Choose it on purpose and be able to say
    why in observation.md - a threshold of 0.8 does not mean bands should be
    anything in particular until you have done the arithmetic.

    You may reuse your Task 1 code.
    """

    def __init__(self, threshold):
        self.threshold = threshold
        # 120 hashes in 30 bands of four rows: the S-curve step is about .427.
        # Spread coefficients over the full prime range.  Small consecutive
        # coefficients make the small integer shingles nearly monotonic,
        # which is not an independent minhash family.
        self.hashes = [
            ((1_103_515_245 * (i + 1) + 12_345) % 4_294_967_311,
             (2_147_483_647 * (i + 1) + 97_531) % 4_294_967_311)
            for i in range(120)
        ]
        self.bands = 30
        self.prime = 4_294_967_311

    def find(self, docs, similarity):
        # Minhash signatures are built directly from the document shingles.
        # The following arithmetic hashes are deterministic, avoiding a
        # process-randomized Python hash and making benchmark results stable.
        signatures = []
        for doc in docs:
            signatures.append([
                min((a * shingle + b) % self.prime for shingle in doc)
                if doc else self.prime
                for a, b in self.hashes
            ])

        rows_per_band = len(self.hashes) // self.bands
        candidates = set()
        for band in range(self.bands):
            buckets = defaultdict(list)
            start = band * rows_per_band
            end = start + rows_per_band
            for index, signature in enumerate(signatures):
                buckets[tuple(signature[start:end])].append(index)
            for bucket in buckets.values():
                for offset, left in enumerate(bucket):
                    for right in bucket[offset + 1:]:
                        candidates.add((left, right))

        return {(i, j) for i, j in candidates
                if similarity(docs[i], docs[j]) >= self.threshold}
