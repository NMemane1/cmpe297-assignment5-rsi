"""
Dream-RSI — Recursive Self-Improvement via Synthetic Data Augmentation

The core idea: when real data is scarce or noisy, the system "dreams" new
training samples by applying learned transformations, then retrains on the
augmented dataset.  Each cycle:

  1. Train a baseline model on current data
  2. Analyse decision-boundary confidence
  3. Generate synthetic samples in low-confidence regions
  4. Retrain on the augmented dataset
  5. Measure improvement and repeat
"""

import numpy as np
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KernelDensity


def _augment_smote_style(X, y, n_new=50, seed=42):
    """Generate synthetic samples via SMOTE-like interpolation."""
    rng = np.random.RandomState(seed)
    X_new, y_new = [], []
    classes = np.unique(y)
    per_class = max(1, n_new // len(classes))

    for c in classes:
        X_c = X[y == c]
        for _ in range(per_class):
            i, j = rng.choice(len(X_c), 2, replace=True)
            lam = rng.uniform(0.2, 0.8)
            X_new.append(X_c[i] + lam * (X_c[j] - X_c[i]))
            y_new.append(c)

    return np.array(X_new), np.array(y_new)


def _augment_boundary(X, y, model, n_new=60, seed=42):
    """Generate synthetic samples near the decision boundary (low-confidence region)."""
    rng = np.random.RandomState(seed)
    if hasattr(model, "decision_function"):
        dist = np.abs(model.decision_function(X))
    elif hasattr(model, "predict_proba"):
        proba = model.predict_proba(X)
        dist = np.abs(proba[:, 1] - 0.5)
    else:
        dist = np.ones(len(X))

    # Favour samples near the boundary (low distance)
    weights = 1.0 / (dist + 1e-6)
    weights /= weights.sum()
    idx = rng.choice(len(X), size=n_new, p=weights, replace=True)
    noise = rng.randn(n_new, X.shape[1]) * 0.08
    X_new = X[idx] + noise
    y_new = model.predict(X_new)
    return X_new, y_new


def _augment_kde(X, y, n_new=60, seed=42):
    """Generate synthetic samples from class-conditional KDE."""
    rng = np.random.RandomState(seed)
    classes = np.unique(y)
    per_class = max(1, n_new // len(classes))
    X_new, y_new = [], []

    for c in classes:
        X_c = X[y == c]
        kde = KernelDensity(bandwidth=0.3, kernel="gaussian")
        kde.fit(X_c)
        samples = kde.sample(per_class, random_state=rng.randint(0, 10000))
        X_new.append(samples)
        y_new.extend([c] * per_class)

    return np.vstack(X_new), np.array(y_new)


AUGMENTATION_STRATEGIES = [
    ("SMOTE-style interpolation", _augment_smote_style),
    ("Decision-boundary focus", _augment_boundary),
    ("Class-conditional KDE", _augment_kde),
]


def run_dream_loop(X_orig, y_orig, label, *, n_cycles=3, verbose=True):
    """Run the Dream-RSI loop and return a log of each cycle."""
    if verbose:
        print(f"\n{'='*70}")
        print(f"  Dream-RSI — {label}")
        print(f"  Original samples: {len(X_orig)}")
        print(f"{'='*70}")

    X_cur = X_orig.copy()
    y_cur = y_orig.copy()
    log = []

    # Baseline
    model = GradientBoostingClassifier(n_estimators=80, max_depth=3, random_state=42)
    baseline = cross_val_score(model, X_cur, y_cur, cv=5, scoring="accuracy").mean()
    model.fit(X_cur, y_cur)

    if verbose:
        print(f"\n  Baseline accuracy (n={len(X_cur)}): {baseline:.4f}")

    log.append({
        "cycle": 0,
        "strategy": "baseline",
        "n_samples": len(X_cur),
        "accuracy": baseline,
        "delta": 0.0,
    })

    best = baseline

    for cycle, (strat_name, strat_fn) in enumerate(AUGMENTATION_STRATEGIES, 1):
        seed = 42 + cycle
        n_new = max(30, len(X_orig) // 3)

        if strat_fn == _augment_boundary:
            X_synth, y_synth = strat_fn(X_cur, y_cur, model, n_new=n_new, seed=seed)
        else:
            X_synth, y_synth = strat_fn(X_cur, y_cur, n_new=n_new, seed=seed)

        X_aug = np.vstack([X_cur, X_synth])
        y_aug = np.concatenate([y_cur, y_synth])

        model_new = GradientBoostingClassifier(n_estimators=80, max_depth=3, random_state=42)
        acc = cross_val_score(model_new, X_aug, y_aug, cv=5, scoring="accuracy").mean()
        delta = acc - best

        if acc > best:
            best = acc
            X_cur = X_aug
            y_cur = y_aug
            model_new.fit(X_cur, y_cur)
            model = model_new
            kept = True
        else:
            kept = False

        entry = {
            "cycle": cycle,
            "strategy": strat_name,
            "n_samples": len(X_aug),
            "accuracy": acc,
            "delta": delta,
            "kept": kept,
        }
        log.append(entry)

        if verbose:
            marker = " ** KEPT **" if kept else " (discarded)"
            print(f"\n--- Cycle {cycle}: {strat_name}{marker} ---")
            print(f"  Synthetic samples added : {len(X_synth)}")
            print(f"  Total samples           : {len(X_aug)}")
            print(f"  Accuracy                : {acc:.4f} (delta {delta:+.4f})")

    if verbose:
        total_gain = best - baseline
        print(f"\n  ** Best accuracy: {best:.4f}  "
              f"(+{total_gain:.4f} over baseline) **\n")

    return log
