import uuid
from typing import Annotated, Dict, Set

from fastapi import APIRouter, Depends

from model.base import Game, GamePlayer, GameStatus
from model.exception import InvalidRequestError
from model.games_api import AddPlayerRequest
from storage.game_db import GamesDB, get_games_db
from storage.state_machine_storage import StateMachineStorage, get_state_machine_storage
from util.consts import MAX_PLAYERS_PER_GAME, DEFAULT_TURN_COUNT
from util.deck import BASE_DECK

router = APIRouter(prefix="/game")


ALLOWED_GAME_STATUS_TRANSITIONS: Dict[GameStatus, Set[GameStatus]] = {
    GameStatus.WAITING_FOR_PLAYERS: {GameStatus.STARTED},
    GameStatus.STARTED: {GameStatus.COMPLETED}
}


@router.post("", name="New Game", description="Initialize a new game")
async def new_game(
        games_db: Annotated[GamesDB, Depends(get_games_db)]
) -> Game:
    game_id = str(uuid.uuid4())
    game = Game(id=game_id, players=[], status=GameStatus.WAITING_FOR_PLAYERS, deck=BASE_DECK.copy())

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

    player = GamePlayer(id=body.player_id, hand=[], played_hand=[], next_turn_count=DEFAULT_TURN_COUNT)
    game.players.append(player)
    games_db.update_game(game)

    return game


@router.post("/{id}/status", name="Change a game status", description="Change a game status")
async def start_game(
        id: str,
        to: GameStatus,
        games_db: Annotated[GamesDB, Depends(get_games_db)],
        state_machine_storage: Annotated[StateMachineStorage, Depends(get_state_machine_storage)]
) -> Game:
    game = games_db.get_game(id)

    if to not in ALLOWED_GAME_STATUS_TRANSITIONS.get(game.status):
        raise InvalidRequestError(f"Cannot transition from {game.status} to {to}")

    game.status = to
    games_db.update_game(game)

    if to == GameStatus.STARTED:
        state_machine_storage.start_new_game(game)
        state_machine_storage.get_game_state_machine(game.id).action()

    return game


@router.post("/{id}/turn", name="Take turn", description="Start a player turn")
async def start_turn(
        id: str,
        games_db: Annotated[GamesDB, Depends(get_games_db)],
        state_machine_storage: Annotated[StateMachineStorage, Depends(get_state_machine_storage)]
) -> Game:
    game = games_db.get_game(id)
    state_machine_storage.get_game_state_machine(game.id).action()

    return game


@router.post("/{id}/action", name="Take action", description="Reflect a player action")
async def take_turn(
        id: str,
        games_db: Annotated[GamesDB, Depends(get_games_db)],
) -> Game:
    pass


@router.get("/{id}/player/{player_id}", name="Get player hand", description="Get a player's hand within a hand")
async def start_game(
        id: str,
        player_id: str,
        games_db: Annotated[GamesDB, Depends(get_games_db)]
) -> GamePlayer:
    game = games_db.get_game(id)
    return game.get_player_by_id(player_id)
