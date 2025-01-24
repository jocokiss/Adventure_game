from pymongo import MongoClient
from src.utilities.api_actions import GameAPIClient


class MongoDBManager:
    def __init__(self):
        self.uri = GameAPIClient().get_mongo_token()
        self.client = MongoClient(self.uri)
        self.db = self.client['AdventureGame']

    def insert_batch(self, collection_name, data: list[dict]):
        """
        Insert multiple documents into a MongoDB collection.

        Args:
            collection_name (str): The name of the collection.
            data (list): List of dictionaries to insert.

        Returns:
            InsertManyResult: Result of the insert operation.
        """
        if data:
            collection = self.db[collection_name]
            result = collection.insert_many(data)
            return result
        self.close_connection()

    def close_connection(self):
        """Close the MongoDB connection."""
        self.client.close()


if __name__ == "__main__":
    db = MongoDBManager()
    db.insert_batch('MovementData', [{
        'coordinates': '(0, 0)',
        'time_spent': 6,
    }])
