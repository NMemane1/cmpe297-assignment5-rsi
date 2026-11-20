"""Synthetic datasets with hidden patterns for the Automated Scientist."""

import numpy as np
from sklearn.datasets import make_classification


def dataset_nonlinear_xor(n=600, noise=0.15, seed=42):
    """XOR-style non-linear pattern: y = sign(x1 * x2) with noise."""
    rng = np.random.RandomState(seed)
    X = rng.randn(n, 5)
    y = ((X[:, 0] * X[:, 1]) > 0).astype(int)
    flip = rng.rand(n) < noise
    y[flip] = 1 - y[flip]
    return X, y, {
        "true_rule": "y = sign(x0 * x1)  — an XOR interaction",
        "relevant_features": [0, 1],
        "irrelevant_features": [2, 3, 4],
    }


def dataset_threshold_sum(n=600, noise=0.10, seed=42):
    """Threshold on the sum of two features: y = 1 if x0 + x2 > 0."""
    rng = np.random.RandomState(seed)
    X = rng.randn(n, 6)
    y = ((X[:, 0] + X[:, 2]) > 0).astype(int)
    flip = rng.rand(n) < noise
    y[flip] = 1 - y[flip]
    return X, y, {
        "true_rule": "y = 1 if (x0 + x2) > 0",
        "relevant_features": [0, 2],
        "irrelevant_features": [1, 3, 4, 5],
    }


def dataset_quadratic_boundary(n=800, noise=0.12, seed=42):
    """Quadratic decision boundary: y = 1 if x0^2 + x1^2 < 2."""
    rng = np.random.RandomState(seed)
    X = rng.uniform(-2.5, 2.5, (n, 4))
    y = ((X[:, 0] ** 2 + X[:, 1] ** 2) < 2.5).astype(int)
    flip = rng.rand(n) < noise
    y[flip] = 1 - y[flip]
    return X, y, {
        "true_rule": "y = 1 if x0² + x1² < 2.5  — circular boundary",
        "relevant_features": [0, 1],
        "irrelevant_features": [2, 3],
    }


ALL_DATASETS = [
    ("XOR Interaction", dataset_nonlinear_xor),
    ("Threshold Sum", dataset_threshold_sum),
    ("Quadratic Boundary", dataset_quadratic_boundary),
]
