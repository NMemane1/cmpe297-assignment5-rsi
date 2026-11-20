"""
Automated Scientist — RSI Method 2

Recursive Self-Improvement loop for hypothesis generation and testing.

Each iteration:
  1. Generate a hypothesis about what drives the target variable.
  2. Design an experiment (feature engineering + model choice).
  3. Run the experiment and evaluate accuracy.
  4. Refine the hypothesis based on results.
  5. Iterate toward deeper understanding.
"""

import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
)
from sklearn.svm import SVC
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import Pipeline


# Each "hypothesis" is a (description, pipeline-factory) pair.
# The scientist tries them in order, progressively refining its approach.

def _make_hypotheses():
    """Return the ladder of hypotheses the scientist will try."""
    return [
        {
            "hypothesis": "The target depends linearly on individual features.",
            "experiment": "Logistic Regression on raw features.",
            "build": lambda: Pipeline([
                ("scale", StandardScaler()),
                ("model", LogisticRegression(max_iter=500)),
            ]),
        },
        {
            "hypothesis": "A single decision tree may capture non-linear splits.",
            "experiment": "Decision Tree (depth 4) on raw features.",
            "build": lambda: Pipeline([
                ("scale", StandardScaler()),
                ("model", DecisionTreeClassifier(max_depth=4, random_state=42)),
            ]),
        },
        {
            "hypothesis": "Feature interactions matter — add polynomial features.",
            "experiment": "Logistic Regression on degree-2 polynomial features.",
            "build": lambda: Pipeline([
                ("poly", PolynomialFeatures(degree=2, interaction_only=False)),
                ("scale", StandardScaler()),
                ("model", LogisticRegression(max_iter=1000)),
            ]),
        },
        {
            "hypothesis": "An ensemble of trees can discover complex interactions.",
            "experiment": "Random Forest (100 trees) on raw features.",
            "build": lambda: Pipeline([
                ("scale", StandardScaler()),
                ("model", RandomForestClassifier(
                    n_estimators=100, max_depth=6, random_state=42
                )),
            ]),
        },
        {
            "hypothesis": "Boosting with polynomial features captures residual patterns.",
            "experiment": "Gradient Boosting on degree-2 polynomial features.",
            "build": lambda: Pipeline([
                ("poly", PolynomialFeatures(degree=2, interaction_only=True)),
                ("scale", StandardScaler()),
                ("model", GradientBoostingClassifier(
                    n_estimators=150, max_depth=4, random_state=42
                )),
            ]),
        },
        {
            "hypothesis": "SVM with RBF kernel can model the circular/non-linear boundary.",
            "experiment": "RBF SVM on raw features (tuned C and gamma).",
            "build": lambda: Pipeline([
                ("scale", StandardScaler()),
                ("model", SVC(kernel="rbf", C=10, gamma="scale", random_state=42)),
            ]),
        },
    ]


def run_scientist_loop(name: str, X, y, ground_truth: dict,
                       *, verbose: bool = True) -> list[dict]:
    """Run the automated-scientist RSI loop and return a log."""
    hypotheses = _make_hypotheses()
    log = []

    if verbose:
        print(f"\n{'='*70}")
        print(f"  Automated Scientist — {name}")
        print(f"  Ground truth: {ground_truth['true_rule']}")
        print(f"{'='*70}")

    best_score = 0.0

    for i, h in enumerate(hypotheses):
        pipe = h["build"]()
        scores = cross_val_score(pipe, X, y, cv=5, scoring="accuracy")
        mean_acc = scores.mean()
        std_acc = scores.std()

        improved = mean_acc > best_score
        delta = mean_acc - best_score if best_score > 0 else 0.0
        if improved:
            best_score = mean_acc

        # Feature importance insight (for tree-based models)
        insight = ""
        pipe.fit(X, y)
        model = pipe.named_steps.get("model")
        if hasattr(model, "feature_importances_"):
            imp = model.feature_importances_
            # Map back through polynomial features if present
            if "poly" in pipe.named_steps:
                n_orig = X.shape[1]
                insight = f"Top raw-feature indices by importance (pre-poly): model uses {len(imp)} features"
            else:
                top_idx = np.argsort(imp)[::-1][:3]
                insight = f"Top features by importance: {list(top_idx)} (true: {ground_truth['relevant_features']})"
        elif hasattr(model, "coef_"):
            coef = np.abs(model.coef_[0])
            if "poly" not in pipe.named_steps:
                top_idx = np.argsort(coef)[::-1][:3]
                insight = f"Top features by |coef|: {list(top_idx)} (true: {ground_truth['relevant_features']})"
            else:
                insight = "Polynomial features used — many interaction terms active"

        entry = {
            "iteration": i,
            "hypothesis": h["hypothesis"],
            "experiment": h["experiment"],
            "accuracy": mean_acc,
            "std": std_acc,
            "improved": improved,
            "delta": delta,
            "insight": insight,
        }
        log.append(entry)

        if verbose:
            marker = " ** NEW BEST **" if improved else ""
            print(f"\n--- Iteration {i}{marker} ---")
            print(f"  Hypothesis  : {h['hypothesis']}")
            print(f"  Experiment  : {h['experiment']}")
            print(f"  Accuracy    : {mean_acc:.4f} (+/- {std_acc:.4f})")
            if delta > 0:
                print(f"  Improvement : +{delta:.4f}")
            print(f"  Insight     : {insight}")

    if verbose:
        total_gain = best_score - log[0]["accuracy"]
        print(f"\n  ** Best accuracy: {best_score:.4f}  "
              f"(+{total_gain:.4f} over baseline) **\n")

    return log
