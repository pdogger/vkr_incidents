from incidents.models import Strategy
import numpy as np

def prepare_results(incident):
    if incident.results == None :
        return {}
    results = {}

    for criteria in incident.results.keys():
        results[criteria] = {}
        for key in incident.results[criteria].keys():
            results[criteria][key] = {
                'value': incident.results[criteria][key],
                'strategy_name': Strategy.objects.get(incident=incident, number=key[-1]).name
            }
            
    return results


def mutate_matrix(matrix, title, letter):
    matrix = np.vstack([np.zeros((1, len(matrix[0]))),np.array(matrix)])
    matrix = np.hstack([np.zeros((len(matrix), 1)),np.array(matrix)]).tolist()
    matrix[0][0] = title
    for x in range(1,len(matrix)):
        matrix[x][0] = letter + str(x)
    
    for y in range(1,len(matrix[0])):
        matrix[0][y] = letter + str(y)

    return matrix

def prepare_score_matrix(scores):
    result = {}
    if scores['C'] != None:
        result["C"] = mutate_matrix(scores["C"], "Критерии", "C")

    result['S'] = {}
    for basis in scores["S"].keys():
        result['S'][basis] = []
        for criteria in range(len(scores["S"][basis])):
            result['S'][basis].append(mutate_matrix(scores["S"][basis][criteria], "", "S"))
    return result

test = {'C': [[1.0, 1.0], [1.0, 1.0]], 'S': {'B1': [[[1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0]], [[1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0]]], 'B2': [[[1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0]], [[1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0]]], 'B3': [[[1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0]], [[1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0]]]}, 'V': {'B1': [0.25, 0.25, 0.25, 0.25], 'B2': [0.25, 0.25, 0.25, 0.25], 'B3': [0.25, 0.25, 0.25, 0.25]}}