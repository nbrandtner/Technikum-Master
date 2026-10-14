# Completed Python kata

## Run

From the Python project folder, with MongoDB on localhost:27017 and the snail race server on localhost:8000:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Verified: 33 tests passed, including the live MongoDB and HTTP checks.

## Implementation

- BetRepositoryMongoDb implements BetRepository and stores the gambler, prediction and timestamp as a MongoDB document.
- BetRepositoryFake implements the same interface using memory. Both run the same parametrized repository contract tests, including inclusive date boundaries and independent stored copies.
- RaceResultProviderHttp calls /results, checks HTTP errors, sorts snails by duration and maps the fastest three into the domain podium. It uses a five-second network timeout.
- RaceResultProviderFake returns configured domain results. HTTP and fake adapters run the same domain contract checks. An exploratory test checks the real endpoint; a deterministic HTTP mapping test verifies podium ordering independently of changing live results.
- BetApplication registers bets and lists winners using these interfaces. Business tests use the fakes and do not need external services.
- SnailRaces.get_last_race selects the greatest timestamp rather than relying on list order.

## Time rules and assumptions

The real server uses Unix timestamps in milliseconds. A winning prediction must match first, second and third exactly, and must have been registered at or before race timestamp minus 3000.

For the last race, bets must be strictly after the previous race timestamp. A bet at the previous race timestamp is excluded; the instructions do not define simultaneous-event ordering, so this boundary is an explicit convention. Without a previous result, nonnegative timestamps up to the cutoff are considered.

The server returns a limited race history. Determining whether a bet belongs to the latest race assumes that its immediately preceding race is present. Winners are returned per winning bet; multiple winning bets by one gambler produce multiple entries.

## Files

The domain contains the application, models and abstract ports. The adapters contain MongoDB, HTTP and in-memory implementations. Tests cover shared adapter contracts, actual infrastructure, HTTP mapping and failures, plus the application rules and their time boundaries.

The original test_requirements_check.py is preserved. Repository contract tests use uniquely named temporary databases and remove them afterward; they do not clear an existing user database.
