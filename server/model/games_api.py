from pydantic import BaseModel


class AddPlayerRequest(BaseModel):
    player_id: str
