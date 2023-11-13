import asyncio
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from ai_engine import get_chain
from text_collector import get_topic_infos
from db import insert_questions, get_topic_questions

app = FastAPI()


@app.get("/practice/questions")
async def get_root(topic: str, validate: bool, mock: bool = True):
    questions = get_topic_questions(topic)
    if questions:
        return JSONResponse(questions)

    topic_infos = get_topic_infos(topic, mock=mock)
    chain = get_chain(validate)
    result = await asyncio.gather(
        *[
            chain.ainvoke({"topic": info.title, "info": info.info})
            for info in topic_infos
        ]
    )
    upload_result = insert_questions(topic, result)
    return JSONResponse({"upload": upload_result, "questions": result})
