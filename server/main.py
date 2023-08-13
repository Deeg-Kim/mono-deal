from fastapi import FastAPI
from starlette.responses import PlainTextResponse

from model.exception import NotFoundError, InvalidRequestError
from routers import games
from util.deck import read_deck_from_file

app = FastAPI()
app.include_router(games.router)

read_deck_from_file()

@app.exception_handler(NotFoundError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=404)

@app.exception_handler(InvalidRequestError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)
