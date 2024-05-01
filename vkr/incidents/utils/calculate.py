from methods.AHPProcessor import AHPProcessor
from methods.RankingProcessor import RankingProcessor
from methods.PayoffMatrixProcessor import PayoffMatrixProcessor
import numpy as np
from pprint import pprint

from incidents.models import Incident, IncidentExpert, IncidentCriteria, Strategy

def make_matrix(scores: list, num: int) -> np.array:
    matrix = np.ones((num, num))
    j = 0
    for i in range(num-1):
        for y in range(i,num-1):
            matrix[i][y+1] = scores[j]
            matrix[y+1][i] = 1/scores[j]
            j+=1
    return matrix

    
def get_ahp_values(matrices: dict) -> dict:
    result = dict()
    for key in matrices["S"].keys():
        ahp = AHPProcessor(matrices["C"], matrices["S"][key], detailed=False)
        result[key] = ahp.calculate_values()

    return result


# Ожидается порядок оценок в соответствии с номером эксперта
def calculate_incident(scores: list) -> dict:
    ahp_values = []
    for score in scores:
        ahp_values.append(get_ahp_values(score))

    rp_values = dict()
    for basis in ahp_values[0].keys():
        rp = RankingProcessor(np.stack([a[basis]["V"]  for a in ahp_values ]))
        rp_values[basis] = rp.calculate_values()

    prepared_payoff_matrix = np.array([x["W"] for x in rp_values.values()]).T
    pmp = PayoffMatrixProcessor(prepared_payoff_matrix)
    pmp.calculate_estimates()
    return pmp.calculate_values()


def check_all_experts_done(incident: Incident) -> bool:
    for e in incident.experts.all():
        if IncidentExpert.objects.filter(incident_id=incident.id, expert_id=e.id,
                                         scores__isnull = True).count() > 0:
            return False
    return True

def prepare_scores(scores: dict, criteria_count: int, strategy_count: int) -> dict:
    result = {}

    if scores["criteria_score"] != None:
        c_matrix = make_matrix(scores["criteria_score"], criteria_count)
        result["C"] = c_matrix

    result["S"] = {}

    for i in range(len(scores["basises"])):
        basis = []
        for criteria in scores["basises"][i]:
            basis.append(make_matrix(criteria, strategy_count))
        result["S"]["B" + str(i+1)] = basis
    
    return result


def get_all_scores(incident: Incident) -> list:
    scores = []

    for expert in IncidentExpert.objects.filter(incident=incident).all().order_by('number'):
        expert_scores = prepare_scores(expert.scores,
                                       IncidentCriteria.objects.filter(incident=incident).count(),
                                       Strategy.objects.filter(incident=incident).count())
        scores.append(expert_scores)
    return scores
