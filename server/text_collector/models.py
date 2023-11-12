from pydantic import BaseModel


class TopicInfo(BaseModel):
    id: str
    title: str
    info: str
