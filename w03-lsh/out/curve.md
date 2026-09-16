# Crossover measurement

Measured on Windows 11 (10.0.26200), AMD64 Family 25 Model 97 (AuthenticAMD),
Python 3.12.14.  This was run in the Codex desktop runtime; the runtime does
not expose the host RAM to this process, and no other deliberately started
workloads were running.

| documents | brute force | LSH | brute peak | LSH peak |
| ---: | ---: | ---: | ---: | ---: |
| 125 | 0.034 s | 0.917 s | 6.6 KiB | 632.6 KiB |
| 250 | 0.120 s | 1.786 s | 7.2 KiB | 1.22 MiB |
| 500 | 0.493 s | 3.640 s | 7.9 KiB | 2.45 MiB |
| 1,000 | 2.015 s | 7.321 s | 10.4 KiB | 4.93 MiB |
| 2,000 | 8.445 s | 14.749 s | 20.9 KiB | 9.98 MiB |
| 4,000 | 34.930 s | 29.313 s | 39.9 KiB | 20.55 MiB |

The brute-force time ratios while doubling `n` were 3.51x, 4.09x, 4.09x, 4.19x,
and 4.14x.  Apart from the smallest measurement's fixed overhead, that is the
expected quadratic curve.  LSH was approximately linear here: 1.95x, 2.04x,
2.01x, 2.01x, and 1.99x.

The time crossover lies between 2,000 and 4,000 documents: at 4,000 LSH took
29.31 s versus brute force's 34.93 s.  The full 4,000-document measurement
took 64.24 s for both methods, which is the first genuinely unpleasant
minute-long wait.  LSH nevertheless reduced comparisons from 7,998,000 to
6,090 (99.92%).  At small sizes it loses because it must compute 120 minhash
values per document, construct 30 band keys, and maintain buckets before it
can skip even one comparison.
