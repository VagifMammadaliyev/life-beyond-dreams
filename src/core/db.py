from core import conf

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)


class Engine:
    def __init__(self, connection_url: str):
        self.client = AsyncIOMotorClient(connection_url)
        self.database_name = connection_url.split("/")[-1]
        self.db: AsyncIOMotorDatabase = self.client[self.database_name]

    def collection(self, collection_name: str) -> AsyncIOMotorCollection:
        return self.db[collection_name]


db_engine = Engine(conf.MONGO_CONNECTION_URL)
