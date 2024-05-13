import base64
import json
import zlib

from incidents.models import Strategy


def prepare_results(incident):
    if incident.results is None:
        return {}
    results = {}

    strategies = Strategy.objects.filter(incident=incident).all()

    incident_results = dict_decode(incident.results)
    for criteria in incident_results.keys():
        results[criteria] = {}
        for strategy in strategies:
            results[criteria][f"S{strategy.number}"] = {
                'value': incident_results[criteria][f"S{strategy.number}"],
                'strategy_name': strategy.name,
            }

    for criteria in results.keys():
        results[criteria] = {
            k: v for k, v in sorted(
                results[criteria].items(),
                key=lambda item: item[1]['value'],
            )
        }

    return results


def dict_encode(data: str) -> str:
    return base64.b64encode(zlib.compress(json.dumps(data).encode())).decode()


def dict_decode(data: str) -> str:
    return json.loads(zlib.decompress(base64.b64decode(data)).decode())
