import numpy as np


def naive_bayes(y, x, *obs):
    y = np.array(y)
    classes = set(y)
    X = np.array(obs).T
    N, M = X.shape
    C = len(classes)
    priors = np.zeros(C)

    # Class priors
    for i, c in enumerate(classes):
        priors[i] = sum(y == c) / N

    # Probs
    probs = np.zeros((C, M))
    for i, c in enumerate(classes):
        for j in range(M):
            probs[i, j] = sum((X[:, j] == x[j]) & (y == c)) / sum(y == c)

    # Joint probs
    joint = np.prod(probs, axis=1)

    # Naive bayes
    return (joint * priors) / sum(joint * priors)
