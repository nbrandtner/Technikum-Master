import requests

from snail_race_kata.domain.race_result_provider import (
    Podium, RaceResultProvider, Snail, SnailRaces,
)


class RaceResultProviderHttp(RaceResultProvider):
    def __init__(self, url="http://localhost:8000/results"):
        self.url = url

    def races(self):
        response = requests.get(self.url, timeout=5)
        response.raise_for_status()
        results = SnailRaces()
        for race in response.json()["races"]:
            fastest = sorted(race["snails"], key=lambda snail: snail["duration"])[:3]
            podium = Podium(*(Snail(snail["number"], snail["name"])
                              for snail in fastest))
            results.with_additional_result(race["raceId"], race["timestamp"], podium)
        return results
