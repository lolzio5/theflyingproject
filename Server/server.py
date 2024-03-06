import asyncio
import websockets

# Dictionary to store clients
clients = {}
num_players=0
# Set to store closed connections
closed_connections = set()

async def send_data(data, websocket):
        data_keys = list(data.keys())
        data_values = list(data.values())
        data_keys_split = ','.join(data_keys)
        data_values_split = ','.join(data_values)
        return clients[websocket]+data_keys_split+'_'+data_values_split

async def combine_dict(websocket):
        data=(await websocket.recv()).split('_')
        location_data_keys = data[1].split(',')
        location_data_values = data[2].split(',')
        return dict(zip(location_data_keys, location_data_values))

async def new_connection(websocket):
    if num_players==0:
        clients[websocket] = "Player 1"
    elif num_players==1:
        clients[websocket] = "Player 2"
    await broadcast(f"Welcome to the game, {clients[websocket]}")

async def connected_client(websocket):
    try:
        await new_connection(websocket)
    except:
        closed_connections.add(websocket)
        del clients[websocket]
        print(f"Client connection closed unexpectedly.")
    while True:
        try:
            location_data = await combine_dict(websocket)
        except:
            closed_connections.add(websocket)
            del clients[websocket]
            print(f"Client connection closed unexpectedly.")
        processed_data = await location_processing(location_data)
        await broadcast(send_data(processed_data, websocket))

async def broadcast(message):
    for websocket in clients:
        try:
            await websocket.send(message)
        except websockets.exceptions.ConnectionClosedError as e:
            closed_connections.add(websocket)
            del clients[websocket]
            print(f"Error occurred while broadcasting message: {e}. Client disconnected.")

async def location_processing(data):
    data['Location x'] = str(float(data['Location x']) * 50)
    data['Location y'] = str(float(data['Location y']) * 50)
    data['Location z'] = str(float(data['Location z']) * 50)
    return data

async def main():
    # Start the WebSocket server
    server = await websockets.serve(connected_client, "127.0.0.1", 12000)
    server.ping_interval = None
    while True:
        print(f"Number of connected clients: {len(clients)}")
        await broadcast(f"Number of connected clients: {len(clients)}")
        await asyncio.sleep(5)
        closed_connections.clear()  # Clear the set of closed connections

# Run the main function
asyncio.run(main())
