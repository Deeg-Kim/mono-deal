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


class Game(BaseModel):
    id: str
    players: List[GamePlayer]
