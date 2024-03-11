import asyncio
import websockets
import json
import updatePositions as p

# Dictionary to store clients
clients = {}
# How many times per second the game should update
game_tick_rate=15

# Assign a name to a new connection
async def new_connection(websocket):
    if len(clients)==0:
        clients[websocket] = "Player 1"
    elif len(clients)==1:
        clients[websocket] = "Player 1"
    elif len(clients)==2:
        clients[websocket] = "Player 2"
    elif len(clients)==3:
        clients[websocket] = "Player 2"
    await broadcast(f"Welcome to the game, {clients[websocket]}")

async def connected_client(websocket):
    # Time between game updates
    DeltaSeconds=1/game_tick_rate
    StoredDataDict={'Thrust': 4000, 'Pitch': 0, 'Roll': 0, 'Yaw': 0, 'Position':[2643.669434,32.385994,726.266418]}
    # Assign a name to a new connection
    try:
        await new_connection(websocket)
    except Exception as e:
        print(f"The exception {e} occured when connecting {clients[websocket]}")
        del clients[websocket]
    
    # Receive data from the server, process it and broadcast to all clients
    while True:
        try:
            FPGA_Data = await websocket.recv()
            TargetDataDict = json.loads(FPGA_Data)
            StoredDataDict, ClientDataDict = processing(TargetDataDict, StoredDataDict, DeltaSeconds)
            ClientDataDict["Name"]=clients[websocket]
            await broadcast(json.dumps(ClientDataDict))
        except:
            print(f"{clients[websocket]} disconnected")
            del clients[websocket]
            break
        await asyncio.sleep(DeltaSeconds)

def processing(TargetData, StoredData, DeltaSeconds):
    ClientData={}
    
    # Given by the FPGA
    TargetThrust=TargetData['Thrust']
    TargetPitch=TargetData['Pitch']
    TargetRoll=TargetData['Roll']
    TargetYaw=TargetData['Yaw']

    # Calculate new values based on old values
    Pitch=p.updatePitch(StoredData['Pitch'], TargetPitch, DeltaSeconds)
    Roll=p.updateRoll(StoredData['Roll'], TargetRoll, DeltaSeconds)
    Yaw=p.updateYaw(StoredData['Yaw'], TargetYaw, DeltaSeconds)
    Position=p.updatePosition(StoredData['Position'],StoredData['Thrust'], TargetThrust, DeltaSeconds)
    Thrust=p.updateThrust(StoredData['Thrust'], TargetThrust, DeltaSeconds)

    # Output the values to the client
    ClientData['Thrust']=Thrust
    ClientData['JetPitch']=Pitch[0]
    ClientData['FlapPitch']=Pitch[1]
    ClientData['ElevatorPitch']=Pitch[2]
    ClientData['JetRoll']=Roll[0]
    ClientData['RightAileronYaw']=Roll[1]
    ClientData['JetYaw']=Yaw[0]
    ClientData['RudderYaw']=Yaw[1]
    ClientData['XPosition']=Position[0][0]
    ClientData['YPosition']=Position[0][1]
    ClientData['ZPosition']=Position[0][2]

    # Store the current values for the next iteration
    StoredData['Thrust']=Thrust
    StoredData['Pitch']=Pitch[-1]
    StoredData['Roll']=Roll[-1]
    StoredData['Yaw']=Yaw[-1]
    StoredData['Position']=Position[0]
    return StoredData, ClientData

# Broadcast to all connected clients
async def broadcast(message):
    try:
        for websocket in clients:
            if clients[websocket]=="Player 1":
                await websocket.send(message)
            elif clients[websocket]=="Player 2":
                await websocket.send(message)
    except:
        print(f"Could not broadcast to {clients[websocket]}. Please reconnect.")
        del clients[websocket]
            
async def main():
    # Start the WebSocket server
    server = await websockets.serve(connected_client, "127.0.0.1", 12000, ping_timeout=99999)
    while True:
        print(f"Number of connected clients: {len(clients)}")
        await asyncio.sleep(5)

# Run the main function
asyncio.run(main())
