from typing import Optional

from model.base import Game
from model.state_machine_model import StateMachine, State, ActionContext
from util.consts import STARTING_HAND_SIZE, DRAW_PER_TURN


class GameInitialState(State):

    def __init__(self, game: Game):
        self.game = game
        super().__init__("GAME_INITIALIZED")

    def evaluate(self, action_context: Optional[ActionContext]) -> str:
        self.game.deck.shuffle()

        for player in self.game.players:
            for i in range(STARTING_HAND_SIZE):
                player.add_to_hand(self.game.deck.draw())

        return "complete"


class CurrentPlayerDrawState(State):

    def __init__(self, game: Game):
        self.game = game
        super().__init__("CURRENT_PLAYER_DRAW")

    def evaluate(self, action_context: Optional[ActionContext]) -> str:
        current_player = self.game.get_current_player()

        for i in range(DRAW_PER_TURN):
            current_player.add_to_hand(self.game.deck.draw())

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

        states = [GameInitialState(game), CurrentPlayerDrawState(game), StartTurnState(game)]

        transitions = {
            "GAME_INITIALIZED": {
                "complete": "CURRENT_PLAYER_DRAW"
            },
            "CURRENT_PLAYER_DRAW": {
                "complete": "START_TURN"
            }
        }

        super().__init__(states, transitions, "GAME_INITIALIZED")