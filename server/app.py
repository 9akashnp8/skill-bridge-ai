import asyncio
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from models import Payload
from ai_engine import get_chain
from text_collector import get_topic_infos
from db import insert_questions, get_topic_questions

app = FastAPI()


@app.post("/practice/questions")
async def get_root(payload: Payload):
    topic = payload.topic
    options = payload.options

    questions = get_topic_questions(topic)
    if questions and not options.re_gen:
        return JSONResponse(questions)

    topic_infos = get_topic_infos(topic, mock=options.mock)
    chain = get_chain(options.validate)
    result = await asyncio.gather(
        *[
            chain.ainvoke({"topic": info.title, "info": info.info})
            for info in topic_infos
        ]
    )
    upload_result = insert_questions(topic, result)
    return JSONResponse({"upload": upload_result, "questions": result})
