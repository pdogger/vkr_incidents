import numpy as np


class RankingProcessor:
    def __init__(self, matrix: np.array) -> None:
        self.matrix = matrix
        self.result = dict()

    def _get_coherence_value(self, X: np.array) -> dict[str, float]:
        K, L = X.shape
        X_mean = X.sum(axis=0) / K

        coherences = {
            f"E{i+1}": np.sum((X[i] - X_mean)**2) / (L - 1) for i in range(K)
        }

        return coherences

    def calculate_values(self, check_coherence: bool = True) -> dict:
        W = self.matrix.sum(axis=0)
        W = W / W.sum()

        self.result["W"] = W

        if check_coherence is True:
            self.result["Z"] = self._get_coherence_value(self.matrix)

        return self.result
