import asyncio
import websockets

player_name="Player 1"

async def send_data(websocket,data):
    data_keys = list(data.keys())
    data_values = list(data.values())
    data_keys_split = ','.join(data_keys)
    data_values_split = ','.join(data_values)
    try:
        await websocket.send(data_keys_split+'_'+data_values_split)
    except:
        print("Couldn't connect to server. Retrying.")

async def main():
    async with websockets.connect('ws://127.0.0.1:12000') as websocket:
        while True:
            location_data = {'Name': player_name, 'x':'0.1', 'y':'0.2', 'z':'0.3'} # Data from accelerometer must be packaged into a dict
            await send_data(websocket,location_data)
            await asyncio.sleep(2)
            
asyncio.run(main())
