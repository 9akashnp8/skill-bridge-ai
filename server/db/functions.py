import itertools
from typing import List, Any
from .client import collection


def parse_data(data):
    data["_id"] = str(data["_id"])
    return data


def get_topic_questions(topic: str):
    return [parse_data(question) for question in collection.find({"topic": topic})]


def format_response(topic, ai_response):
    questions = list(itertools.chain.from_iterable(ai_response))
    return [{"topic": topic, "question": question} for question in questions]


def insert_questions(questions: List[Any]) -> bool:
    result = collection.insert_many(questions)
    return len(result.inserted_ids) == len(questions)
