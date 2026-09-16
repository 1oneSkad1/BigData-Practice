# Big Data Practice

This repository contains my coursework and assignment submissions for the 2026-2 Introduction to Big Data course at Korea University Sejong.

- Student repository: [1oneSkad1/BigData-Practice](https://github.com/1oneSkad1/BigData-Practice)
- Original course repository: [codingchild2424/2026-lecture-bigdata-practice](https://github.com/codingchild2424/2026-lecture-bigdata-practice)
- Main submission artifacts: each week's `out/` directory, especially `out/observation.md`

## Assignment Progress

| Week | Topic | Status | Submission |
|---|---|---|---|
| Week 2 | MapReduce and Spark | Optional | [`w02-mapreduce/`](w02-mapreduce/) |
| Week 3 | Finding Similar Items with MinHash and LSH | In progress | [`w03-lsh/`](w03-lsh/) |
| Week 4 | Mining Data Streams | Not started | [`w04-stream/`](w04-stream/) |
| Week 5 | PageRank and Link Analysis | Not started | [`w05-pagerank/`](w05-pagerank/) |
| Week 6 | Apriori and Frequent Itemsets | Not started | [`w06-apriori/`](w06-apriori/) |
| Week 7 | K-Means Clustering | Not started | [`w07-kmeans/`](w07-kmeans/) |

## Current Assignment: Week 3

The Week 3 assignment focuses on finding similar items efficiently.

- Task 1: implement MinHash signatures and LSH banding from the matrix up.
- Task 2: measure where brute-force comparison and LSH cross over on my machine.
- Task 3: recover the same similar pairs while performing far fewer comparisons.
- Main reflection: [`w03-lsh/out/observation.md`](w03-lsh/out/observation.md)

## Running and Validation

Run the following commands from the Week 3 directory:

```bash
cd w03-lsh
python task1_minhash.py --verify
python task2_crossover.py --sizes 250,500,1000,2000
python bench.py --yours
python test_tasks.py
python ../check.py w03
```

Depending on the local Python installation, `python3` or `py` may be used instead of `python`.

## Repository Workflow

- Base assignment files are synchronized from the original course repository.
- My implementations are written in the corresponding `task*.py` files.
- Generated results and observations are stored in each week's `out/` directory.
- Provided benchmark and test harnesses are left unchanged unless explicitly instructed otherwise.
- Before submission, I run both the weekly tests and the repository-level checker.

## Attribution

The assignment specifications, starter code, test harnesses, and course structure originate from the [course repository](https://github.com/codingchild2424/2026-lecture-bigdata-practice). My implementations, measurements, outputs, and written observations are maintained in this repository for submission.
