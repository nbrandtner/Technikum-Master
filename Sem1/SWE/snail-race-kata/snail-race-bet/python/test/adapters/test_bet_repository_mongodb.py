import uuid

import pytest
from pymongo import MongoClient

from snail_race_kata.adapters.bet_repository_fake import BetRepositoryFake
from snail_race_kata.adapters.bet_repository_mongodb import BetRepositoryMongoDb
from snail_race_kata.domain.bet import Bet
from snail_race_kata.domain.podium_pronostic import PodiumPronostic


@pytest.fixture(params=['fake', 'mongodb'])
def repository(request):
    if request.param == 'fake':
        yield BetRepositoryFake()
        return
    client = MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=3000)
    database = client['kata_contract_' + uuid.uuid4().hex]
    try:
        client.admin.command('ping')
        yield BetRepositoryMongoDb(database)
    finally:
        client.drop_database(database.name)
        client.close()


def make_bet(timestamp, gambler='Alice'):
    return Bet(gambler, PodiumPronostic(1, 2, 3), timestamp)


def test_register_and_retrieve(repository):
    bet = make_bet(100)
    repository.register(bet)
    assert repository.find_by_date_range(0, 200) == [bet]


def test_range_includes_both_boundaries(repository):
    for timestamp in [99, 100, 150, 200, 201]:
        repository.register(make_bet(timestamp))
    assert sorted(b.timestamp for b in repository.find_by_date_range(100, 200)) == [100, 150, 200]


def test_empty_and_reversed_range(repository):
    assert repository.find_by_date_range(0, 100) == []
    repository.register(make_bet(50))
    assert repository.find_by_date_range(100, 0) == []


def test_multiple_bets_at_same_timestamp(repository):
    repository.register(make_bet(100, 'Alice'))
    repository.register(make_bet(100, 'Bob'))
    assert sorted(b.gambler for b in repository.find_by_date_range(100, 100)) == ['Alice', 'Bob']


def test_storage_and_reads_are_independent_of_mutation(repository):
    bet = make_bet(100)
    repository.register(bet)
    bet.pronostic.first = 9
    retrieved = repository.find_by_date_range(0, 200)
    assert retrieved == [make_bet(100)]
    retrieved[0].gambler = 'Changed'
    assert repository.find_by_date_range(0, 200) == [make_bet(100)]
