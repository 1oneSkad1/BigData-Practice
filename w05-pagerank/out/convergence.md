# Task 2 - PageRank Convergence Experiments

## Method and reproduction

The supplied task2_convergence.py measured the Task 1 implementation. bench.py was unchanged, and graphs used seed 246. Each condition was measured once. Timing covers the pagerank call, excluding graph generation and top-10 sorting. All 17 runs stopped after 7-25 iterations, below the limit of 500.

Prediction before measurement: increasing beta or tightening tol should increase iteration counts. Increasing graph size should increase work per iteration without necessarily increasing the iteration count proportionally.

```powershell
python task2_convergence.py --betas 0.5,0.7,0.85,0.95,0.99
python task2_convergence.py --nodes 20000 --betas 0.5,0.7,0.85,0.95,0.99
foreach ($tolerance in @('1e-3','1e-4','1e-5','1e-6','1e-7','1e-8','1e-9')) {
    python task2_convergence.py --tol $tolerance --betas 0.85
}
```

Runs are appended to convergence.json; repeating these commands adds records.

## A1-A3: Beta and convergence

Tolerance was fixed at 1e-10.

| beta | Iterations: 1,200 nodes | Seconds | Iterations: 20,000 nodes | Seconds |
|---:|---:|---:|---:|---:|
| 0.50 | 14 | 0.012793 | 14 | 0.398900 |
| 0.70 | 17 | 0.016304 | 18 | 0.468928 |
| 0.85 | 20 | 0.019232 | 21 | 0.515470 |
| 0.95 | 23 | 0.022834 | 24 | 0.648251 |
| 0.99 | 24 | 0.025150 | 25 | 0.529242 |

Iteration counts increased with beta. Less teleportation allows differences in rank to persist longer through links. However, these graphs converged in 24-25 iterations even at beta=0.99; no dramatic blow-up was observed.

For the transition matrix M with dangling-node redistribution, differences propagate through beta*M. Beta bounds the worst-case L1 contraction factor, but actual convergence also depends on graph structure and the initial vector. Beta alone does not determine the exact iteration count.

## A4: Graph size, iteration count, and time

Node count increased by about 16.67 times, from 1,200 to 20,000. At a fixed beta, the iteration count increased by only zero or one. At beta=0.85, iterations rose from 20 to 21 (1.05 times), while time rose from 0.019232 to 0.515470 seconds (about 26.80 times).

Iteration count depends on convergence behavior; time also depends on the nodes and edges processed in each iteration. The adjacency-list implementation costs O(N+E) per iteration. Larger graphs can therefore take much longer even with similar iteration counts. Generated graph structure also changes with size, so this is not an experiment that isolates node count alone.

These are single-run timings affected by system load, CPU state, and caches. At 20,000 nodes, beta=0.99 took less time than 0.95 despite using more iterations. Fine timing differences and the 26.80-times ratio should not be treated as universal performance laws.

## A5: Tolerance and cost per extra digit

Node count was 1,200 and beta was 0.85. Tolerance bounds the L1 change between successive vectors, not directly the error relative to the exact stationary vector.

| tol | Iterations | Additional iterations |
|---:|---:|---:|
| 1e-3 | 7 | - |
| 1e-4 | 9 | 2 |
| 1e-5 | 10 | 1 |
| 1e-6 | 12 | 2 |
| 1e-7 | 14 | 2 |
| 1e-8 | 16 | 2 |
| 1e-9 | 18 | 2 |
| 1e-10 | 20 | 2 |

Each extra decimal digit cost one or two iterations, averaging (20-7)/7 = approximately 1.86 iterations per digit. Tightening from 1e-6 to 1e-10 cost eight iterations for four digits. Approximately geometric decay explains the roughly constant cost per digit for this graph and beta.

## A6: Top-10 ranking stability

At tol=1e-10, both graph sizes produced the following rankings.

| Position | beta=0.5 | beta=0.7, 0.85, 0.95, 0.99 |
|---:|---|---|
| 1 | p00009 | p00009 |
| 2 | p00001 | p00001 |
| 3 | p00006 | p00006 |
| 4 | p00005 | p00005 |
| 5 | p00003 | p00003 |
| 6 | p00002 | p00002 |
| 7 | p00000 | p00004 |
| 8 | p00004 | p00000 |
| 9 | p00007 | p00007 |
| 10 | p00008 | p00008 |

The first tested beta with a changed order was 0.7: positions seven and eight swapped. Top-10 membership and the top-ranked node remained unchanged. Values between 0.5 and 0.7 were not sampled, so 0.7 is not claimed as the exact crossing point.

Membership was stable, but detailed order depended on beta. Published rankings should report beta and sensitivity to parameter changes rather than treating every position as independent of modeling choices.

## A7: Machine and measurement conditions

- Date: 2026-09-30 (Asia/Seoul).
- CPU: Intel Core Ultra 5 228V; 8 physical cores and 8 logical processors.
- RAM reported by Windows: 33,834,090,496 bytes, approximately 31.51 GiB.
- OS: Windows 11, build 26200.
- Python: 3.14.3.
- A process snapshot immediately after measurement showed ChatGPT, Chrome, Microsoft Edge, Node, MySQL, and Windows background services. Their CPU utilization during experiments was not measured.

Raw results are stored in convergence.json. These timings are observations from this environment, not averages from repeated trials on an idle machine.
