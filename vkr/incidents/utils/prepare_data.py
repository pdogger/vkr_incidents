from incidents.models import Strategy

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