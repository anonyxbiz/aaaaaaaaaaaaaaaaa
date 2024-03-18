# slangai
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from checkdata import define
from ac import Gss
from os import system as o

p = print

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SlangAI(BaseModel):
    keyword: str

def sanitize(keyword):
    question_synonyms = ["what ", "who ", "a ", "how ", "is ", "the ", "?", "how to ", "why is "]
    stop_words = ["to ", "and ", "in ", "on ", "for ", "with ", "about ", "of ", "that ", "from ", "by ", "at ", "an ", "as ", "are ", "were ", "is ", "am ", "it ", "its ", "it's ", "they ", "them ", "he ", "him ", "she ", "her ", "you ", "your ", "we ", "us ", "our ", "his ", "some ", "their "]
    for synonym in question_synonyms:
        keyword = keyword.lower().replace(synonym, '').strip()
    for sw in stop_words:
        keyword = keyword.lower().replace(sw, '').strip()
    return keyword

@app.post("/SlangAI/")
async def SlangAI(request_data: SlangAI):
    try:
        keyword = sanitize(request_data.keyword)
        answer = define(keyword)
        if answer:
            answer = {'SlangAI': answer}

        elif not answer:
            answer = Gss(keyword)
            answer = {
                'SlangAI': answer,
            }

        return answer
    except Exception as e:
        raise HTTPException(status_code=404, detail='Not Found')

if __name__ == "__main__":
    try:
        o('cls')
    except:
        pass

    uvicorn.run("slangai:app", host="127.0.0.1", port=8000, reload=True)

