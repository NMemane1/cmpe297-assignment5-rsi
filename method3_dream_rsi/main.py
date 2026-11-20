#!/usr/bin/env python3
"""Run the Dream-RSI loop on all base problems."""

from base_problem import ALL_PROBLEMS
from dream_rsi import run_dream_loop


def main():
    print("=" * 70)
    print("  Dream-RSI")
    print("  Recursive Self-Improvement via Synthetic Data Augmentation")
    print("=" * 70)

    summary = []

    for make_problem in ALL_PROBLEMS:
        X, y, label = make_problem()
        log = run_dream_loop(X, y, label)
        baseline = log[0]["accuracy"]
        best = max(e["accuracy"] for e in log)
        best_strat = [e for e in log if e["accuracy"] == best][0]["strategy"]
        summary.append((label, len(X), baseline, best, best_strat))

    print("\n" + "=" * 70)
    print("  Dream-RSI — Summary")
    print("=" * 70)
    print(f"  {'Problem':<25} {'n':>5} {'Baseline':>8} {'Best':>8} {'Gain':>8}  Best Strategy")
    print(f"  {'-'*25} {'-'*5} {'-'*8} {'-'*8} {'-'*8}  {'-'*30}")
    for label, n, baseline, best, strat in summary:
        gain = best - baseline
        print(f"  {label:<25} {n:>5} {baseline:>8.4f} {best:>8.4f} {gain:>+8.4f}  {strat}")
    print()


if __name__ == "__main__":
    main()
