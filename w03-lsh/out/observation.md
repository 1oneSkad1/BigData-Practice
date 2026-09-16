# Observations

## Task 1

The signature builder makes one sequential pass through rows and updates only
the columns indexed by the current row.  A pass per column would repeatedly
scan an out-of-core matrix, turning sequential I/O into many full reads.  I
reject signature lengths that do not divide evenly by the band count rather
than silently dropping leftover hashes.  S1--S4 estimates as 1.0 with two
hashes although its true Jaccard score is 2/3; using more independent hashes
would narrow the sampling error, at the cost of signature storage and hashing.

## Task 2

On the recorded Windows/AMD64 runtime, crossover was between 2,000 and 4,000
documents: at 4,000, brute force took 34.93 s and LSH 29.31 s.  The brute
doubling ratios through 4,000 were 3.51x, 4.09x, 4.09x, 4.19x, and 4.14x,
consistent with a quadratic curve.  The 4,000-document measurement took 64.24
s in total, the first unpleasant wait; LSH's peak memory was 20.55 MiB.

## Task 3

I used 120 hashes split into 30 bands of 4 rows.  Its nominal S-curve step is
`(1/30)^(1/4) = 0.427`; putting it below the 0.6 threshold favors recall.  At
similarity 0.6 the candidate probability is
`1 - (1 - 0.6^4)^30 = 98.4%`.  The benchmark obtained 97.5% recall while
avoiding 99.92% of comparisons.  Moving the step above the threshold would cut
more candidates but loses recall; on a much larger system hashing itself stops
being free once CPU, memory bandwidth, signature storage, and bucket shuffles
become dominant.
