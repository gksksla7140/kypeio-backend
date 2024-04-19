from os import name
import socketio
import asyncio
import random

# Initialize two Socket.IO clients
sio_client_1 = socketio.AsyncClient()
sio_client_2 = socketio.AsyncClient()

# Define event handlers for connect and disconnect events for client 1
@sio_client_1.event
async def connect():
    print("Client 1: Connected to Socket.IO server")

@sio_client_1.event
async def disconnect():
    print("Client 1: Disconnected from Socket.IO server")

# Define event handlers for connect and disconnect events for client 2
@sio_client_2.event
async def connect():
    print("Client 2: Connected to Socket.IO server")

@sio_client_2.event
async def disconnect():
    print("Client 2: Disconnected from Socket.IO server")

async def send_progress(client, progress):
    await client.emit("progress", {"progress": progress}, namespace="/game")

async def simulate_progress(client):
    progress = 0
    while progress < 100:
        await send_progress(client, progress)
        progress += random.randint(1, 10)
        await asyncio.sleep(1)

async def test_socket_io_connection():
    server_url = "http://localhost:8000/ws"
    game_id = "123"
    player_id_1 = "123"
    player_id_2 = "456"
    try:
        # Connect both clients to the Socket.IO server
        await asyncio.gather(
            sio_client_1.connect(
                url=server_url,
                namespaces="/game",
                headers={"game_id": game_id, "player_id": player_id_1},
                socketio_path="/ws",
            ),
            sio_client_2.connect(
                url=server_url,
                namespaces="/game",
                headers={"game_id": game_id, "player_id": player_id_2},
                socketio_path="/ws",
            )
        )

        # Start simulating progress updates from both clients
        await asyncio.gather(
            simulate_progress(sio_client_1),
            simulate_progress(sio_client_2)
        )

    finally:
        # Disconnect both clients from the Socket.IO server
        await asyncio.gather(
            sio_client_1.disconnect(),
            sio_client_2.disconnect()
        )

# Run the test function
asyncio.run(test_socket_io_connection())
