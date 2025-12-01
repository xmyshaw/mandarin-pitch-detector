"""Module for pitch detection algorithms."""
import numpy as np
from sklearn.linear_model import LinearRegression

def linear_regression(X: np.ndarray, y: np.ndarray) -> tuple:
    X = X.reshape(-1, 1)
    y = y.reshape(-1, 1)
    reg = LinearRegression().fit(X, y)
    return reg.coef_, reg.intercept_, reg.score(X, y)
