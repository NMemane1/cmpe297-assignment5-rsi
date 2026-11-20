# Method 1: AIDE — AI Development Environment

## Overview

AIDE implements a Recursive Self-Improvement loop for **code optimisation**.  Given an initial (naive) implementation of a function the system iteratively:

1. **Benchmarks** the current code (wall-clock time, peak memory)
2. **Analyses** the code for optimisation opportunities
3. **Generates** an improved version
4. **Tests** the new version for correctness and speed
5. **Keeps** the better version and repeats

In this demonstration the analysis and generation steps walk a predefined "version ladder" so the demo is fully reproducible without an LLM API key.  In production, these steps would call a code-generation model.

## Problems

| # | Problem | Start | End | Speedup |
|---|---------|-------|-----|---------|
| 1 | Bubble Sort → Tim Sort | O(n²) bubble | Python built-in sort | ~100x+ |
| 2 | Word Frequency Counter | Quadratic .count() | collections.Counter | ~10x+ |
| 3 | Sales Data Aggregation | Triple nested loop | pandas groupby | ~5x+ |
| 4 | Fibonacci | Naive recursion O(2^n) | Matrix exponentiation O(log n) | massive |

## Running

```bash
cd method1_aide
python main.py
```

## Output

The script prints each iteration with:
- Version label and code
- Mean/min execution time
- Peak memory usage
- Percentage improvement and speedup factor
- Final summary table across all problems

## Key RSI Concept

AIDE demonstrates that code quality can be improved through **iterative refinement** — each version builds on insights from the previous one.  The improvement trajectory is measurable (execution time) and verifiable (correctness checks).
