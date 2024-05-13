import numpy as np
from incidents.models import Incident, IncidentExpert
from incidents.utils.prepare_data import dict_decode
from methods.AHPProcessor import AHPProcessor
from methods.PayoffMatrixProcessor import PayoffMatrixProcessor
from methods.RankingProcessor import RankingProcessor


def make_matrix(scores: list, num: int) -> list:
    matrix = np.ones((num, num))
    j = 0
    for i in range(num - 1):
        for y in range(i, num - 1):
            matrix[i][y + 1] = scores[j]
            matrix[y + 1][i] = 1 / scores[j]
            j += 1
    return matrix.tolist()


def get_ahp_values(matrices: dict) -> dict:
    result = {}
    for key in matrices["S"].keys():
        ahp = AHPProcessor(matrices["C"], matrices["S"][key], detailed=False)
        result[key] = ahp.calculate_values()

    return result


# Ожидается порядок оценок в соответствии с номером эксперта
def calculate_incident(scores: list) -> dict:
    ahp_values = []
    for score in scores:
        ahp_values.append(get_ahp_values(score))

    rp_values = {}
    for basis in ahp_values[0].keys():
        rp = RankingProcessor(np.stack([a[basis]["V"] for a in ahp_values]))
        rp_values[basis] = rp.calculate_values()

    prepared_payoff_matrix = np.array([x["W"] for x in rp_values.values()]).T
    pmp = PayoffMatrixProcessor(prepared_payoff_matrix)
    pmp.calculate_estimates()
    return pmp.calculate_values()


def check_all_experts_done(incident: Incident) -> bool:
    experts = IncidentExpert.objects.filter(incident_id=incident.id, scores__isnull=True)
    if len(experts) > 0:
        return False
    return True


def prepare_scores(scores: dict, criteria_count: int, strategy_count: int) -> dict:
    result = {}

    if scores["criteria_score"] is not None:
        c_matrix = make_matrix(scores["criteria_score"], criteria_count)
        result["C"] = c_matrix

    result["S"] = {}
    result["V"] = {}

    for i in range(len(scores["basises"])):
        basis = []
        for criteria in scores["basises"][i]:
            basis.append(make_matrix(criteria, strategy_count))
        result["S"]["B" + str(i+1)] = basis
        result['V']["B" + str(i+1)] = AHPProcessor(
            c_matrix, basis,
            detailed=False,
        ).calculate_values()['V'].tolist()

    return result


def get_all_scores(experts: list) -> list:
    scores = []

    for expert in experts:
        scores.append(dict_decode(expert.scores))
    return scores
