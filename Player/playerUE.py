import asyncio
import websockets

player_name="Player 1"

def combine_dict(data):
    data=data.split('_')
    location_data_keys=data[0].split(',')
    location_data_values=data[1].split(',')
    dictionary=dict(zip(location_data_keys,location_data_values))
    return dictionary

async def main():
    async with websockets.connect('ws://127.0.0.1:12000') as websocket:
        while True:
            response=await websocket.recv()
            if (response[0]=='N'):
                data=combine_dict(response)
                print(data) # Name of player and processed data received from server
            elif(response[0]=='W'):
                print(response) # Welcome Message
            await asyncio.sleep(0.5)
            
asyncio.run(main())
