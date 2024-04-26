from functools import reduce
import numpy as np

from methods.PairwiseProcessor import PairwiseProcessor


class AHPProcessor(PairwiseProcessor):
    def __init__(self, C_scores: list, S_scores: list[list], detailed: bool = True) -> None:
        self.C_scores = np.array(C_scores)
        self.S_scores = np.array(S_scores)
        self.detailed = detailed
        self.result = dict()
        self.coherence = dict()

        self._C_weights: np.array | None = None
        self._S_weights: np.array | None = None
        self._V: np.array | None = None

    def _check_coherence(self) -> float:
        self.coherence["C"] = self._get_coherence_value(self.C_scores, self._C_weights)

        self.coherence["S"] = {
            f"C{i + 1}": self._get_coherence_value(self.S_scores[i], self._S_weights[i]) \
                for i in range(len(self.C_scores))
        }

        return self.coherence

    def calculate_values(self, check_coherence: bool = True) -> dict:
        self._C_weights = self._get_weights(self.C_scores)
        self._S_weights = np.array([self._get_weights(x) for x in self.S_scores])

        self._V = np.array([sum(F * self._C_weights) for F in self._S_weights.T])

        self.result["V"] = self._V

        if check_coherence is True:
            self.result["Z"] = self._check_coherence()

        if self.detailed is True:
            self.result["C_weights"] = self._C_weights
            self.result["S_weights"] = self._S_weights

        return self.result
