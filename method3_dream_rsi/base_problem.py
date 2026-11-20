"""Base classification problems for Dream-RSI synthetic data augmentation."""

import numpy as np
from sklearn.datasets import make_moons, make_circles


def problem_moons(n=300, noise=0.25, seed=42):
    """Two interleaving half-moons — small dataset, noisy."""
    X, y = make_moons(n_samples=n, noise=noise, random_state=seed)
    return X, y, "Two Moons (noisy)"


def problem_circles(n=300, noise=0.15, seed=42):
    """Concentric circles — inner vs outer ring."""
    X, y = make_circles(n_samples=n, noise=noise, factor=0.4, random_state=seed)
    return X, y, "Concentric Circles"


def problem_sparse_xor(n=120, noise=0.12, seed=42):
    """XOR pattern with very few samples — augmentation should help most here."""
    rng = np.random.RandomState(seed)
    X = rng.randn(n, 2)
    y = ((X[:, 0] * X[:, 1]) > 0).astype(int)
    flip = rng.rand(n) < noise
    y[flip] = 1 - y[flip]
    return X, y, "Sparse XOR (n=120)"


ALL_PROBLEMS = [
    problem_moons,
    problem_circles,
    problem_sparse_xor,
]
