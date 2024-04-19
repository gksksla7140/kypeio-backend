import socketio
import asyncio


# Initialize a Socket.IO client
sio_client = socketio.AsyncClient()

# Define event handlers for connect and disconnect events
@sio_client.event
async def connect():
    print("Connected to Socket.IO server")

@sio_client.event
async def disconnect():
    print("Disconnected from Socket.IO server")


async def test_socket_io_connection():
    server_url = "http://localhost:8000"
    game_id = "123"
    player_id = "123"
    try:
        # Connect to the Socket.IO server with the specified game_id and player_id
        await sio_client.connect(
            url=f"{server_url}",
            namespaces="/game",
            headers={"game_id": game_id, "player_id": player_id},
            socketio_path="/ws",
        )

    finally:
        # Disconnect from the Socket.IO server
        await sio_client.disconnect()

# Run the test function
asyncio.run(test_socket_io_connection())
