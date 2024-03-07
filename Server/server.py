import asyncio
import websockets

import updatePositions as p
# Dictionary to store clients
clients = {}
# How many times per second the game should update
game_tick_rate=30 

def split_dict(data):
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
    elif len(clients)==2:
        clients[websocket] = "Player 2"
    await broadcast(f"Welcome to the game, {clients[websocket]}")

async def connected_client(websocket):
    # Tracks the number of seconds between each packet sent
    DeltaSeconds=0
    CurrentDataDict={}
    try:
        await new_connection(websocket)
    except:
        print(f"{clients[websocket]} unexpectedly disconnected.")
        del clients[websocket]
    while True:
        try:
            FPGA_Data=await websocket.recv()
        except:
            print(f"{clients[websocket]} unexpectedly disconnected.")
            del clients[websocket]
            break
        TargetDataDict = combine_dict(FPGA_Data)
        CurrentDataDict = await processing(TargetDataDict, CurrentDataDict, 1/game_tick_rate)
        await broadcast(split_dict(CurrentDataDict))
        asyncio.sleep(1/game_tick_rate)
        

async def processing(TargetData, CurrentData, DeltaSeconds):
    # Given by the FPGA
    TargetThrust=float(TargetData['Thrust'])
    TargetPitch=float(TargetData['Pitch'])
    TargetRoll=float(TargetData['Roll'])
    TargetYaw=float(TargetData['Yaw'])
    # Retained from the previous iteration
    CurrentThrust=p.updateThrust(CurrentThrust, TargetThrust, DeltaSeconds)
    CurrentPitch=p.updatePitch(CurrentPitch, TargetPitch, DeltaSeconds)
    CurrentRoll=p.updatePitch(CurrentRoll, TargetRoll, DeltaSeconds)
    CurrentYaw=p.updatePitch(CurrentYaw, TargetYaw, DeltaSeconds)
    CurrentPosition=p.updatePosition(CurrentThrust, TargetThrust, DeltaSeconds)
    CurrentData['Thrust']=str(CurrentThrust)
    CurrentData['Pitch']=str(CurrentThrust)
    CurrentData['Roll']=str(CurrentThrust)
    CurrentData['Yaw']=str(CurrentThrust)
    CurrentData['Position']=str(CurrentPosition)
    return CurrentData

async def broadcast(message):
    for websocket in clients:
        try:
            await websocket.send(message)
        except:
            print(f"Could not broadcast to {clients[websocket]}. Please reconnect.")
            del clients[websocket]
            
async def main():
    # Start the WebSocket server
    server = await websockets.serve(connected_client, "127.0.0.1", 12000)
    server.ping_interval = None
    while True:
        print(f"Number of connected clients: {len(clients)}")
        await asyncio.sleep(5)

# Run the main function
asyncio.run(main())
