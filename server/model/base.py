from enum import Enum
from typing import List, Any

from pydantic import BaseModel


class CardType(Enum):
    PROPERTY = "property"
    ACTION = "action"


class Card(BaseModel):
    type: CardType


class PropertyCardFamily(BaseModel):
    color: str
    full_set: int
    rent: List[int]


class PropertyCard(Card):
    family: PropertyCardFamily
    name: str


class Deck(BaseModel):
    cards: List[Card]

    def add_card(self, card):
        self.cards.append(card)


class GamePlayer(BaseModel):
    id: str
    hand: List[Card]
    played_hand: List[Card]
    next_turn_count: int


class GameStatus(Enum):
    WAITING_FOR_PLAYERS = "waiting_for_players"
    STARTED = "started"
    COMPLETED = "completed"


class Game(BaseModel):
    id: str
    players: List[GamePlayer]
    status: GameStatus
