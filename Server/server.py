import asyncio
import websockets
import json
import updatePositions as p

# Dictionary to store clients
clients = {}
# How many times per second the game should update
game_tick_rate=30 

async def new_connection(websocket):
    if len(clients)==0:
        clients[websocket] = "Player 1"
    elif len(clients)==1:
        clients[websocket] = "Player 1's Controller"
    elif len(clients)==2:
        clients[websocket] = "Player 2"
    elif len(clients)==3:
        clients[websocket] = "Player 2's Controller"
    await broadcast(f"Welcome to the game, {clients[websocket]}")

async def connected_client(websocket):
    # Tracks the number of seconds between each packet sent
    DeltaSeconds=1/game_tick_rate
    StoredDataDict={'Thrust': 0, 'Pitch': 0, 'Roll': 0, 'Yaw': 0, 'Position':[3,2,4]}
    try:
        await new_connection(websocket)
    except Exception as e:
        print(f"The exception {e} occured when connecting")
        del clients[websocket]
    while True:
        FPGA_Data = await websocket.recv()
        TargetDataDict = json.loads(FPGA_Data)
        StoredDataDict, ClientDataDict = processing(TargetDataDict, StoredDataDict, DeltaSeconds)
        await broadcast(json.dumps(ClientDataDict))
        await asyncio.sleep(DeltaSeconds)

def processing(TargetData, StoredData, DeltaSeconds):
    ClientData={}
    
    # Given by the FPGA
    TargetThrust=TargetData['Thrust']
    TargetPitch=TargetData['Pitch']
    TargetRoll=TargetData['Roll']
    TargetYaw=TargetData['Yaw']

    # Calculate new values based on old values
    CurrentPitch=p.updatePitch(StoredData['Pitch'], TargetPitch, DeltaSeconds)
    CurrentRoll=p.updateRoll(StoredData['Roll'], TargetRoll, DeltaSeconds)
    CurrentYaw=p.updateYaw(StoredData['Yaw'], TargetYaw, DeltaSeconds)
    CurrentPosition=p.updatePosition(StoredData['Position'],StoredData['Thrust'], TargetThrust, DeltaSeconds)
    if(TargetThrust):
        CurrentThrust=p.updateThrust(StoredData['Thrust'], TargetThrust, DeltaSeconds)
    else:
        CurrentThrust=CurrentPosition[1]
    
    # Output the values to the client
    ClientData['Thrust']=CurrentThrust
    ClientData['Pitch']=CurrentPitch[:-1]
    ClientData['Roll']=CurrentRoll[:-1]
    ClientData['Yaw']=CurrentYaw[:-1]
    ClientData['Position']=CurrentPosition[0]

    # Store the current values for the next iteration
    StoredData['Thrust']=CurrentThrust
    StoredData['Pitch']=CurrentPitch[-1]
    StoredData['Roll']=CurrentRoll[-1]
    StoredData['Yaw']=CurrentYaw[-1]
    StoredData['Position']=CurrentPosition[0]
    return StoredData, ClientData

async def broadcast(message):
    for websocket in clients:
        try:
            await websocket.send(message)
        except:
            print(f"Could not broadcast to all clients. Please reconnect.")
            
async def main():
    # Start the WebSocket server
    server = await websockets.serve(connected_client, "127.0.0.1", 12000)
    server.ping_timeout = None
    while True:
        print(f"Number of connected clients: {len(clients)}")
        await asyncio.sleep(15)

# Run the main function
asyncio.run(main())
