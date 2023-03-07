import os
from typing import Optional, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from models import db, Sheet

app = FastAPI()

if os.getenv('PRODUCTION') == 'no':
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


class Item(BaseModel):
    id: str
    link: str
    title: str
    abc: str
    abc_link: Optional[str]
    musicxml_link: Optional[str]
    has_midi: bool
    midi_link: Optional[str]

    class Config:
        orm_mode = True


class SearchResult(BaseModel):
    id: str
    title: str

    class Config:
        orm_mode = True


@app.get('/api/search/{word}', response_model=List[SearchResult])
def search(word: str):
    results = (db.query(Sheet.id, Sheet.title)
                 .filter(Sheet.title.ilike(f'%{word}%'))
                 .limit(15).all())
    return results


@app.get('/api/get/{item_id}', response_model=Item)
def get_an_item(item_id: str):
    sheet = db.query(Sheet).get(item_id)
    return sheet
