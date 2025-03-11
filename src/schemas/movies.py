from datetime import date
from typing import Optional, List

from pydantic import BaseModel, Configdict


class MovieDetailResponseSchema(BaseModel):
    id : int
    name : str
    date : date
    score : int
    genre : str
    overview : str
    crew : str
    orig_title : str
    status : str
    orig_lang : str
    budget : int
    revenue : int
    country : str

    model_config = Configdict(from_atributes=True)


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page : Optional[str]
    next_page = Optional[str]
    total_pages = int
    total_items = int
