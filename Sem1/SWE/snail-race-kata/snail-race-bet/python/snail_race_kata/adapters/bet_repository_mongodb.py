from typing import List

from dataclasses import asdict
from pymongo.database import Database
from snail_race_kata.domain.bet_repository import BetRepository

from snail_race_kata.domain.bet import Bet
from snail_race_kata.domain.podium_pronostic import PodiumPronostic


class BetRepositoryMongoDb(BetRepository):
    def __init__(self, database: Database):
        self.database = database

    def register(self, bet: Bet) -> None:
        self._get_collection().insert_one(asdict(bet))

    def find_by_date_range(self, from_timestamp: int, to_timestamp: int) -> List["Bet"]:
        documents = self._get_collection().find(
            {"timestamp": {"$gte": from_timestamp, "$lte": to_timestamp}}
        )
        return [Bet(item["gambler"], PodiumPronostic(**item["pronostic"]),
                    item["timestamp"]) for item in documents]

    def _get_collection(self):
        return self.database.get_collection("bets")
