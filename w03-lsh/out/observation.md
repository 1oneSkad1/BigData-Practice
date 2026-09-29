# Observations

## Task 1

I read each row once to avoid reading the same data again.
If the hash count does not divide evenly into bands, the code raises an error.
S1 and S4 gave 1.0 instead of 2/3. More hashes could reduce the error but need more time and memory.

## Task 2

I ran this on Windows with an AMD CPU. LSH became faster between 2,000 and 4,000 documents.
At 4,000, brute force took 34.93 seconds and LSH took 29.31 seconds. Doubling from 2,000 made brute force about 4.14 times slower.
Both runs together took about 64 seconds at 4,000, so the wait felt long.

## Task 3

I used 120 hashes and 30 bands. The step is `(1/30)^(1/4) ≈ 0.427`, below 0.6 to miss fewer similar pairs.
It found 97.5% of the similar pairs and skipped 99.92% of comparisons.
A higher step could miss more pairs. With much more data, making the hashes would also take a lot of time.
