# Method 3: Dream-RSI — Synthetic Data Augmentation

## Overview

Dream-RSI implements a Recursive Self-Improvement loop for **data augmentation**.  When real training data is scarce or noisy the system "dreams" synthetic samples to strengthen its decision boundary:

1. **Train** a baseline model on the original data
2. **Analyse** where the model is least confident
3. **Generate** synthetic samples using a learned strategy
4. **Retrain** on the augmented dataset
5. **Evaluate** and keep the augmented set only if accuracy improves

## Problems

| # | Problem | Samples | Why Augmentation Helps |
|---|---------|---------|----------------------|
| 1 | Two Moons (noisy) | 300 | Noisy boundary benefits from densification |
| 2 | Concentric Circles | 300 | Circular boundary needs more support vectors |
| 3 | Sparse XOR (n=120) | 120 | Very few samples — biggest improvement expected |

## Augmentation Strategies

Each cycle applies a progressively smarter strategy:

1. **SMOTE-style interpolation** — creates new samples by interpolating between same-class neighbours
2. **Decision-boundary focus** — generates samples in regions where the current model is least confident
3. **Class-conditional KDE** — fits a kernel density estimate per class and draws new samples from it

Only augmented datasets that improve accuracy are kept (a greedy accept/reject gate).

## Running

```bash
cd method3_dream_rsi
python main.py
```

## Output

Each cycle prints:
- The augmentation strategy used
- Number of synthetic samples added
- Cross-validated accuracy on the augmented dataset
- Whether the augmented set was kept or discarded

## Key RSI Concept

Dream-RSI shows that **the training data itself can be improved through iterative refinement**.  Unlike AIDE (which improves code) or the Automated Scientist (which improves hypotheses), Dream-RSI improves the data the model learns from.  This is a third axis of recursive self-improvement: better data leads to a better model, which guides better data generation.
