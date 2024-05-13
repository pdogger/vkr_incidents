import numpy as np


class PayoffMatrixProcessor:
    def __init__(self, matrix: np.array, invert: bool = True) -> None:
        self.matrix = matrix if invert is False else 1 / matrix
        self.estimates = dict()
        self.result = dict()

    def _get_sorted_dict(self, values: np.array) -> dict[str, float]:
        return dict(
            sorted(
                {f"S{i + 1}": v for i, v in enumerate(values)}.items(),
                key=lambda x: x[1],
            ),
        )

    def calculate_estimates(self) -> dict[str, np.array]:
        self.estimates["Z_max"] = np.max(self.matrix, axis=1)
        self.estimates["Z_min"] = np.min(self.matrix, axis=1)
        self.estimates["Z_mean"] = np.mean(self.matrix, axis=1)

        self.estimates["Z_min_s"] = np.min(self.matrix, axis=0)
        self.estimates["R_max"] = np.max(self.matrix - self.estimates["Z_min_s"], axis=1)

        return self.estimates

    def calculate_values(
        self,
        alpha_hur: float | None = 0.5,
        alphas_Q: tuple = (0.25, 0.25, 0.25, 0.25),
    ) -> dict[str, float]:
        self.result["Q_vald"] = self._get_sorted_dict(self.estimates["Z_max"])
        self.result["Q_lapl"] = self._get_sorted_dict(self.estimates["Z_mean"])
        self.result["Q_sav"] = self._get_sorted_dict(self.estimates["R_max"])
        self.result["Q_hur"] = self._get_sorted_dict(
            alpha_hur * self.estimates["Z_max"] + (1 - alpha_hur) * self.estimates["Z_min"],
        )
        self.result["Q"] = self._get_sorted_dict(
            alphas_Q[0] * self.estimates["Z_max"] + alphas_Q[1] * self.estimates["Z_min"] +
            alphas_Q[2] * self.estimates["Z_mean"] + alphas_Q[3] * self.estimates["R_max"],
        )

        return self.result
