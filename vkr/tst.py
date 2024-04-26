from pprint import pprint
import numpy as np
import pandas as pd

from methods.AHPProcessor import AHPProcessor
from methods.RankingProcessor import RankingProcessor
from methods.PayoffMatrixProcessor import PayoffMatrixProcessor


def get_ahp_values(matrices: dict) -> dict:
    result = dict()
    for key in matrices["S"].keys():
        ahp = AHPProcessor(matrices["C"], matrices["S"][key], detailed=False)
        result[key] = ahp.calculate_values()

    return result


E1_matrices = {
    "C": [
            [1, 3],
            [1/3, 1]
        ],
    "S": {
        "B1": [
            [
                [1, 1/3, 1/5, 1],
                [3, 1, 1, 5],
                [5, 1, 1, 5],
                [1, 1/5, 1/5, 1]
            ],
            [
                [1, 3, 3, 5],
                [1/3, 1, 1, 3],
                [1/3, 1, 1, 3],
                [1/5, 1/3, 1/3, 1]
            ]
        ],
        "B2": [
            [
                [1, 1, 1, 3],
                [1, 1, 1, 3],
                [1, 1, 1, 3],
                [1/3, 1/3, 1/3, 1]
            ],
            [
                [1, 1, 1, 5],
                [1, 1, 1, 3],
                [1, 1, 1, 3],
                [1/5, 1/3, 1/3, 1]
            ]
        ],
        "B3": [
            [
                [1, 3, 3, 3],
                [1/3, 1, 1, 3],
                [1/3, 1, 1, 3],
                [1/3, 1/3, 1/3, 1]
            ],
            [
                [1, 5, 5, 7],
                [1/5, 1, 1, 3],
                [1/5, 1, 1, 3],
                [1/7, 1/3, 1/3, 1]
            ]
        ]
    }
}

E2_matrices = {
    "C": [
            [1, 5],
            [1/5, 1]
        ],
    "S": {
        "B1": [
            [
                [1, 1/3, 1/3, 3],
                [3, 1, 3, 7],
                [3, 1/3, 1, 7],
                [1/3, 1/7, 1/7, 1]
            ],
            [
                [1, 3, 1, 5],
                [1/3, 1, 1/3, 3],
                [1, 3, 1, 7],
                [1/5, 1/3, 1/7, 1]
            ]
        ],
        "B2": [
            [
                [1, 1, 3, 7],
                [1, 1, 3, 7],
                [1/3, 1/3, 1, 5],
                [1/7, 1/7, 1/5, 1]
            ],
            [
                [1, 1/3, 1, 5],
                [3, 1, 3, 5],
                [1, 1/3, 1, 5],
                [1/5, 1/5, 1/5, 1]
            ]
        ],
        "B3": [
            [
                [1, 3, 5, 3],
                [1/3, 1, 3, 3],
                [1/5, 1/3, 1, 1],
                [1/3, 1/3, 1, 1]
            ],
            [
                [1, 5, 3, 5],
                [1/5, 1, 1/3, 1],
                [1/3, 3, 1, 3],
                [1/5, 1, 1/3, 1]
            ]
        ]
    }
}

ahp_values = dict()
ahp_values["E1"] = get_ahp_values(E1_matrices)
ahp_values["E2"] = get_ahp_values(E2_matrices)
pprint(ahp_values)

print()
rp_values = dict()
for basis in ahp_values["E1"].keys():
    rp = RankingProcessor(np.stack((ahp_values["E1"][basis]["V"], ahp_values["E2"][basis]["V"])))
    rp_values[basis] = rp.calculate_values()
pprint(rp_values)

print()
prepared_payoff_matrix = np.array([x["W"] for x in rp_values.values()]).T
pmp = PayoffMatrixProcessor(prepared_payoff_matrix)
pmp_estimates = pmp.calculate_estimates()
pprint(pmp_estimates, sort_dicts=False)

print()
pmp_values = pmp.calculate_values()
pprint(pmp_values, sort_dicts=False)
