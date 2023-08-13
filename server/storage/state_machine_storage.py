from typing import Dict

from game.state_machine import GameStateMachine
from model.base import Game


class StateMachineStorage:

    def __init__(self):
        self.game_state_machines: Dict[str, GameStateMachine] = {}

    def start_new_game(self, game: Game):
        state_machine = GameStateMachine(game)
        self.game_state_machines[game.id] = state_machine

    def get_game_state_machine(self, game_id: str) -> GameStateMachine:
        return self.game_state_machines[game_id]


state_machine_storage = StateMachineStorage()


def get_state_machine_storage() -> StateMachineStorage:
    return state_machine_storage
