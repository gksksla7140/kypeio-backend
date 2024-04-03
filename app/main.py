from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from app.models import game
from .game_manager import GameManager
from .models import Player, JoinRequest, CreateRequest
from .utils import generate_game_id

app = FastAPI()
manager = GameManager()


@app.post("/create_game/")
async def create_game(create_request: CreateRequest):
    game_id = generate_game_id()
    while game_id in manager.games:
        game_id = generate_game_id()

    manager.create_game(create_request.host_id, "TestGame")

    return {"message": "Game created", "game_id": game_id}


@app.websocket("/ws/{game_id}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str, player_id: str):
    await websocket.accept()

    player = Player(player_id=player_id, websocket=websocket)

    try:
        manager.add_player_to_game(game_id, player)
    except ValueError as e:
        await websocket.send_text(str(e))
        return

    await manager.broadcast_to_game(game_id)

    try:
        while True:
            data = await websocket.receive_text()
            manager.games[game_id].type_character(player_id, data)
            await manager.games[game_id].broadcast()
    except WebSocketDisconnect:
        websocket.close()
        manager.remove_player_from_game(game_id, player_id)
        await manager.games[game_id].broadcast()


html = """
<!DOCTYPE html>
<html>
<head>
    <title>TypeRacer Game</title>
</head>
<body>
    <h1>TypeRacer Game</h1>
    <h2 id="game-name">Game Name</h2>
    <div>
        <h3>Text Events:</h3>
        <ul id="messages"></ul>
    </div>
    <div>
        <h3>JSON Events:</h3>
        <ul id="json-events"></ul>
    </div>
    <form onsubmit="sendMessage(event); return false;">
        <input type="text" id="messageText" autocomplete="off"/>
        <button>Send</button>
    </form>
    <script>
        var client_id = Math.floor(Math.random() * 1000000);
        var ws = new WebSocket(`ws://localhost:8000/ws/TestGame/${client_id}`);
        ws.onmessage = function(event) {
            var data = JSON.parse(event.data);
            if (data.type === "progress") {
                document.getElementById('progress').innerText = "Your progress: " + data.progress;
            } else {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(data.message)
                message.appendChild(content)
                messages.appendChild(message)
            }
        };
        function sendMessage(event) {
            var input = document.getElementById("messageText")
            ws.send(input.value)
            input.value = ''
            event.preventDefault()
        }
    </script>
</body>
</html>


"""


@app.get("/")
async def get():
    return HTMLResponse(content=html, status_code=200)
