import pytest

from snail_race_kata.adapters.bet_repository_fake import BetRepositoryFake
from snail_race_kata.adapters.race_result_provider_fake import RaceResultProviderFake
from snail_race_kata.domain.bet import Bet
from snail_race_kata.domain.bet_application import BetApplication
from snail_race_kata.domain.podium_pronostic import PodiumPronostic
from snail_race_kata.domain.race_result_provider import Podium, Snail, SnailRaces
from snail_race_kata.domain.winner import Winner


def application(previous=True):
    podium = Podium(Snail(1, 'A'), Snail(2, 'B'), Snail(3, 'C'))
    races = SnailRaces()
    if previous:
        races.with_additional_result(1, 10000, podium)
    races.with_additional_result(2, 20000, podium)
    return BetApplication(BetRepositoryFake(), RaceResultProviderFake(races))


def test_registers_complete_bet():
    app = application()
    app.place_bet('Alice', 15000, 1, 2, 3)
    assert app.bet_repository.find_by_date_range(0, 20000) == [
        Bet('Alice', PodiumPronostic(1, 2, 3), 15000)]


@pytest.mark.parametrize('timestamp,wins', [
    (9999, False), (10000, False), (10001, True),
    (16999, True), (17000, True), (17001, False),
    (20000, False), (21000, False),
])
def test_time_boundaries(timestamp, wins):
    app = application()
    app.place_bet('Alice', timestamp, 1, 2, 3)
    assert app.get_winners_for_last_race() == ([Winner('Alice')] if wins else [])


@pytest.mark.parametrize('prediction', [(2, 1, 3), (1, 3, 2), (1, 2, 4)])
def test_requires_exact_podium(prediction):
    app = application()
    app.place_bet('Alice', 15000, *prediction)
    assert app.get_winners_for_last_race() == []


def test_multiple_winners_and_losing_bet():
    app = application()
    app.place_bet('Alice', 15000, 1, 2, 3)
    app.place_bet('Bob', 16000, 1, 2, 3)
    app.place_bet('Charlie', 16000, 3, 2, 1)
    assert app.get_winners_for_last_race() == [Winner('Alice'), Winner('Bob')]


def test_no_bets_or_races():
    assert application().get_winners_for_last_race() == []
    app = BetApplication(BetRepositoryFake(), RaceResultProviderFake())
    app.place_bet('Alice', 100, 1, 2, 3)
    assert app.get_winners_for_last_race() == []


def test_first_race_has_no_previous_lower_boundary():
    app = application(previous=False)
    app.place_bet('Alice', 1000, 1, 2, 3)
    assert app.get_winners_for_last_race() == [Winner('Alice')]
