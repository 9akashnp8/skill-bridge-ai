from pydantic import BaseModel


class QuestionOptions(BaseModel):
    validate: bool
    re_gen: bool
    mock: bool


class Payload(BaseModel):
    topic: str
    options: QuestionOptions
