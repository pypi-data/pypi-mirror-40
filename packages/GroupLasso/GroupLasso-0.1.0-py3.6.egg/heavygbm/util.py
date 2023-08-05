import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sum_gradient_mse(t, score):
    """
    score = xのとき、
    二乗和誤差のx微分は、2 * (score - t)
    """
    return 2 * np.sum(score - t)


def sum_hessian_mse(score):
    """
    score = xのとき、
    二乗和誤差のx 2回微分は、2
    """
    return 2 * len(score)


def sum_gradient_xentropy(t, proba):
    """
    proba = sigmoid(x)のとき、
    交差エントロピー誤差のx微分は、proba - t
    """
    return np.sum(proba - t)


def sum_hessian_xentropy(proba):
    """
    proba = sigmoid(x)のとき、
    交差エントロピー誤差のx 2回微分は、proba * (1 - proba)
    """
    return np.sum(proba * (1 - proba))


sum_gradient = {
    "mse": sum_gradient_mse,
    "xentropy": sum_gradient_xentropy
}

sum_hessian = {
    "mse": sum_hessian_mse,
    "xentropy": sum_hessian_xentropy
}
