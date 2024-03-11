import asyncio
import websockets
import json

player_name="Player 1"
game_tick_rate=20

async def main():
    async with websockets.connect('ws://127.0.0.1:12000') as websocket:
        while True:
            data=await websocket.recv()
            if data[0]!='W':
                data=json.loads(data)
            print(data)
            await asyncio.sleep(1/game_tick_rate)
            
asyncio.run(main())
