import asyncio
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from ai_engine import chain
from text_collector import get_material

app = FastAPI()

@app.get("/practice/questions")
async def get_root(topic: str):
    material = get_material(topic, mock=True)
    infos = []
    for info in material:
        content = info["title"]
        content += "\n".join(i["content"] for i in info["children"])
        infos.append(content)
    result = await asyncio.gather(*[chain.ainvoke({"info": info}) for info in infos])
    return JSONResponse(result)
