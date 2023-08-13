import json
from typing import Dict, List

from model.base import PropertyCardFamily, Deck, PropertyCard, CardType, PropertyWildcardCard, RentCard, MoneyCard


def read_deck_from_file() -> Deck:
    deck = Deck()

    with open("./data/deck.json", "r") as f:
        contents = f.read()
        data = json.loads(contents)
        families: Dict[str, PropertyCardFamily] = {}

        for json_family in data["families"]:
            family = PropertyCardFamily(**json_family)
            families[family.color] = family

        for json_card in data["cards"]:
            unique_id = json_card["unique_id"]
            card_type = json_card["type"]
            cash_value = json_card["cash_value"]

            if card_type == "property":
                family = families[json_card["family"]]
                name = json_card["name"]
                card = PropertyCard(
                    unique_id=unique_id, type=CardType.PROPERTY, cash_value=cash_value, family=family, name=name
                )
                deck.add_card(card)
            elif card_type == "property_wildcard":
                card_families: List[PropertyCardFamily] = []
                for family in json_card["families"]:
                    card_families.append(families[family])
                card = PropertyWildcardCard(
                    unique_id=unique_id, type=CardType.PROPERTY_WILDCARD, cash_value=cash_value, families=card_families
                )
                deck.add_card(card)
            elif card_type == "rent":
                card_families: List[PropertyCardFamily] = []
                for family in json_card["families"]:
                    card_families.append(families[family])
                card = RentCard(
                    unique_id=unique_id, type=CardType.RENT, cash_value=cash_value, families=card_families
                )
                deck.add_card(card)
            elif card_type == "money":
                card = MoneyCard(unique_id=unique_id, type=CardType.MONEY, cash_value=cash_value)
                deck.add_card(card)

    return deck


BASE_DECK = read_deck_from_file()