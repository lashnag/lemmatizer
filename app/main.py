import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pymystem3 import Mystem
from logger import init_logger, request_headers

init_logger()
logging.getLogger().info("Lemmatizer run")
server = FastAPI()
mystem = Mystem()

@server.post("/lemmatize")
async def lemmatize(request: Request):
    request_headers.set(dict(request.headers))
    try:
        body = await request.json()
        lemmas = mystem.lemmatize(body.get("word"))
        return JSONResponse(content={'lemmatized': lemmas[0]})
    except Exception as error:
        logging.getLogger().error(f"Common error: {error}", exc_info=True)
        raise HTTPException(status_code=500, detail="Произошла ошибка при лемматизации")

@server.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}