import base64
import zlib
from incidents.models import Strategy
import json
def prepare_results(incident):
    if incident.results == None:
        return {}
    results = {}

    strategies = Strategy.objects.filter(incident=incident).all()
    
    incident_results = json.loads(zlib.decompress(base64.b64decode(incident.results)).decode())
    for criteria in incident_results.keys():
        results[criteria] = {}
        for strategy in strategies:
            results[criteria][f"S{strategy.number}"] = {
                'value': incident_results[criteria][f"S{strategy.number}"],
                'strategy_name': strategy.name
            }

    for criteria in results.keys():
        results[criteria] = {k: v for k, v in sorted(results[criteria].items(),
                                                     key=lambda item: item[1]['value'])}

    return results