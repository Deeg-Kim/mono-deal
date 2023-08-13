import random
from abc import abstractmethod
from enum import Enum
from typing import List

from pydantic import BaseModel

from model.exception import InvalidGameStateError


class CardType(Enum):
    PROPERTY = "property"
    ACTION = "action"


class Card(BaseModel):
    type: CardType
    cash_value: int

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError


class PropertyCardFamily(BaseModel):
    color: str
    full_set: int
    rent: List[int]


class PropertyCard(Card):
    family: PropertyCardFamily
    name: str

    def get_name(self):
        return self.name


class Deck(BaseModel):
    cards: List[Card]
    discard_pile: List[Card]

    def add_card(self, card: Card):
        self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards) == 0:
            if len(self.discard_pile) == 0:
                raise InvalidGameStateError("Deck is out of cards")
            self.cards = self.discard_pile.copy()
            self.discard_pile.clear()
            self.shuffle()

        return self.cards.pop(0)

    def discard(self, card: Card):
        self.discard_pile.append(card)


class GamePlayer(BaseModel):
    id: str
    hand: List[Card]
    played_hand: List[Card]
    next_turn_count: int

    def add_to_hand(self, card: Card):
        print(f"Adding [{card.get_name()}] to Player [{self.id}] hand")
        self.hand.append(card)


class GameStatus(Enum):
    WAITING_FOR_PLAYERS = "waiting_for_players"
    STARTED = "started"
    COMPLETED = "completed"


class Game(BaseModel):
    id: str
    players: List[GamePlayer]
    status: GameStatus
    deck: Deck
    current_player_idx: int = 0

    def get_current_player(self) -> GamePlayer:
        return self.players[self.current_player_idx]

    def to_next_player(self) -> None:
        if self.current_player_idx == len(self.players) - 1:
            self.current_player_idx = 0
        else:
            self.current_player_idx += 1
