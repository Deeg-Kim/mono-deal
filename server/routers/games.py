import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from model.base import Game
from storage.game_db import GamesDB, get_games_db

router = APIRouter(prefix="/game")


@router.post("", name="New Game", description="Initialize a new game")
async def new_game(
        games_db: Annotated[GamesDB, Depends(get_games_db)]
):
    game_id = str(uuid.uuid4())
    game = Game(id=game_id, players=[])

    games_db.insert_game(game)

    return game


@router.put("/{id}/players", name="Add player", description="Add player to an existing game")
async def add_player(
        id: str,
        games_db: Annotated[GamesDB, Depends(get_games_db)]
):
    game = games_db.get_game(id)

