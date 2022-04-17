from typing import Dict

from core.db import Engine


class StatsRepository:
    COLLECTION = "stats"

    def __init__(self, db: Engine):
        self.db = db

    async def get_stats(self, user: str) -> Dict[str, int]:
        stats = await self.db.collection(self.COLLECTION).find_one({"user": user})
        return stats and stats["stats"] or {}

    async def save_stats(self, user: str, stats: Dict[str, int]):
        if await self.db.collection(self.COLLECTION).find_one({"user": user}):
            await self.db.collection(self.COLLECTION).update_one(
                {"user": user}, {"$set": {"stats": stats}}
            )
        else:
            await self.db.collection(self.COLLECTION).insert_one(
                {"user": user, "stats": stats}
            )
