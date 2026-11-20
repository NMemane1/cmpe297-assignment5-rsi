# Method 2: Automated Scientist

## Overview

The Automated Scientist implements a Recursive Self-Improvement loop for **hypothesis discovery**.  Given a dataset with a hidden pattern the system iteratively:

1. **Hypothesises** about what drives the target variable
2. **Designs** an experiment (feature engineering + model)
3. **Runs** the experiment and measures accuracy
4. **Analyses** feature importances and residuals
5. **Refines** the hypothesis and repeats with a more powerful approach

## Datasets

| # | Dataset | Hidden Rule | Features |
|---|---------|-------------|----------|
| 1 | XOR Interaction | y = sign(x0 * x1) | 5 (2 relevant) |
| 2 | Threshold Sum | y = 1 if x0 + x2 > 0 | 6 (2 relevant) |
| 3 | Quadratic Boundary | y = 1 if x0² + x1² < 2.5 | 4 (2 relevant) |

Each dataset includes irrelevant noise features that the scientist must learn to ignore.

## Hypothesis Ladder

1. Logistic Regression (linear baseline)
2. Decision Tree (non-linear splits)
3. Polynomial Features + Logistic Regression (interaction terms)
4. Random Forest (ensemble discovery)
5. Gradient Boosting + Polynomial Features (residual patterns)
6. RBF SVM (non-linear boundary modelling)

## Running

```bash
cd method2_scientist
python main.py
```

## Output

Each iteration prints:
- The current hypothesis and experiment design
- Cross-validated accuracy and standard deviation
- Whether the iteration improved on the previous best
- Feature importance insights compared to ground truth

## Key RSI Concept

The Automated Scientist demonstrates that **model understanding can be improved through iterative refinement**.  Each hypothesis builds on insights from the previous one, progressively uncovering the true data-generating process.  The system converges toward the ground-truth rule without being told what it is.
