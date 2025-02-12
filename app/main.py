from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from fastapi.responses import JSONResponse
from pymystem3 import Mystem
from logger import init_logger

init_logger()
logging.getLogger().info("Lemmatizer run")
server = FastAPI()
mystem = Mystem()

class SentenceRequest(BaseModel):
    word: str

@server.post("/lemmatize")
def lemmatize(request: SentenceRequest):
    try:
        lemmas = mystem.lemmatize(request.word)
        return JSONResponse(content={'lemmatized': lemmas[0]})
    except Exception as error:
        logging.getLogger().error(f"Common error: {error}", exc_info=True)
        raise HTTPException(status_code=500, detail="Произошла ошибка при лемматизации")