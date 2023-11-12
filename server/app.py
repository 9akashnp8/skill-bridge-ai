import asyncio
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from ai_engine import chain
from text_collector import get_material

app = FastAPI()


@app.get("/practice/questions")
async def get_root(topic: str):
    material = get_material(topic, mock=True)
    result = await asyncio.gather(
        *[chain.ainvoke({"topic": info.title, "info": info.info}) for info in material]
    )
    return JSONResponse(result)
