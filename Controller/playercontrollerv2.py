import asyncio
import websockets
import json
import subprocess

player_name="Player 1"
# How many times per second the game should update
game_tick_rate=10 

# cmd="C:/intelFPGA_lite/18.1/nios2eds/Nios II Command Shell.bat nios2-terminal"
cmd="nios2-terminal"

process = subprocess.Popen(
    cmd, 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE
)

def signed_16(value):
    return -(value & 0x8000) | (value & 0x7fff)

def map_to_range(num, inMin, inMax, outMin, outMax):
    return outMin + (float(num - inMin) * float(outMax - outMin) / float(inMax - inMin))

async def send_data(websocket):
    x_read = 0
    y_read = 0
    button_0 = 0
    button_1 = 0
    switches = 0
    x_normalised = 0
    y_normalised = 0
    BUTTON = 0
    SWITCH = 0
    
    accelerometer_data = process.stdout.readline()
    if accelerometer_data!=b'' and process.poll() is None:
        output = accelerometer_data.decode("utf-8").strip()
            
        #===== Extract Data =====#
        if (("x_read" in output) and ("y_read" in output) and ("button_0" in output) and ("button_1" in output) and ("switch" in output)):
            x_read = signed_16(int(output.split("\t")[0].split(":")[1].strip(), 16))
            y_read = signed_16(int(output.split("\t")[1].split(":")[1].strip(), 16))
            button_0 = int(output.split("\t")[2].split(":")[1].strip())
            button_1 = int(output.split("\t")[3].split(":")[1].strip())
            switches = int(output.split("\t")[4].split(":")[1].strip(), 16)
                
        #===== Process Data =====#
        x_normalised = map_to_range(x_read, -255, 255, 1, -1)
        y_normalised = map_to_range(y_read, -255, 255, -1, 1)
            
        if button_0 == 1 and button_1 == 0:
            BUTTON = -1
        elif button_0 == 0 and button_1 == 1:
            BUTTON = 1
        else:
            BUTTON = 0
        
        if switches == 1:
            SWITCH = 1
        elif switches == 512:
            SWITCH = -1
        else:
            SWITCH = 0
                
    #===== Package Data =====#
    location_data={'Name': player_name, 'Thrust': SWITCH, 'Pitch': y_normalised, 'Roll': x_normalised, 'Yaw': BUTTON} # Data from accelerometer must be packaged into a dict
    # print("Sent data: ", location_data)
    await websocket.send(json.dumps(location_data))

async def main():
    async with websockets.connect('ws://127.0.0.1:12000', ping_timeout=99999) as websocket:
        while True:
            await send_data(websocket)
            await asyncio.sleep(1/game_tick_rate)
asyncio.run(main())
