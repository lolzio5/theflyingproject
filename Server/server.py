import asyncio
import websockets
import json
import boto3
import dynamoDB.leaderboard as lb
import updatePositions as p

# Dictionary to store clients
clients = {}
# How many times per second the game should update
game_tick_rate=240

# server_ip="0.0.0.0"
server_ip="127.0.0.1"

# Assign a name to a new connection
async def new_connection(websocket):
    name = await websocket.recv()
    clients[websocket] = name
    await broadcast(f"Welcome to the game, {clients[websocket]}")

async def connected_client(websocket):
    # Time between game updates
    DeltaSeconds=1/game_tick_rate
    # Assign a name to a new connection
    try:
        await new_connection(websocket)
        if clients[websocket]=="Player 2":
            StoredDataDict={'Thrust': 4000, 'Pitch': 0, 'Roll': 0, 'Yaw': 0, 'Position':[3593.2771,2131.5019,965]}
        elif clients[websocket]=="Player 1":
            StoredDataDict={'Thrust': 4000, 'Pitch': 0, 'Roll': 0, 'Yaw': 0, 'Position':[2643.669434,32.385994,726.266418]}
    except Exception as e:
        print(f"The exception {e} occured when connecting {clients[websocket]}")
        del clients[websocket]
    
    # Receive data from the server, process it and broadcast to all clients
    while True:
        #######################Update dynamoDB##########################
        dynamodb = boto3.resource('dynamodb')
        json_data = await websockets.recv()
        if lb.update_leaderboard(dynamodb, json_data):
            continue
        
        try:
            FPGA_Data = await websocket.recv()
            print(FPGA_Data)
            TargetDataDict = json.loads(FPGA_Data)
            StoredDataDict, ClientDataDict = processing(TargetDataDict, StoredDataDict, DeltaSeconds)
            ClientDataDict["Name"]=clients[websocket]
            await broadcast(json.dumps(ClientDataDict))
        except Exception as e:
            print(f"{clients[websocket]} disconnected with error {e}")
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

    # Store the current values for the next iteration
    StoredData['Thrust']=Thrust
    StoredData['Pitch']=Pitch[-1]
    StoredData['Roll']=Roll[-1]
    StoredData['Yaw']=Yaw[-1]
    StoredData['Position']=Position
    return StoredData, ClientData

# Broadcast to all connected clients
async def broadcast(message):
    try:
        for websocket in clients:
            await websocket.send(message)
    except:
        print(f"Could not broadcast to {clients[websocket]}. Please reconnect.")
        del clients[websocket]
            
async def main():
    # Start the WebSocket server 
    await websockets.serve(connected_client, server_ip, 12000, ping_timeout=999999)
    while True:
        print(f"Number of connected clients: {len(clients)}")
        await asyncio.sleep(5)

# Run the main function
asyncio.run(main())
