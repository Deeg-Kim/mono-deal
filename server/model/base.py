from enum import Enum
from typing import List

from pydantic import BaseModel


class CardType(Enum):
    PROPERTY = 1
    ACTION = 2


class Card(BaseModel):
    type: CardType


class GamePlayer(BaseModel):
    id: str
    hand: List[Card]
    played_hand: List[Card]


class Game(BaseModel):
    id: str
    players: List[GamePlayer]
