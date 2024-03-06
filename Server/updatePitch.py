import unreal as un
import numpy as np
import matplotlib.pyplot as plt

def interpolate_to(current_value, target_value, delta_time, interpolation_speed):
    interpolation_factor = 1.0 - np.exp(-interpolation_speed * delta_time)
    interpolated_value = current_value + interpolation_factor * (target_value - current_value)
    return interpolated_value

def updatePitch(CurrentPitch, TargetPitch, DeltaSeconds, MaxFlapPitch=10, MaxElevatorPitch=25):

    CurrentPitch = interpolate_to(CurrentPitch, TargetPitch, DeltaSeconds, 10)
    
    JetPitch = CurrentPitch * DeltaSeconds * 20
    FlapPitch = un.map_range_clamped(CurrentPitch, -1, 1, MaxFlapPitch, -MaxFlapPitch)
    
    ElevatorPitch = un.map_range_clamped(CurrentPitch, -1, 1, MaxElevatorPitch, -MaxElevatorPitch)
    
    return [JetPitch, FlapPitch, ElevatorPitch]

# Simulation parameters
initial_pitch = 0.0
target_pitch = 30.0
delta_seconds = 0.1
max_steps = 10

# Lists to store pitch values for visualization
jet_pitch_values = []
flap_pitch_values = []
elevator_pitch_values = []

# Simulate the passage of time and observe the interpolation
current_pitch = initial_pitch
for step in range(max_steps):
    pitches = updatePitch(current_pitch, target_pitch, delta_seconds)
    
    jet_pitch_values.append(pitches[0])
    flap_pitch_values.append(pitches[1])
    elevator_pitch_values.append(pitches[2])
    
    current_pitch = pitches[0]  # Update current pitch for the next iteration

# Plotting the results
time_steps = np.arange(0, max_steps * delta_seconds, delta_seconds)

plt.plot(time_steps, jet_pitch_values, label='JetPitch')
plt.plot(time_steps, flap_pitch_values, label='FlapPitch')
plt.plot(time_steps, elevator_pitch_values, label='ElevatorPitch')
plt.xlabel('Time (seconds)')
plt.ylabel('Pitch Values')
plt.legend()
plt.show()