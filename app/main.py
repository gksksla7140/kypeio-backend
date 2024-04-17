from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    status,
    HTTPException,
    Query,
)
from fastapi.middleware.cors import CORSMiddleware

from .game_manager import GameManager
from .models import Player, JoinRequest, CreateRequest, BaseResponse
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


@app.post(
    "/create_game", status_code=status.HTTP_201_CREATED, response_model=BaseResponse
)
async def create_game(create_request: CreateRequest):
    game_id = generate_game_id()
    while manager.create_game(create_request.host_id, game_id) is False:
        game_id = generate_game_id()
    game = manager.get_game(game_id)
    await game.add_player(Player(create_request.host_id))

    return BaseResponse(
        message="Game created",
        game_detail={
            "game_id": game.game_id,
            "host_id": game.host_id,
            "players": list(game.players.keys()),
        },
    )


@app.post("/join_game", status_code=status.HTTP_201_CREATED)
async def join_game(join_request: JoinRequest):
    game_id = join_request.game_id
    player_id = join_request.player_id

    game = manager.get_game(game_id)
    await game.add_player(Player(player_id))

    return BaseResponse(
        message="Player joined",
        game_detail={
            "game_id": game.game_id,
            "host_id": game.host_id,
            "players": list(game.players.keys()),
        },
    )


@app.get("/game/{game_id}")
async def get_game_details(game_id: str):
    game = manager.get_game(game_id)

    return BaseResponse(
        message="Game details",
        game_detail={
            "game_id": game.game_id,
            "host_id": game.host_id,
            "players": list(game.players.keys()),
        },
    )


@app.websocket("/game/{game_id}/ws")
async def websocket_endpoint(
    websocket: WebSocket, game_id: str, player_id: str = Query(..., min_length=1)
):
    await websocket.accept()

    try:
        game = manager.get_game(game_id)
        game.add_websocket_to_player(player_id, websocket)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        while True:
            typedCount = await websocket.receive_text()
            await game.update_progress()(player_id, typedCount)
    except WebSocketDisconnect:
        game.remove_websocket_from_player(player_id)
