from pynput import keyboard, mouse
import updatePositions as up

stop_script = False
normalized_x = 0
normalized_y = 0

DeltaSeconds = 1
CurrentThrust = 4000
Current = [0,0,0]

def normalize(value, in_min, in_max, out_min, out_max):
    # Map the value from the input range to the output range
    return (value - in_min) / (in_max - in_min) * (out_max - out_min) + out_min

def on_move(x, y):
    global normalized_x, normalized_y
    global DeltaSeconds, Current
    # Define the screen dimensions (adjust these according to your screen resolution)
    screen_width, screen_height = 1920, 1080

    # Normalize the X and Y coordinates to the range [-1, 1]
    normalized_x = normalize(x, 0, screen_width, -1, 1)
    normalized_y = normalize(y, 0, screen_height, -1, 1)

    scaled_x = normalized_x * 360
    scaled_y = normalized_y * 360

    pitch = up.updatePitch(Current[0], scaled_y, DeltaSeconds)[0]
    roll = up.updateRoll(Current[1], scaled_x, DeltaSeconds)[0]
    print(f'Jet Movement: ({pitch}, {roll})')

def on_press(key):
    global stop_script
    if key == keyboard.Key.esc:
        print('Stopping the script...')
        stop_script = True
        return False  # Stop the listener

# Set up the listener
with mouse.Listener(on_move=on_move) as mouse_listener, keyboard.Listener(on_press=on_press) as key_listener:
    while not stop_script:
        key_listener.join()
        
print('Script stopped.')