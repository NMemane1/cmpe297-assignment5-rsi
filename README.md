# CMPE-297 Assignment 5: Recursive Self-Improvement (RSI)

Three distinct RSI methods demonstrating how AI systems can iteratively improve their own performance along different axes.

## Methods

| # | Method | What Improves | Directory |
|---|--------|---------------|-----------|
| 1 | **AIDE** (AI Development Environment) | Code performance (execution time, memory) | `method1_aide/` |
| 2 | **Automated Scientist** | Model understanding (hypothesis accuracy) | `method2_scientist/` |
| 3 | **Dream-RSI** | Training data quality (synthetic augmentation) | `method3_dream_rsi/` |

## Quick Start

```bash
pip install -r requirements.txt

# Web UI (all methods in one app)
python app.py
# Open http://localhost:9010

# Or run each method independently via CLI
cd method1_aide && python main.py
cd method2_scientist && python main.py
cd method3_dream_rsi && python main.py
```

## Method 1: AIDE

Iteratively optimises code implementations.  Starts with a naive solution (e.g. bubble sort, recursive Fibonacci) and walks through progressively faster versions, benchmarking each.

**Key metric:** Execution time speedup (10x to 1000x+)

## Method 2: Automated Scientist

Iteratively discovers hidden patterns in datasets.  Starts with a simple hypothesis (linear model) and refines through increasingly sophisticated experiments (polynomial features, ensembles, kernel methods).

**Key metric:** Accuracy improvement and feature importance convergence

## Method 3: Dream-RSI

Iteratively augments training data.  When real data is scarce, the system generates synthetic samples using SMOTE interpolation, decision-boundary focus, and class-conditional KDE.  Only keeps augmented data that improves the model.

**Key metric:** Accuracy gain from synthetic data

## Requirements

- Python 3.8+
- scikit-learn
- numpy
- pandas (for AIDE sales aggregation problem)

## Author

Nikita Memane — CMPE-297 Special Topics, Fall 2026
