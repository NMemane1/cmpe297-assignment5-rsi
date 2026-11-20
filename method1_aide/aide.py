"""
AIDE — AI Development Environment (RSI Method 1)

Recursive Self-Improvement loop for code optimisation.

Each iteration:
  1. Execute the current code version and measure wall-clock time.
  2. Analyse the code for optimisation opportunities (simulated).
  3. Select the next improved version from the problem's version ladder.
  4. Benchmark the new version against the old one.
  5. Keep the faster version and iterate.

The "analysis" and "generation" steps are deterministic here (we walk a
predefined version ladder) so the demo is fully reproducible without an
LLM API key.  In a production AIDE system these steps would call a code
LLM.
"""

import textwrap
import time
import tracemalloc
from typing import Any, Callable


def _benchmark(code: str, inp: Any, repeats: int = 5) -> dict:
    """Execute *code* (which must define ``solve``) and return timing stats."""
    ns: dict = {}
    exec(compile(code, "<aide>", "exec"), ns)
    fn: Callable = ns["solve"]

    # warm-up
    fn(inp)

    tracemalloc.start()
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        result = fn(inp)
        t1 = time.perf_counter()
        times.append(t1 - t0)
    _, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "mean_s": sum(times) / len(times),
        "min_s": min(times),
        "max_s": max(times),
        "peak_mem_kb": peak_mem / 1024,
        "result": result,
    }


def run_aide_loop(problem: dict, *, verbose: bool = True) -> list[dict]:
    """Run the AIDE optimisation loop on *problem* and return a log."""
    versions = problem["versions"]
    make_input = problem["make_input"]
    verify = problem["verify"]

    log: list[dict] = []
    inp = make_input()

    if verbose:
        print(f"\n{'='*70}")
        print(f"  AIDE RSI Loop — {problem['name']}")
        print(f"  {problem['description']}")
        print(f"{'='*70}")

    prev_time = None

    for i, ver in enumerate(versions):
        stats = _benchmark(ver["code"], inp)

        # correctness check
        correct = verify(stats["result"], inp)

        delta = ""
        speedup = ""
        if prev_time is not None and stats["mean_s"] > 0:
            change = (prev_time - stats["mean_s"]) / prev_time * 100
            delta = f"{change:+.1f}%"
            speedup = f"{prev_time / stats['mean_s']:.2f}x"

        entry = {
            "iteration": i,
            "label": ver["label"],
            "mean_s": stats["mean_s"],
            "min_s": stats["min_s"],
            "peak_mem_kb": stats["peak_mem_kb"],
            "correct": correct,
            "delta": delta,
            "speedup": speedup,
        }
        log.append(entry)

        if verbose:
            print(f"\n--- Iteration {i} : {ver['label']} ---")
            print(f"  Mean time   : {stats['mean_s']*1000:>10.3f} ms")
            print(f"  Min time    : {stats['min_s']*1000:>10.3f} ms")
            print(f"  Peak memory : {stats['peak_mem_kb']:>10.1f} KB")
            print(f"  Correct     : {correct}")
            if delta:
                print(f"  Improvement : {delta}  ({speedup} faster)")
            print(f"  Code:")
            for line in ver["code"].strip().splitlines():
                print(f"    {line}")

        prev_time = stats["mean_s"]

    if verbose:
        total_speedup = log[0]["mean_s"] / log[-1]["mean_s"] if log[-1]["mean_s"] > 0 else float("inf")
        print(f"\n  ** Total speedup: {total_speedup:.1f}x  "
              f"({log[0]['mean_s']*1000:.3f} ms → {log[-1]['mean_s']*1000:.3f} ms) **\n")

    return log
