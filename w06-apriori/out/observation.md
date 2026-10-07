# Week 6 Observations

## Task 1 — Apriori and Association Rules
- The top rule, 1468 -> 0, had confidence 0.8387 versus 0.0040 in reverse; its lift of 1.2824 suggests modest association, not strong causal evidence.
- Of 1,999,000 possible pairs, 1,708,476 survived singleton pruning; Apriori actually held 820,259 observed pair counters at support 50.

## Task 2 — Lowering Support
- The standard data completed at support 1 (334.15 MB peak); expanded data stopped at support 50 under an artificial 256 MiB budget, not actual RAM exhaustion.
- Counter growth per halving was 5.54x, 4.67x, then 3.00x; from support 400 to 50, counters grew 77.49x versus 25.69x for answers, then counters saturated below 25.

## Task 3 — PCY and Memory
- Using 1,000,003 buckets to limit collisions preserved exact answers and cut pair counters by 98.4%; bucket storage was 4.00 MB, with a 0.125 MB bitmap retained for pass two.
- Traced peak allocation fell from 107.87 to 4.63 MB, crossing over between 2,000 and 5,000 baskets at support 50; 10,007 buckets eliminated counter savings through collisions (details in experiments.json).
