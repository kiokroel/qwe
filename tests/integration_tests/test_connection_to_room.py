from fastapi.testclient import TestClient
from main import app

import json

client = TestClient(app)


def test_connection_to_room_positive():
    game_type = "gameWithFriend"
    room_name = "test_connection_to_room_positive"
    player_name_2 = "player_2"
    side_2 = "white"

    request_message_connect = {
        "jsonType": "roomConnectionRequest",
        "data": {
            "gameType": game_type,
            "room": {
                "roomName": room_name
            },
            "player": {
                "playerName": player_name_2,
                "playerSide": side_2
            }
        },
    }

    player_name = "player_1"
    side = "black"

    request_message_create = {
        "jsonType": "roomInitRequest",
        "data": {
            "gameType": game_type,
            "room": {
                "roomName": room_name
            },
            "player": {
                "playerName": player_name,
                "playerSide": side
            }
        },
    }

    json_request_message_create = json.dumps(request_message_create)
    json_request_message_connect = json.dumps(request_message_connect)

    room_connection_status = "successfully_connected"
    responce_message_connect = {
        "jsonType": "roomConnectionResponce",
        "data": {
            "gameType": game_type,
            "room": {
                    "roomName": room_name,
            },
            "roomConnectionStatus": room_connection_status,
            "players": {
                "roomCreator": {"name": player_name, "side": side, },
                "connectedPlayer": {"name": player_name_2, "side": side_2, },
            }
        },
    }

    with client.websocket_connect(f"api/chess/ws") as websocket:
        websocket.send_json(json_request_message_create)

        with client.websocket_connect(f"api/chess/ws") as websocket_1:
            websocket_1.send_json(json_request_message_connect)
            json_responce_message = websocket_1.receive_json()

        websocket_1.close()
        websocket.close()

    actual_responce_message = json.loads(json_responce_message)
    assert actual_responce_message["jsonType"] == responce_message_connect["jsonType"]
    assert actual_responce_message["data"] == responce_message_connect["data"]


def test_connection_to_room_negative():
    game_type = "gameWithFriend"
    room_name = "test_connection_to_room_negative"
    player_name = "player_2"
    side = "white"

    request_message_connect = {
        "jsonType": "roomConnectionRequest",
        "data": {
            "gameType": game_type,
            "room": {
                "roomName": room_name
            },
            "player": {
                "playerName": player_name,
                "playerSide": side
            }
        },
    }

    json_request_message_connect = json.dumps(request_message_connect)

    connection_status = "does not exists"
    responce_message_connect = {
        "jsonType": "roomConnectionResponce",
        "data": {
            "gameType": game_type,
            "room": {
                "roomName": room_name,
            },
            "roomConnectionStatus": connection_status,
            "players": {
                "roomCreator": None,
                "connectedPlayer": None
            }
        },
    }

    with client.websocket_connect(f"api/chess/ws") as websocket:
        websocket.send_json(json_request_message_connect)
        json_responce_message = websocket.receive_json()

        websocket.close()

    actual_responce_message = json.loads(json_responce_message)
    assert actual_responce_message["jsonType"] == responce_message_connect["jsonType"]
    assert actual_responce_message["data"] == responce_message_connect["data"]
