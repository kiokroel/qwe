from pydantic import BaseModel, Field

from core.schemas.Player import Player
from core.schemas.Room import Room
from core.schemas.mixins.ErrorsMixin import ErrorsMixin
from core.schemas.mixins.JsonTypeStrMixin import JsonTypeStrMixin
from core.schemas.mixins.SystemMessageMixin import SystemMessagesMixin


class Players(BaseModel):
    players: dict[str, Player] = None


class RoomConnectionResponceData(BaseModel):
    game_type: str = Field(alias="gameType")
    room: Room
    room_connection_status: str = Field(alias="roomConnectionStatus")
    players: Players


class RoomConnectionResponce(JsonTypeStrMixin, SystemMessagesMixin, ErrorsMixin):
    data: RoomConnectionResponceData
