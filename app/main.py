from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    status,
    HTTPException,
    Query,
)
from fastapi.middleware.cors import CORSMiddleware

from app.models import game, player

from .errors import (
    GameNotFoundError,
    PlayerIdAlreadyExistsError,
)
from .sockets import sio_app

from .game_manager import manager
from .models import Player, JoinRequest, CreateRequest, BaseResponse
from .utils import generate_game_id, get_player_statuses_in_game

app = FastAPI()
app.mount("/", app=sio_app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

game_id = "123"
player_id = "123"
manager.create_game(player_id, game_id)
game = manager.get_game(game_id)
game.add_player(Player(player_id))


@app.post(
    "/create_game", status_code=status.HTTP_201_CREATED, response_model=BaseResponse
)
async def create_game(create_request: CreateRequest):
    game_id = generate_game_id()
    while manager.create_game(create_request.host_id, game_id) is False:
        game_id = generate_game_id()
    game = manager.get_game(game_id)
    success = await game.add_player(Player(create_request.host_id))
    if not success:
        raise PlayerIdAlreadyExistsError(create_request.host_id)

    return BaseResponse(
        message="Game created",
        game_detail={
            "game_id": game.game_id,
            "host_id": game.host_id,
            "players": get_player_statuses_in_game(game),
        },
    )


@app.post("/join_game", status_code=status.HTTP_201_CREATED)
async def join_game(join_request: JoinRequest):
    game_id = join_request.game_id
    player_id = join_request.player_id

    game = manager.get_game(game_id)

    if game is None:
        raise GameNotFoundError(game_id)
    success = await game.add_player(Player(player_id))
    if not success:
        raise PlayerIdAlreadyExistsError(player_id)

    return BaseResponse(
        message="Player joined",
        game_detail={
            "game_id": game.game_id,
            "host_id": game.host_id,
            "players": get_player_statuses_in_game(game),
        },
    )
