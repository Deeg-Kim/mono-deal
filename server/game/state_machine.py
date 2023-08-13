from model.base import Game, Deck


class GameStateMachine:

    def __init__(self, game: Game, deck: Deck):
        self.game = game
        self.deck = deck


