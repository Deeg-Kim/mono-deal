from abc import ABC, abstractmethod
from typing import List

from model.base import Game, GameStatus
from model.exception import NotFoundError


class GamesDB(ABC):

    @abstractmethod
    def get_game(self, game_id: str) -> Game:
        raise NotImplementedError

    @abstractmethod
    def insert_game(self, game: Game):
        raise NotImplementedError

    @abstractmethod
    def update_game(self, game: Game):
        raise NotImplementedError

    @abstractmethod
    def get_games_by_status(self, game_status: GameStatus) -> List[Game]:
        raise NotImplementedError


class GamesDBInMemory(GamesDB):
    def __init__(self):
        super().__init__()
        self.memory = {}

    def get_game(self, game_id: str) -> Game:
        if game_id not in self.memory:
            raise NotFoundError(f"Could not find game with id {game_id}")

        return self.memory[game_id]

    def insert_game(self, game: Game):
        self.memory[game.id] = game

    def update_game(self, game: Game):
        if game.id not in self.memory:
            raise NotFoundError(f"Could not find game with id {game.id}")

        self.memory[game.id] = game

    def get_games_by_status(self, game_status: GameStatus) -> List[Game]:
        res = []

        for game in self.memory.values():
            if game.status == game_status:
                res.append(game)

        return res


games_db = GamesDBInMemory()


def get_games_db() -> GamesDB:
    return games_db
