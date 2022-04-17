from core.db import Engine


class DreamsRepository:
    COLLECTION = "dreams"

    def __init__(self, db: Engine):
        self.db = db

    async def save_dream(self, user: str, channel: str, dream: str):
        return await self.db.collection(self.COLLECTION).insert_one(
            {"user": user, "channel": channel, "dream": dream}
        )

    async def get_distinct_channels(self):
        return await self.db.collection(self.COLLECTION).distinct("channel")
