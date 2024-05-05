from incidents.models import Strategy

def prepare_results(incident):
    if incident.results == None:
        return {}
    results = {}

    strategies = Strategy.objects.filter(incident=incident).all()

    for criteria in incident.results.keys():
        results[criteria] = {}
        for strategy in strategies:
            results[criteria][f"S{strategy.number}"] = {
                'value': incident.results[criteria][f"S{strategy.number}"],
                'strategy_name': strategy.name
            }

    for criteria in results.keys():
        results[criteria] = {k: v for k, v in sorted(results[criteria].items(),
                                                     key=lambda item: item[1]['value'])}

    return results