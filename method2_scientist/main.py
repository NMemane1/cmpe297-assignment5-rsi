#!/usr/bin/env python3
"""Run the Automated Scientist RSI loop on all synthetic datasets."""

from datasets import ALL_DATASETS
from scientist import run_scientist_loop


def main():
    print("=" * 70)
    print("  Automated Scientist")
    print("  Recursive Self-Improvement for Hypothesis Discovery")
    print("=" * 70)

    summary = []

    for name, make_data in ALL_DATASETS:
        X, y, truth = make_data()
        log = run_scientist_loop(name, X, y, truth)
        if log:
            baseline = log[0]["accuracy"]
            best = max(e["accuracy"] for e in log)
            best_method = [e for e in log if e["accuracy"] == best][0]["experiment"]
            summary.append((name, baseline, best, best_method, truth["true_rule"]))

    print("\n" + "=" * 70)
    print("  Automated Scientist — Summary")
    print("=" * 70)
    print(f"  {'Dataset':<22} {'Baseline':>8} {'Best':>8} {'Gain':>8}  Best Method")
    print(f"  {'-'*22} {'-'*8} {'-'*8} {'-'*8}  {'-'*30}")
    for name, baseline, best, method, rule in summary:
        gain = best - baseline
        print(f"  {name:<22} {baseline:>8.4f} {best:>8.4f} {gain:>+8.4f}  {method}")
    print()
    print("  Ground-truth rules:")
    for name, _, _, _, rule in summary:
        print(f"    {name}: {rule}")
    print()


if __name__ == "__main__":
    main()
