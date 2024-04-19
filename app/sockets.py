from re import L
import socketio

from .models.game import Game, Player
from .game_manager import manager


class GameNamespace(socketio.AsyncNamespace):
    async def on_connect(self, sid, environ):
        # Extract game ID and player ID from header
        game_id = environ.get("HTTP_GAME_ID")
        player_id = environ.get("HTTP_PLAYER_ID")

        if not game_id or not player_id:
            return False

        # Validate game ID
        game = manager.get_game(game_id)
        player = game.get_player(player_id)
        if not player or not game:
            print("Invalid Player or Game ", "Player: ", player, "Game: ", game)
            return False
        
        if player.is_connected():
            print("Player already connected")
            return False
        
        player.connected()
        await self.save_session(sid, {"game": game, "player": player})
        await self.enter_room(sid, game_id)
        await self.emit("player_joined", {"player_id": player_id}, room=game_id, skip_sid=sid)

        print(f"Socket.IO client {sid} connected to game room {game_id}")
    

    async def on_progress(self, sid, data):
        session = await self.get_session(sid)
        game: Game = session["game"]
        player: Player = session["player"]

        player_progress = int(data.get("progress"))
        game.update_progress(player.player_id, player_progress)
        print(f"Player {player.player_id} progress: {player_progress}")
        await self.emit("progress", {"player_id": player.player_id, "progress": player_progress}, room=game.game_id, skip_sid=sid)

    async def on_disconnect(self, sid):
        session = await self.get_session(sid)
        game: Game = session["game"]
        player:Player = session["player"]
        player.disconnected()

        game.remove_player(player.player_id)

        if game.is_game_empty():
            manager.remove_game(game.game_id)

        print(f"Socket.IO client {sid} disconnected from game room {game.game_id}")


# Create a socket.io server
sio_server = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[])

# Attach the GameNamespace to the socket.io server
sio_server.register_namespace(GameNamespace("/game"))

# Create an ASGI application with the socket.io server
sio_app = socketio.ASGIApp(socketio_server=sio_server, socketio_path="/ws")
