from functools import reduce
import numpy as np

R_table = {
    3: 0.58,
    4: 0.9,
    5: 1.12
}


class PairwiseProcessor:
    def __init__(self, S_scores: list) -> None:
        self.S_scores = np.array(S_scores)
        self.result = dict()
        self.coherence = dict()

        self._V: np.array | None = None


    def _get_weights(self, X: np.array) -> np.array:
        V = np.array([pow(reduce(lambda a, b: a*b, alt), 1 / X.shape[0]) for alt in X])
        V = V / V.sum()

        return V

    def _get_coherence_value(self, X: np.array, V: np.array) -> float:
        if len(V) < 3:
            return 0

        G = X.sum(axis=0)
        A = np.sum(G*V)

        L = len(V)
        coherence = (A - L) / (R_table[L] * (L - 1))

        return coherence

    def _check_coherence(self) -> float:
        self.coherence["S"] = self._get_coherence_value(self.S_scores, self._V)

        return self.coherence

    def calculate_values(self, check_coherence: bool = True) -> dict:
        self._V = self._get_weights(self.S_scores)
        self.result["V"] = self._V

        if check_coherence is True:
            self.result["Z"] = self._check_coherence()

        return self.result
