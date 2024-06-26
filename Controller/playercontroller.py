import asyncio
import websockets

import subprocess

player_name="Player 1"

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
    x_read = 0
    y_read = 0
    button_0 = 0
    button_1 = 0
    switches = 0
    x_normalised = 0
    y_normalised = 0
    BUTTON = 0
    SWITCH = 0
    
    async with websockets.connect('ws://127.0.0.1:12000') as websocket:
        output = None
        while True:
            accelerometer_data = process.stdout.readline()
            if accelerometer_data == b'' and process.poll() is not None:
                break
            if accelerometer_data:
                output = accelerometer_data.decode("utf-8").strip()
                # print(output)
                
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
                    
                print("norm x_read: ", x_normalised, "  norm y_read: ", y_normalised, "  BUTTON: ", BUTTON, "  SWITCH: ", SWITCH)

            #===== Send Data =====#
            location_data = {'Name': player_name, 'Thrust': str(SWITCH), 'Pitch': str(y_normalised), 'Roll': str(x_normalised), 'Yaw': str(BUTTON), 'Position':'3,2,4'} # Data from accelerometer must be packaged into a dict
            # await send_data(websocket,location_data)
            # await asyncio.sleep(0.0001)
            
asyncio.run(main())
