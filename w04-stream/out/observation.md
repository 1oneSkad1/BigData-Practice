# Week 4 · Mining Data Streams

## Task 1

- Bloom never clears inserted bits, preventing false negatives; predicted/measured false positives were 0.860%/0.840% (sampling variation). Reservoir uses `randrange(i + 1) < k` for uniform k/n inclusion with only k stored items.
- Stochastic FM combines grouped geometric means by their median, scaled by 64/1.526: 16,620 versus 19,953 true; raw mean/median gave 51,776/16,384. The fixed damping is heuristic.

## Task 2

- At 25 million items, exact counting took 44.28s and 744.7MB, exceeding my 30s waiting budget; time, rather than RAM exhaustion, stopped the experiment.
- Exact memory grew O(n), while FM stayed near 4KB, O(1); accuracy did not improve consistently. Factor-two estimates suit rough traffic sizing, but not billing; see `limits.md` for measurements and machine details.

## Task 3

- Minimizing `(1-exp(-kn/m))^k` gives `k*=(m/n)ln 2≈7` and a 0.8193% floor at 10 bits/item. Measured false positives fell from 9.511% to 0.897%, with zero false negatives and 80,000 retained bits including object overhead.
- With unknown n, monitor saturation and add scalable Bloom layers if memory permits: guessing low increases false positives, while guessing high wastes space. Unlimited insertions cannot retain low error under a fixed budget.
