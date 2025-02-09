from fastapi import FastAPI
from pydantic import BaseModel
import logging
from fastapi.responses import JSONResponse
from pymystem3 import Mystem

logging.getLogger().info("Lemmatizer run")
server = FastAPI()
mystem = Mystem()

class SentenceRequest(BaseModel):
    word: str

@server.post("/lemmatize")
def lemmatize(request: SentenceRequest):
    lemmas = mystem.lemmatize(request.word)
    return JSONResponse(content={'lemmatized': lemmas[0]})