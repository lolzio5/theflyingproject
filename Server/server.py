import asyncio
import websockets

# Dictionary to store clients
clients = {}
# Set to store closed connections
closed_connections = set()

def send_data(data):
        data_keys = list(data.keys())
        data_values = list(data.values())
        data_keys_split = ','.join(data_keys)
        data_values_split = ','.join(data_values)
        return data_keys_split+'_'+data_values_split

def combine_dict(data):
        data=data.split('_')
        location_data_keys = data[0].split(',')
        location_data_values = data[1].split(',')
        return dict(zip(location_data_keys, location_data_values))

async def new_connection(websocket):
    if len(clients)==0:
        clients[websocket] = "Player 1"
    elif len(clients)==1:
        clients[websocket] = "Player 2"
    await broadcast(f"Welcome to the game, {clients[websocket]}")

async def connected_client(websocket):
    try:
        await new_connection(websocket)
    except:
        print(f"{clients[websocket]} unexpectedly disconnected.")
        del clients[websocket]
    while True:
        try:
            data=await websocket.recv()
            data_dict = combine_dict(data)
        except:
            print(f"{clients[websocket]} unexpectedly disconnected.")
            del clients[websocket]
            break
        processed_data = await location_processing(data_dict)
        await broadcast(send_data(processed_data))

async def broadcast(message):
    for websocket in clients:
        try:
            await websocket.send(message)
        except:
            print(f"Could not broadcast to {clients[websocket]}. Please reconnect.")
            del clients[websocket]
            
async def location_processing(data):
    data['x'] = str(float(data['x']) * 50)
    data['y'] = str(float(data['y']) * 50)
    data['z'] = str(float(data['z']) * 50)
    return data

async def main():
    # Start the WebSocket server
    server = await websockets.serve(connected_client, "127.0.0.1", 12000)
    server.ping_interval = None
    while True:
        print(f"Number of connected clients: {len(clients)}")
        await asyncio.sleep(5)

# Run the main function
asyncio.run(main())
