from copy import deepcopy

from snail_race_kata.domain.race_result_provider import RaceResultProvider, SnailRaces


class RaceResultProviderFake(RaceResultProvider):
    def __init__(self, results=None):
        self._results = deepcopy(results if results is not None else SnailRaces())

    def races(self):
        return deepcopy(self._results)
