import os
from datetime import datetime

from Clients import MijnAfvalWijzerClient, MongoDBClient
from dotenv import load_dotenv

load_dotenv()


class TrashCanClient:
    def __init__(self):
        self.client = MijnAfvalWijzerClient(
            api_key=os.getenv("MIJN_AFVAL_WIJZER_API_KEY")
        )
        self.database_client = MongoDBClient()

    def get_collection_key(self, zip_code: str, house_number: str, add_on: str):
        zip_code = zip_code.replace(" ", "-")
        return f"{zip_code}-{house_number}-{add_on}"

    def is_date_in_the_past(self, date_str):
        try:
            given_date = datetime.strptime(date_str, '%Y-%m-%d')
            current_date = datetime.now()
            return given_date < current_date
        except ValueError:
            # The string is not a valid date format
            return False

    def get_data_from_api(self, collection, zip_code: str, house_number: str, add_on: str):
        data = self.client.get_data(zip_code, house_number, add_on)

        for item in data:
            if self.is_date_in_the_past(item["date"]):
                continue

            collection.update_one(
                {"_id": item["date"] + "|" + item["type"]},
                {"$set": {"type": item["type"], "date": item["date"]}},
                upsert=True
            )
        return collection

    def get_data(self, zip_code: str, house_number: str, add_on: str):
        # find or create collection
        collection = self.database_client.get_db()[self.get_collection_key(
            zip_code, house_number, add_on
        )]
        if collection.count_documents({}) < os.getenv("MINIMUM_COLLECTION_SIZE", 6):
            collection = self.get_data_from_api(
                collection, zip_code, house_number, add_on
            )

        return list(collection.find())

    def cleanup(self):
        try:
            collections = self.database_client.get_db().list_collection_names()
            for collection in collections:
                if self.database_client.get_db()[collection].count_documents({}):
                    self.cleanup_collection(collection)
        except Exception as e:
            raise "Error cleaning up the database: {}".format(e)

    def cleanup_collection(self, collection):
        for item in self.database_client.get_db()[collection].find():
            if self.is_date_in_the_past(item["date"]):
                self.database_client.get_db()[collection].delete_one(
                    {"_id": item["date"] + "|" + item["type"]}
                )
