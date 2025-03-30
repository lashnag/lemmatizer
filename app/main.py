import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from logger import init_logger, request_headers
from pymorphy2 import MorphAnalyzer

init_logger()
logging.getLogger().info("Lemmatizer run")
server = FastAPI()
morph = MorphAnalyzer()

@server.post("/lemmatize")
async def lemmatize(request: Request):
    request_headers.set(dict(request.headers))
    try:
        body = await request.json()
        lemma = lemmatize_word(body.get("word"))
        return JSONResponse(content={'lemmatized': lemma})
    except Exception as error:
        logging.getLogger().error(f"Common error: {error}", exc_info=True)
        raise HTTPException(status_code=500, detail="Произошла ошибка при лемматизации")

def lemmatize_word(word: str):
    parsed = morph.parse(word)[0]
    return parsed.normal_form

@server.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}