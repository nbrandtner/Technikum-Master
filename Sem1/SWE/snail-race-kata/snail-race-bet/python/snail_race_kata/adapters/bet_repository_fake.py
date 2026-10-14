from copy import deepcopy

from snail_race_kata.domain.bet_repository import BetRepository


class BetRepositoryFake(BetRepository):
    def __init__(self):
        self._bets = []

    def register(self, bet):
        self._bets.append(deepcopy(bet))

    def find_by_date_range(self, from_timestamp, to_timestamp):
        return deepcopy([bet for bet in self._bets
                         if from_timestamp <= bet.timestamp <= to_timestamp])
