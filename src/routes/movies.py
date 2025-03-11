from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from src.schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema

DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 10
ROOT = "/theater"
router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
def list_movies(
        page: int = Query(DEFAULT_PAGE, ge=1),
        per_page: int = Query(DEFAULT_PER_PAGE, ge=1, le=20),
        db: Session = Depends(get_db)
) -> MovieListResponseSchema:

    offset = (page - 1) * per_page
    total_items = db.query(MovieModel).count()
    total_pages = math.ceil(total_items / per_page)

    next_page = f"{ROOT}/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None
    prev_page = f"{ROOT}/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None

    movies = db.query(MovieModel).limit(per_page).offset(offset).all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )


@router.get("/movies/{movie_id}", response_model=MovieDetailResponseSchema)
def get_movie(movie_id: int, db: Session = Depends(get_db)) -> MovieModel:
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
