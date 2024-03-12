import subprocess
import time
#from pynput.keyboard    import Controller   as KeyboardController
#from pynput.keyboard    import Key
#from pynput.mouse       import Controller   as MouseController
#from pynput.mouse       import Button

### Command to start the Nios II Terminal
# cmd = "C:/intelFPGA_lite/18.1/nios2eds/Nios II Command Shell.bat nios2-terminal"
cmd = "nios2-terminal"

### Start the Nios II Terminal as a subprocess using python library subprocess
process = subprocess.Popen(
    cmd, 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE
)

#keyboard = KeyboardController()
#mouse = MouseController()

x_read = 0
y_read = 0
x_normalised = 0
y_normalised = 0
button_0 = 0
button_1 = 0
BUTTON = 0
switches = 0
SWITCH = 0

def signed_16(value):
    return -(value & 0x8000) | (value & 0x7fff)

def map_to_range(num, inMin, inMax, outMin, outMax):
    return outMin + (float(num - inMin) * float(outMax - outMin) / float(inMax - inMin))

### Read output from FPGA
output = None
while True:
    accelerometer_data = process.stdout.readline()
    if accelerometer_data == b'' and process.poll() is not None:
        break
    if accelerometer_data:
        output = accelerometer_data.decode("utf-8").strip()
        # print(output)

        ### Extract x_read, y_read, button_0, button_1, switch values from FPGA output
        if (("x" in output) and ("y" in output) and ("b0" in output) and ("b1" in output) and ("s" in output)):
            x_read = signed_16(int(output.split("\t")[0].split(":")[1].strip(), 16))
            y_read = signed_16(int(output.split("\t")[1].split(":")[1].strip(), 16))
            button_0 = int(output.split("\t")[2].split(":")[1].strip())
            button_1 = int(output.split("\t")[3].split(":")[1].strip())
            switches = int(output.split("\t")[4].split(":")[1].strip(), 16)
        
        print("raw x_read: ", x_read, "  raw y_read: ", y_read, "  button_0: ", button_0, "  button_1: ", button_1, "  switches: ", switches)
        
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
            
        # print("raw x_read: ", x_read, "  raw y_read: ", y_read, "  BUTTON: ", BUTTON, "  SWITCH: ", SWITCH)

        ### Map x_read and y_read values to [-1, 1]
        x_normalised = map_to_range(x_read, -255, 255, 1, -1)
        y_normalised = map_to_range(y_read, -255, 255, -1, 1)
        # print("dec x_read: ", x_normalised, "  dec y_read: ", y_normalised)

        ### Simulate mouse movement (for roll and pitch)
        # mouse.position = (x_normalised, y_normalised)
        # print('Now we have moved it to {0}'.format(mouse.position))
        
        ### Simulate yaw
        # {add stuff here}
        
        ### Simulate thrust
        # {add stuff here}