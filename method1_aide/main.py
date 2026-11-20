#!/usr/bin/env python3
"""Run the AIDE RSI loop on all sample problems."""

from problems import ALL_PROBLEMS
from aide import run_aide_loop


def main():
    print("=" * 70)
    print("  AIDE — AI Development Environment")
    print("  Recursive Self-Improvement for Code Optimisation")
    print("=" * 70)

    summary = []

    for problem in ALL_PROBLEMS:
        log = run_aide_loop(problem)
        if log:
            first = log[0]["mean_s"]
            last = log[-1]["mean_s"]
            speedup = first / last if last > 0 else float("inf")
            summary.append((problem["name"], len(log), speedup, first, last))

    print("\n" + "=" * 70)
    print("  AIDE — Summary of All Problems")
    print("=" * 70)
    print(f"  {'Problem':<35} {'Iters':>5}  {'Speedup':>8}  {'Start ms':>10}  {'End ms':>10}")
    print(f"  {'-'*35} {'-'*5}  {'-'*8}  {'-'*10}  {'-'*10}")
    for name, iters, speedup, start, end in summary:
        print(f"  {name:<35} {iters:>5}  {speedup:>7.1f}x  {start*1000:>10.3f}  {end*1000:>10.3f}")
    print()


if __name__ == "__main__":
    main()
