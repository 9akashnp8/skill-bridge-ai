from typing import List, Any
from .client import collection


def parse_data(data):
    data["_id"] = str(data["_id"])
    return data


def get_topic_questions(topic: str):
    return [parse_data(question) for question in collection.find({"topic": topic})]


def insert_questions(topic: str, questions: List[Any]) -> bool:
    payload = [{"topic": topic, "question": question} for question in questions]
    result = collection.insert_many(payload)
    return len(result.inserted_ids) == len(payload)
