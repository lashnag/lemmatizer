import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from logger import init_logger, request_headers
from pymorphy3 import MorphAnalyzer
import spacy

init_logger()
logging.getLogger().info("Lemmatizer run")
server = FastAPI()

morph_ru = MorphAnalyzer()
nlp_en = spacy.load("en_core_web_sm")
nlp_es = spacy.load("es_core_news_sm")

SUPPORTED_LANGUAGES = {"ru", "en", "es"}

@server.post("/lemmatize")
async def lemmatize(request: Request):
    request_headers.set(dict(request.headers))
    try:
        body = await request.json()
        word = body.get("word")
        language = body.get("language")
        if not isinstance(word, str) or not word:
            raise ValueError("word must be a non-empty string")
        if not isinstance(language, str) or language not in SUPPORTED_LANGUAGES:
            raise ValueError(f"language must be one of: {sorted(SUPPORTED_LANGUAGES)}")
        lemma = lemmatize_word(word, language)
        return JSONResponse(content={'lemmatized': lemma})
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        logging.getLogger().error(f"Common error: {error}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Lemmatization error: {error}")

def lemmatize_word(word: str, language: str) -> str:
    if language == "ru":
        return morph_ru.parse(word)[0].normal_form
    elif language == "en":
        return nlp_en(word)[0].lemma_
    elif language == "es":
        return nlp_es(word)[0].lemma_

@server.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}