from methods import AHPProcessor, RankingProcessor, PayoffMatrixProcessor
import numpy as np

from incidents.models import Incident, IncidentExpert


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


def get_all_scores(incident: Incident) -> list:
    scores = []

    # TODO упорядочить по номеру эксперта
    for e in incident.experts.all():
        scores.append(IncidentExpert.objects.get(incident_id=incident.id, expert_id=e.id).scores)
    return scores
