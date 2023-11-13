from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from decouple import config

user = config("MONGODB_USER")
password = config("MONGODB_PASSWORD")
mongo_url = config("MONGODB_URL")
uri = f"mongodb+srv://{user}:{password}@{mongo_url}/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi("1"))
db = client["skill-bridge-ai-db"]
collection = db["topic-questions-collection"]

try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
