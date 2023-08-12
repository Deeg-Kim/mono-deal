import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from model.base import Game, GamePlayer
from model.exception import InvalidRequestError
from model.games_api import AddPlayerRequest
from storage.game_db import GamesDB, get_games_db
from util.consts import MAX_PLAYERS_PER_GAME

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
        body: AddPlayerRequest,
        games_db: Annotated[GamesDB, Depends(get_games_db)]
) -> Game:
    game = games_db.get_game(id)

    if len(game.players) >= MAX_PLAYERS_PER_GAME:
        raise InvalidRequestError(f"Cannot have more than {MAX_PLAYERS_PER_GAME} players per game")

    player = GamePlayer(id=body.player_id, hand=[], played_hand=[])
    game.players.append(player)
    games_db.update_game(game)

    return game
