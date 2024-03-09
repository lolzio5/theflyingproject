import asyncio
import websockets
import json

player_name="Player 1"

async def main():
    async with websockets.connect('ws://127.0.0.1:12000') as websocket:
        while True:
            data=await websocket.recv()
            if data[0]!='W':
                data=json.loads(data)
            print(data)
            await asyncio.sleep(0.5)
            
asyncio.run(main())
