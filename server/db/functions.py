import json
from typing import List, Any
from .client import collection


def get_topic_questions(topic: str):
    return json.dumps(
        [question for question in collection.find({"topic": topic})], default=str
    )


def insert_questions(topic: str, questions: List[Any]) -> bool:
    payload = [{"topic": topic, "question": question} for question in questions]
    result = collection.insert_many(payload)
    return len(result.inserted_ids) == len(payload)
