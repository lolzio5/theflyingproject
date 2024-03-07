import numpy as np
import matplotlib.pyplot as plt
from updatePositions import interpolate_to

def updatePitch(CurrentPitch, TargetPitch, DeltaSeconds, MaxFlapPitch=10, MaxElevatorPitch=25):

    CurrentPitch = interpolate_to(CurrentPitch, TargetPitch, DeltaSeconds, 10)
    
    JetPitch = CurrentPitch * DeltaSeconds * 20
    
    FlapPitch = np.interp(CurrentPitch, [-1, 1], [-MaxFlapPitch, MaxFlapPitch])
    
    ElevatorPitch = np.interp(CurrentPitch, [-1, 1], [-MaxElevatorPitch, MaxElevatorPitch])
    
    return [JetPitch, -FlapPitch, -ElevatorPitch]

currentpitch = 0
targetpitch = 1
deltaseconds = 0.1
time = 0
timestamp = []
values = []

while currentpitch != targetpitch:
    currentpitch = interpolate_to(currentpitch, targetpitch, deltaseconds, 10)
    time += deltaseconds
    timestamp.append(time)
    values.append(currentpitch)
# plt.plot(timestamp, values)
# plt.show()

FlapPitch = []

for i in values:
    FlapPitch.append(np.interp(i, [-1,1], [-25, 25]))

plt.plot(timestamp, FlapPitch)
plt.show()