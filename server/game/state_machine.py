from typing import Optional

from model.base import Game
from model.state_machine_model import StateMachine, State, ActionContext
from util.consts import STARTING_HAND_SIZE


class GameInitialState(State):

    def __init__(self, game: Game):
        self.game = game
        super().__init__("GAME_INITIALIZED")

    def evaluate(self, action_context: Optional[ActionContext]) -> str:
        for player in self.game.players:
            for i in range(STARTING_HAND_SIZE):
                player.add_to_hand(self.game.deck.draw())

        return "complete"


class StartTurnState(State):

    def __init__(self, game: Game):
        self.game = game
        super().__init__("START_TURN")

    def evaluate(self, action_context: Optional[ActionContext]) -> str:
        pass


class GameStateMachine(StateMachine):

    def __init__(self, game: Game):
        self.game = game

        states = [GameInitialState(game)]

        transitions = {
            "GAME_INITIALIZED": {
                "complete": "START_TURN"
            }
        }

        super().__init__(states, transitions, "GAME_INITIALIZED")