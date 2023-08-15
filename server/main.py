from fastapi import FastAPI
from starlette.responses import PlainTextResponse

from model.exception import NotFoundError, InvalidRequestError, UnauthorizedError
from routers import games, users

app = FastAPI()
app.include_router(games.router)
app.include_router(users.router)


@app.exception_handler(NotFoundError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=404)


@app.exception_handler(InvalidRequestError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.exception_handler(UnauthorizedError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=401)
