from core.db import Engine


class DreamsRepository:
    COLLECTION = "dreams"

    def __init__(self, db: Engine):
        self.db = db

    async def save_dream(self, user: str, dream: str):
        return await self.db.collection(self.COLLECTION).insert_one(
            {"user": user, "dream": dream}
        )
