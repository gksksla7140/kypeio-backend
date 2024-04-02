from fastapi import WebSocket, FastAPI, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List

app = FastAPI()


class Player:
    def __init__(self, player_id: int, name: str, websocket: WebSocket):
        self.player_id: int = player_id
        self.name: str = name
        self.websocket: WebSocket = websocket


class GameManager:
    def __init__(self):
        self.players: List[Player] = []

    async def add_player(self, player_id: int, name: str, websocket: WebSocket):
        await websocket.accept()
        player = Player(player_id, name, websocket)
        self.players.append(player)

    async def remove_player(self, websocket: WebSocket):
        self.players = [p for p in self.players if p.websocket != websocket]

    async def send_personal_message(self, player_id: int, message: str):
        player = next((p for p in self.players if p.player_id == player_id), None)
        if player:
            await player.websocket.send_text(message)

    async def broadcast(self, message: str):
        for player in self.players:
            await player.websocket.send_text(message)


game_manager = GameManager()

@app.get("/")
async def get():
    html = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Chat</title>
        </head>
        <body>
            <h1>WebSocket Chat</h1>
            <h2>Your ID: <span id="ws-id"></span></h2>
            <form action="" onsubmit="sendMessage(event)">
                <input type="text" id="messageText" autocomplete="off"/>
                <button>Send</button>
            </form>
            <ul id='messages'>
            </ul>
            <script>
                var client_id = Date.now()
                document.querySelector("#ws-id").textContent = client_id;
                var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
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
    return HTMLResponse(content=html, status_code=200)



@app.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: int):
    await game_manager.add_player(player_id, f"Player {player_id}", websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await game_manager.send_personal_message(player_id, f"You wrote: {data}")
            await game_manager.broadcast(f"Player {player_id} says: {data}")
    except WebSocketDisconnect:
        await game_manager.remove_player(websocket)
        await game_manager.broadcast(f"Player {player_id} left the game")
