from typing import List

from snail_race_kata.domain.winner import Winner
from snail_race_kata.domain.bet import Bet
from snail_race_kata.domain.podium_pronostic import PodiumPronostic


class BetApplication:
    def __init__(self, bet_repository, race_result_provider):
        self.bet_repository = bet_repository
        self.race_result_provider = race_result_provider

    def place_bet(
        self, gambler: str, timestamp: int, first: int, second: int, third: int
    ) -> None:
        self.bet_repository.register(
            Bet(gambler, PodiumPronostic(first, second, third), timestamp)
        )

    def get_winners_for_last_race(self) -> List[Winner]:
        races = self.race_result_provider.races()
        last_race = races.get_last_race()
        if last_race is None:
            return []

        previous_timestamps = [race.timestamp for race in races.races
                               if race.timestamp < last_race.timestamp]
        # Millisecond timestamps: a bet at the previous race belongs to a later race.
        start = max(previous_timestamps) + 1 if previous_timestamps else 0
        cutoff = last_race.timestamp - 3000
        podium = last_race.podium
        expected = PodiumPronostic(podium.first.number, podium.second.number,
                                   podium.third.number)
        return [Winner(bet.gambler)
                for bet in self.bet_repository.find_by_date_range(start, cutoff)
                if bet.pronostic == expected]
