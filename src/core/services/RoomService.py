from core.entities.GameRoom.AbstractGameRoom import AbstractGameRoom
from core.repository.RoomRepository.AbstractRoomRepository import AbstractRoomRepository


class RoomService:
    def __init__(self, game_room_repository):
        self.__game_room_repository: AbstractRoomRepository = game_room_repository

    def create_room(self, room_name: str, game_type: str) -> None:
        game_room = self.__game_room_repository.get_room(room_name)
        if not game_room:
            self.__game_room_repository.create_room(room_name, game_type)

    def get_room(self, room_name: str) -> AbstractGameRoom:
        return self.__game_room_repository.get_room(room_name)

    def add_player_to_room(self, room_name: str, player) -> None:
        self.__game_room_repository.add_player_to_room(room_name, player)
