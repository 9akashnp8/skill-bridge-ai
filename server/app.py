import asyncio
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from ai_engine import chain
from text_collector import get_topic_infos

app = FastAPI()


@app.get("/practice/questions")
async def get_root(topic: str):
    topic_infos = get_topic_infos(topic, mock=True)
    result = await asyncio.gather(
        *[
            chain.ainvoke({"topic": info.title, "info": info.info})
            for info in topic_infos
        ]
    )
    return JSONResponse(result)
