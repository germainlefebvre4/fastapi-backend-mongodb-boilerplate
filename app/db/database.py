from pymongo import MongoClient
from app.core.config import settings

def get_default_bucket():
    client = MongoClient(settings.MONGODB_CONNECTION_STRING)
    return client[settings.MONGODB_DATABASE]
