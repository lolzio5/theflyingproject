import asyncio
import websockets

player_name="Player 1"

async def send_data(websocket,data):
    data_keys = list(data.keys())
    data_values = list(data.values())
    data_keys_split = ','.join(data_keys)
    data_values_split = ','.join(data_values)
    try:
        await websocket.send(player_name+'_'+data_keys_split+'_'+data_values_split)
    except:
        print("Couldn't connect to server. Retrying.")
def combine_dict(data):
    data=data.split('_')
    location_data_keys=data[1].split(',')
    location_data_values=data[2].split(',')
    dictionary=zip(location_data_keys,location_data_values)
    dictionary["Name"]=data[0]
    return dictionary

async def main():
    async with websockets.connect('ws://127.0.0.1:12000') as websocket:
        in_game=False
        while True:
            response=await websocket.recv()
            if (response[0]=='P'):
                data=combine_dict(response.split('_'))
                print(data)
            elif(response[0]=='W'):
                in_game=True
                print(response)

            if(in_game):
                location_data = {'Name': player_name, 'x':'0.5050540', 'y':'0.4554', 'z':'0.6464'}
                await send_data(websocket,location_data)
            await asyncio.sleep(2)
            
asyncio.run(main())
