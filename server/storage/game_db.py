from abc import ABC, abstractmethod

from model.base import Game
from model.exception import NotFoundError


class GamesDB(ABC):

    @abstractmethod
    def get_game(self, game_id: str):
        raise NotImplementedError

    @abstractmethod
    def insert_game(self, game: Game):
        raise NotImplementedError

    @abstractmethod
    def update_game(self, game: Game):
        raise NotImplementedError


class GamesDBInMemory(GamesDB):
    def __init__(self):
        super().__init__()
        self.memory = {}

    def get_game(self, game_id: str):
        if game_id not in self.memory:
            raise NotFoundError(f"Could not find game with id {game_id}")

        return self.memory[game_id]

    def insert_game(self, game: Game):
        self.memory[game.id] = game

    def update_game(self, game: Game):
        if game.id not in self.memory:
            raise NotFoundError(f"Could not find game with id {game.id}")

        self.memory[game.id] = game


games_db = GamesDBInMemory()


def get_games_db() -> GamesDB:
    return games_db
