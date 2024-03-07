import numpy as np
import matplotlib.pyplot as plt
from updatePositions import interpolate_to

def normalize_vector(vector):
    length = np.linalg.norm(vector)

    if length != 0:
        normalized_vector = vector / length
    else:
        normalized_vector = vector

    return normalized_vector

def updatePosition(CurrentPosition, CurrentThrust, TargetThrust, DeltaSeconds, Drag=0.25, MinThrust=4000, Gravity=981):
    
    # Get direction vectors by normalizing CurrentPosition
    CurrentForwardPosition = normalize_vector(CurrentPosition)
    # Smooth deceleration
    if TargetThrust < CurrentThrust:
        CurrentThrust = interpolate_to(CurrentThrust, TargetThrust, DeltaSeconds, Drag)
    else:
        CurrentThrust = TargetThrust
    
    # Calculate New Position
    NewPosition = [i * CurrentThrust * DeltaSeconds for i in CurrentForwardPosition]
    
    # Calculate Applied Gravity
    AppliedGravity = np.interp(CurrentThrust, [0, MinThrust], [-Gravity, 0])
    
    # Update Position
    NewPosition[2] -= AppliedGravity * DeltaSeconds

    return [NewPosition, CurrentThrust]


CurrentThrust = 4000
TargetThrust = 3000
CurrentPosition = [0.1,0.2,0.3]
DeltaSeconds = 0.1
time = 0
timestamp = []
value = []
output = [CurrentPosition, CurrentThrust]

for i in range (0, 1000):
    output = updatePosition(output[0], output[1], TargetThrust, DeltaSeconds)
    value.append(normalize_vector(output[0])[2])
    # value.append(output[1])
    time+=1
    timestamp.append(time)

plt.plot(timestamp, value)
plt.show()

