import pytest
import requests

from snail_race_kata.adapters.race_result_provider_fake import RaceResultProviderFake
from snail_race_kata.adapters.race_result_provider_http import RaceResultProviderHttp
from snail_race_kata.domain.race_result_provider import Podium, Snail, SnailRace, SnailRaces


def test_explore_real_endpoint():
    response = requests.get('http://localhost:8000/results', timeout=5)
    response.raise_for_status()
    assert 'json' in response.headers['Content-Type']
    data = response.json()
    assert data['races']
    for race in data['races']:
        assert isinstance(race['raceId'], int)
        assert isinstance(race['timestamp'], int)
        assert len(race['snails']) >= 3
        assert all(isinstance(snail['duration'], (int, float)) for snail in race['snails'])


@pytest.fixture(params=['http', 'fake'])
def provider(request):
    if request.param == 'http':
        return RaceResultProviderHttp()
    podium = Podium(Snail(2, 'B'), Snail(3, 'C'), Snail(1, 'A'))
    return RaceResultProviderFake(SnailRaces().with_additional_result(1, 10000, podium))


def test_provider_contract(provider):
    results = provider.races()
    assert isinstance(results, SnailRaces)
    assert results.races
    assert results.get_last_race().timestamp == max(r.timestamp for r in results.races)
    for race in results.races:
        assert isinstance(race, SnailRace)
        assert isinstance(race.race_id, int)
        assert isinstance(race.timestamp, int)
        podium = race.podium
        snails = [podium.first, podium.second, podium.third]
        assert len({snail.number for snail in snails}) == 3
        assert all(isinstance(snail, Snail) and snail.name for snail in snails)


def test_http_maps_fastest_snails_in_order(monkeypatch):
    class Response:
        def raise_for_status(self):
            pass

        def json(self):
            return {'races': [{'raceId': 7, 'timestamp': 10000, 'snails': [
                {'number': 1, 'name': 'A', 'duration': 40},
                {'number': 2, 'name': 'B', 'duration': 10},
                {'number': 3, 'name': 'C', 'duration': 20},
                {'number': 4, 'name': 'D', 'duration': 30},
            ]}]}
    monkeypatch.setattr(requests, 'get', lambda *args, **kwargs: Response())
    race = RaceResultProviderHttp().races().get_last_race()
    assert race.race_id == 7
    assert race.timestamp == 10000
    assert race.podium == Podium(Snail(2, 'B'), Snail(3, 'C'), Snail(4, 'D'))


def test_http_propagates_failure(monkeypatch):
    def fail(*args, **kwargs):
        raise requests.ConnectionError('Unavailable')
    monkeypatch.setattr(requests, 'get', fail)
    with pytest.raises(requests.ConnectionError):
        RaceResultProviderHttp().races()


def test_empty_fake_and_latest_race():
    assert RaceResultProviderFake().races().get_last_race() is None
    podium = Podium(Snail(1, 'A'), Snail(2, 'B'), Snail(3, 'C'))
    races = SnailRaces().with_additional_result(1, 100, podium).with_additional_result(2, 200, podium)
    fake = RaceResultProviderFake(races)
    races.races.clear()
    first_read = fake.races()
    assert first_read.get_last_race().race_id == 2
    first_read.races.clear()
    assert len(fake.races().races) == 2
