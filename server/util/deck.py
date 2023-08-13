import json
from typing import Dict

from model.base import PropertyCardFamily, Deck, PropertyCard, CardType


def read_deck_from_file() -> Deck:
    deck = Deck(cards=[], discard_pile=[])

    with open("./data/deck.json", "r") as f:
        contents = f.read()
        data = json.loads(contents)
        families: Dict[str, PropertyCardFamily] = {}

        for json_family in data["families"]:
            family = PropertyCardFamily(**json_family)
            families[family.color] = family

        for json_card in data["cards"]:
            card_type = json_card["type"]

            if card_type == "property":
                family = families[json_card["family"]]
                name = json_card["name"]
                cash_value = json_card["cash_value"]
                card = PropertyCard(type=CardType.PROPERTY, cash_value=cash_value, family=family, name=name)
                deck.add_card(card)

    return deck


BASE_DECK = read_deck_from_file()