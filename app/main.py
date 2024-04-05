from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import game

from .game_manager import GameManager
from .models import Player, JoinRequest, CreateRequest
from .utils import generate_game_id

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = GameManager()


@app.post("/create_game", status_code=status.HTTP_201_CREATED)
async def create_game(create_request: CreateRequest):
    game_id = generate_game_id()
    while manager.create_game(create_request.host_id, game_id) is False:
        game_id = generate_game_id()
    game = manager.get_game(game_id)

    return {"message": "Game created", "game_id": game_id}


@app.post("/join_game", status_code=status.HTTP_201_CREATED)
async def join_game(join_request: JoinRequest):
    game_id = join_request.game_id
    player_id = join_request.player_id

    try:
        game = manager.get_game(game_id)
        await game.add_player(Player(player_id))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "Player added to game"}


@app.websocket("/ws/{game_id}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str, player_id: str):
    await websocket.accept()

    try:
        game = manager.get_game(game_id)
        game.add_websocket_to_player(player_id, websocket)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        while True:
            data = await websocket.receive_text()
            await game.type_character(player_id, data)
    except WebSocketDisconnect:
        game.remove_player(player_id)
        await manager.games[game_id].broadcast_progress()
